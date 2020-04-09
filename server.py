import socket
import pickle
import sqlite3
import json
import threading
import os
import hashlib
import time
import random
import sys

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
            
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.bind((self.ip, self.port))
            self.sock.listen(5)

        else:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.bind(("localhost", 50000))
            self.sock.listen(5)

    def run(self):
        while True:
            client, addr = self.sock.accept()                
            threading._start_new_thread(self._new_client_connection, (client, addr))

    def _new_client_connection(self, client, addr):
        """
        Sobald ein Client connected, wird diese Methode im neuen Thread aufgerufen
        """
        print(f"Neue eingehende Verbindung von {addr[0]}:{addr[1]}")
        

        while True:
            # Es wird auf neue Daten gewartet. Es handelt sich um vordefinierte Commands
            try:
                data = pickle.loads(client.recv(1024))

                if not data:
                    client.close()
                    break

                if data == 1:
                    # Neues Quiz
                    client.send("Neues Quiz".encode())
                    username = pickle.loads(client.recv(1024))

                    # Quizdaten werden aus der Datenbank gelesen
                    quiz = QuizDatabase("Database/quiz.db", username)
                    quiz._cur.execute("SELECT * FROM quiz ORDER BY RANDOM() LIMIT 15")
                    data = quiz._cur.fetchall()
                    quiz._conn.close()

                    # Quizdaten werden an den Client gesendet
                    client.send(pickle.dumps(data))

                    # Ergebnisse des Quizes werden empfangen
                    data = pickle.loads(client.recv(2**12))

                    # Hier werden die empfangenen Daten in die Datenbank geschrieben
                    person = PersonDatabase("Database/user.db")
                    
                    # Überprüfung, ob der Datensatz geschrieben werden konnte
                    insert = person.new_score(data[0], data[1], data[2])

                    person._conn.close()

                    # DB wurde zunächst geschlossen um sicherzustellen, dass der letzte Eintrag schon
                    # geschrieben wurde                    
                    person = PersonDatabase("Database/user.db")

                    place_personal = person.check_score_by_username(data[2], data[0], data[1])
                    place_global = person.check_score_by_global(data[0], data[1])
                    
                    person._conn.close()
                    
                    # Der Bool der Überprüfung wird an den Client gesendet
                    client.send(pickle.dumps((insert[0], place_personal, place_global)))                   

                elif data == 2:
                    # Highscoreliste
                    person = PersonDatabase("Database/user.db")
                    query = """
                    SELECT correct_answers, time_sec, username, timestamp_creation
                    FROM score ORDER BY correct_answers DESC, time_sec ASC LIMIT 25
                    """
                    
                    person._cur.execute(query)

                    client.send(pickle.dumps(person._cur.fetchall()))


                elif data == 3:
                    # Neue Frage erstellen
                    client.send("Neue Frage".encode())

                    data = pickle.loads(client.recv(2**12))
                    
                    quiz = QuizDatabase("Database/quiz.db", data[-1])
                    insert_question = quiz.new_question(*data[0:-1])
                    
                    client.send(pickle.dumps(insert_question))
                    quiz._conn.close()

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
        
        if access:
            person._cur.execute("SELECT admin FROM user WHERE username = ?", (username,))

            return access, eval(person._cur.fetchone()[0])

        else:
            return access, False
        
        person._conn.close()


class QuizDatabase:
    def __init__(self, database, username):
        self.username = username

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
            author TEXT,
            editor TEXT,
            timestamp_creation INTEGER,
            timestamp_lastchange INTEGER
        )
        """

        self._cur.execute(query)
        self._conn.commit()

    def new_question(self, question, wrong_answer_1, wrong_answer_2, wrong_answer_3, correct_answer, category):

        query = """
        INSERT INTO quiz (
            question,
            wrong_answer_1,
            wrong_answer_2,
            wrong_answer_3,
            correct_answer,
            category,
            author,
            editor,
            timestamp_creation,
            timestamp_lastchange
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
        
        try:
            self._cur.execute(query, (question, wrong_answer_1, wrong_answer_2, wrong_answer_3, correct_answer, category, self.username, self.username, int(time.time()), int(time.time())))
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
    
        self._conn.close()        

    def __del__(self):
        self._conn.close()


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

        query = """
        CREATE TABLE IF NOT EXISTS score (
            score_id INTEGER PRIMARY KEY AUTOINCREMENT,
            correct_answers INTEGER,
            time_sec REAL,
            username TEXT,
            timestamp_creation INTEGER,
            FOREIGN KEY(username) REFERENCES user(username)
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

    def new_score(self, correct_answers, time_sec, username):
        query = """
        INSERT INTO score (correct_answers, time_sec, username, timestamp_creation) VALUES (
            ?, ?, ?, ?
        )
        """

        try:
            self._cur.execute(query, (correct_answers, time_sec, username, int(time.time())))
            self._conn.commit()
            return True, ""
        
        except Exception as e:
            return False, e

    def check_score_by_username(self, username: str, score: int, time_needed: float):
        """
        :param username: String -> Username
        :param score: Integer -> Erzielter Score
        :param time_needed: Float -> Erzielte Zeit
        :return: Integer -> Platz der eigenen Scores. 0 wird returnt, wenn es keine Übereinstimmung gibt
        """

        query = """
        SELECT correct_answers, time_sec FROM score 
            WHERE username = ?
            ORDER BY correct_answers DESC, time_sec ASC
        """

        self._cur.execute(query, (username,))
        data = self._cur.fetchall()

        index = 0

        for d in data:
            if d[0] == score and d[1] == time_needed:
                return index + 1
            index += 1
        
        return 0
    
    def check_score_by_global(self, score: int, time_needed: float):
        """
        :param score: Integer -> Erzielter Score
        :param time_needed: FLoat -> Erzielte Zeit
        :return: Integer -> Globaler Platz im Ranking
        """

        query = """
        SELECT correct_answers, time_sec FROM score
            ORDER BY correct_answers DESC, time_sec ASC
        """

        self._cur.execute(query)
        data = self._cur.fetchall()

        index = 0
        
        for d in data:
            if d[0] == score and d[1] == time_needed:
                return index + 1
            index += 1
        
        return 0

    def __del__(self):
        self._conn.close()


if __name__ == "__main__":
    s = Server()
    s.run()
    # d = PersonDatabase("Database/user.db")
    # print(d.check_score_by_global(3, 4.44))
    # print(d.check_score_by_username("lbehrens2", 3, 6.68))

    # d = QuizDatabase("Database/quiz.db", "lbehrens2")
    # print(d.new_question("Aadfsdfsdf", "sdfew", "q", "xvbftg", "rgeergerge", "23234"))
    # p = PersonDatabase("Database/user.db")
