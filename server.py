import socket
import pickle
import sqlite3
import json
import threading
import os
import hashlib

# Decorator
def check_permission(username, password):
    def decorator(function):
        def wrapper(*args, **kwargs):
            conn = sqlite3.connect("Database/user.db")
            cur = conn.cursor()
            
            try:
                cur.execute("SELECT password FROM user WHERE username = ?", (username,))
                data = cur.fetchone()
                
                if data is None:
                    return False, "Username does not exists"
                else:
                    if data != password:
                        return False, "Password is not correct"

                    else:
                        return_value = function(*args, **kwargs)
                        return return_value

            except Exception as e:
                return False, e
        return wrapper
    return decorator


class Server:
    def __init__(self):
        
        if os.path.exists("Config/serversettings.json"):
            with open("Config/serversettings.json") as f:
                config = json.load(f)
            
            self.ip = config.get("ip")
            self.port = config.get("port")
            
            try:
                self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.sock.bind((self.ip, self.port))
                self.sock.listen(5)

            except Exception as e:
                self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.sock.bind(("localhost", 50000))
                self.sock.listen(5)
        else:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.bind(("localhost", 50000))
            self.sock.listen(5)

    def run(self):
        while True:
            client, addr = self.sock.accept()                
            threading._start_new_thread(self.new_client_connection, (client, addr))

    def new_client_connection(self, client, addr):
        """
        Sobald ein Client connected, wird diese Methode im neuen Thread aufgerufen
        """
        print(f"Neue eingehende Verbindung von {addr[0]}:{addr[1]}")
        

        while True:
            # Es wird auf neue Daten gewartet. Es handelt sich um vordefinierte Commands
            try:
                data = pickle.loads(client.recv(1024))
                print(data)

                if not data:
                    client.close()

                if data == 1:
                    # Neues Quiz
                    pass

                elif data == 2:
                    # Highscoreliste
                    pass

                elif data == 3:
                    # Neue Frage erstellen
                    pass

                elif data == 4:
                    # Frage bearbeiten/löschen
                    pass
                
                elif data == 5:
                    # Login
                    client.send("Login".encode())
                    data = pickle.loads(client.recv(2**12))
                    
                    access = self.check_credentials(*data)
                    client.send(pickle.dumps(access))

            except Exception as e:
                client.close()
                break
                print(e)
        

    def check_credentials(self, username, password):
        person = PersonDatabase("Database/user.db")

        hashed_password = hashlib.sha256()
        hashed_password.update(password.encode("utf-8"))

        access = person.check_access(username, hashed_password.hexdigest())
        return access


class QuizDatabase:
    def __init__(self, database, username=None, password=None):
        self.username = username
        self.password = password

        person = PersonDatabase("Database/users.db")
        self.permission = person.check_access(username, password)

        # Initialize SQLite3-Connection and create cursor
        self._conn = sqlite3.connect(database)
        self._cur = self._conn.cursor()

        # Create Table if not exist
        query = """
        CREATE TABLE IF NOT EXISTS quiz (
            quiz_id INTEGER PRIMARY KEY AUTOINCREMENT,
            question TEXT,
            wrong_answer_1 TEXT,
            wrong_answer_2 TEXT,
            wrong_answer_3 TEXT,
            correct_answer TEXT,
            category TEXT,
            difficulty_level INTEGER,
            author TEXT,
            editor TEXT,
            timestamp_creation INTEGER,
            timestamp_lastchange INTEGER
        )
        """

        self._cur.execute(query)
        self._conn.commit()

    def new_question(self, question, wrong_answer_1, wrong_answer_2, wrong_answer_3, correct_answer, category, difficulty_level):
        if self.permission:
            query = """
            INSERT INTO quiz (
                question,
                wrong_answer_1,
                wrong_answer_2,
                wrong_answer_3,
                correct_answer,
                category,
                difficulty_level,
                author,
                editor,
                timestamp_creation,
                timestamp_lastchange
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """
            
            try:
                self._cur.execute(query, (question, wrong_answer_1, wrong_answer_2, wrong_answer_3, correct_answer, category, difficulty_level, self.username, self.username, int(time.time()), int(time.time)))
                self._conn.commit()
                
                return True, ""

            except Exception as e:
                return False, e
    
    def change_question(self, primarykey, column, new_value):
        if self.permission:
            query = f"""
            UPDATE quiz 
            SET {column} = ?, editor = ?, timestamp_lastchange = ?
            WHERE quiz_id = ?
            """

            try:
                self._cur.execute(query, (new_value, self.username, int(time.time()), primarykey))
                self._conn.commit()
                return True, ""

            except Exception as e:
                return False, e

    def delete_question(self, primarykey):
        if self.permission:
            query = f"""
            DELETE FROM quiz WHERE quiz_id = ?
            """

            try:
                self._cur.execute(query, (primarykey))
                self._conn.commit()
                return True, ""
            
            except Exception as e:
                return False, e
    

class PersonDatabase:
    def __init__(self, database, admin=False):
        self._conn = sqlite3.connect(database)
        self._cur = self._conn.cursor()

        self.admin = admin

        query = """
        CREATE TABLE IF NOT EXISTS user (
            username TEXT PRIMARY KEY,
            password TEXT,
            f_name TEXT,
            l_name TEXT,
            email TEXT,
            admin BOOL
        )
        """

        self._cur.execute(query)
        self._conn.commit()

    def new_user(self, username, password_hash, f_name, l_name, email, admin=False):
        # Check if username exists
        exists = self._cur.execute("SELECT * FROM user WHERE username = ?", (username,))

        if exists is None:
            query = """
            INSERT INTO user (username, password, f_name, l_name, email, admin) VALUES (
                ?, ?, ?, ?, ?, ?
            )
            """
            try:
                self._cur.execute(query, (username, password_hash, f_name, l_name, admin))
                self._conn.commit()
                return True, ""

            except Exception as e:
                return False, e
        
        else:
            return False, "Username already exists"
    
    def check_access(self, username, hashed_password):
        query = """
        SELECT password FROM user WHERE username = ?
        """

        self._cur.execute(query, (username,))

        data = self._cur.fetchone()
        

        if data is None:
            return False

        else:
            if hashed_password == data[0]:
                return True
            else:
                return False


if __name__ == "__main__":
    s = Server()
    s.run()
    # d = QuizDatabase("Database/quiz.db")
    # print(d.new_question("owqnf", "ik", "omo", "oikm", "ownergfiou", "aaa", 13))
    # d.change_question(1, "question", "qssdfsf")
