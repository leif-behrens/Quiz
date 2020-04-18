#!/usr/bin/python3

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

from database import *
from functions import *


class Server:
    def __init__(self):
                
        Path("./Database").mkdir(parents=True, exist_ok=True)
        Path("./Config").mkdir(parents=True, exist_ok=True)

        if os.path.exists("Config/serversettings.json"):
            with open("Config/serversettings.json") as f:
                config = json.load(f)
            
            self.ip = config.get("serversettings").get("ip")
            self.port = config.get("serversettings").get("port")
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.bind((self.ip, self.port))

        else:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.bind(("", 50000))

    def run(self):
        self.sock.listen()
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
                data = recv(client)

                if not data:
                    client.close()
                    break

                elif data == 1:
                    # Neues Quiz
                    send(client, "")

                    username = recv(client)

                    # Quizdaten werden aus der Datenbank gelesen
                    quiz = QuizDatabase("Database/quiz.db", username)
                    quiz._cur.execute("SELECT * FROM quiz ORDER BY RANDOM() LIMIT 15")
                    data = quiz._cur.fetchall()
                    
                    quiz._conn.close()

                    # Quizdaten werden an den Client gesendet
                    send(client, data)
                
                elif data == 2:
                    # Highscoreliste
                    person = PersonDatabase("Database/user.db")
                    query = """
                    SELECT correct_answers, time_sec, username, timestamp_creation
                    FROM score ORDER BY correct_answers DESC, time_sec ASC LIMIT 25
                    """
                    
                    person._cur.execute(query)

                    send(client, person._cur.fetchall())

                elif data == 3:
                    # Neue Frage erstellen
                    # client.send("Neue Frage".encode())
                    send(client, "")

                    # data = pickle.loads(client.recv(2**12))
                    data = recv(client)
                    
                    quiz = QuizDatabase("Database/quiz.db", data[-1])
                    insert_question = quiz.new_question(*data[0:-1])
                    
                    # client.send(pickle.dumps(insert_question))
                    send(client, insert_question)
                    quiz._conn.close()

                elif data == 4:
                    # Alle Fragen einer bestimmten Kategorie erhalten
                    send(client, "")
                    user, category = recv(client) # Username empfangen

                    quiz = QuizDatabase("Database/quiz.db", user)
                    query = """
                    SELECT quiz_id, question, category, author, editor, timestamp_creation, timestamp_lastchange
                    FROM quiz WHERE category = ?
                    ORDER BY quiz_id ASC
                    """

                    quiz._cur.execute(query, (category,))

                    send(client, quiz._cur.fetchall()) # Sende Fragen an Client
                
                elif data == 5:
                    # Login                    
                    send(client, "")
                    data = recv(client)

                    access = self.check_credentials(*data)
                    send(client, access)

                elif data == 6:
                    # Eine Frage erhalten
                    send(client, "")
                    data = recv(client)    # Erhalte Primary Key der zu bearbeitenden Frage sowie den Username

                    quiz = QuizDatabase("Database/quiz.db", data[1])

                    query = """
                    SELECT question, wrong_answer_1, wrong_answer_2, wrong_answer_3, correct_answer, category
                    FROM quiz 
                    WHERE quiz_id = ?
                    """

                    quiz._cur.execute(query, (data[0],))

                    question = quiz._cur.fetchone()

                    send(client, question)
                
                elif data == 7:
                    # Speichere editierte Frage
                    send(client, "")

                    # Bearbeitete Frage und username
                    # [question, wrong_answer_1, 2, 3, correct_answer, category, username, primarykey]
                    updated = recv(client)

                    quiz = QuizDatabase("Database/quiz.db", updated[-2])

                    response = quiz.change_question(*updated)
                    
                    send(client, response)

                elif data == 8:
                    # Quiz Resultate in Datenbank schreiben
                    send(client, "")

                    # Ergebnisse des Quizes werden empfangen
                    data = recv(client)

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
                    send(client, (insert[0], place_personal, place_global))

                elif data == 9:
                    # Username Check
                    send(client, "")
                    
                    data = recv(client)

                    person = PersonDatabase("Database/user.db")

                    # Es wird versucht, einen neuen User zu erstellen
                    new_user = person.new_user(*data)

                    person._conn.close()

                    send(client, new_user)

                elif data == 10:
                    # Frage löschen
                    send(client, "")
                    username, pk = recv(client)

                    quiz = QuizDatabase("Database/quiz.db", username)
                    
                    delete = quiz.delete_question(pk)

                    send(client, delete)

                    quiz._conn.close()

                elif data == 11:
                    # Alle Kategorien erhalten
                    send(client, "")
                    username = recv(client)

                    quiz = QuizDatabase("Database/quiz.db", username)
                    
                    query = """
                    SELECT DISTINCT category FROM quiz
                    """

                    quiz._cur.execute(query)
                    
                    data = quiz._cur.fetchall()
                    send(client, data)

                    quiz._conn.close()

                elif data == 12:
                    # Check ob User existiert
                    send(client, "")
                    username = recv(client)
                    person = PersonDatabase("Database/user.db")
                    
                    query = """
                    SELECT username FROM user WHERE username = ?
                    """

                    person._cur.execute(query, (username,))

                    send(client, person._cur.fetchone())

                    person._conn.close()

                elif data == 13:
                    # Alle Infos des Users
                    send(client, "")
                    user = recv(client)

                    person = PersonDatabase("Database/user.db")
                    person._cur.execute("SELECT * FROM user WHERE username = ?", (user,))
                    data = person._cur.fetchone()

                    send(client, data)

                    person._conn.close()
                
                elif data == 14:
                    # Editierte Userdaten speichern
                    send(client, "")
                    data = recv(client) # Erhalte Tupel (password, f_name, l_name, email, admin, username)
                    
                    
                    person = PersonDatabase("Database/user.db")
                    
                    try:
                        # Wenn kein neues Passwort gesetzt wird, wird dieses auch nicht upgedatet
                        # Der Hash steht für eine leere Zeichenkette
                        if data[0] == "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855": 
                            query = """
                            UPDATE user 
                            SET
                                f_name = ?, 
                                l_name = ?, 
                                email = ?, 
                                admin = ?
                            WHERE username = ?
                            """

                            person._cur.execute(query, data[1:])
                        
                        else:
                            query = """
                            UPDATE user 
                            SET
                                password = ?, 
                                f_name = ?, 
                                l_name = ?, 
                                email = ?, 
                                admin = ?
                            WHERE username = ?
                            """

                            person._cur.execute(query, data)
                        
                        person._conn.commit()
                        send(client, (True, ""))

                    except Exception as e:
                        send(client, (False, e))
                    
                    finally:                        
                        person._conn.close()

                elif data == 15:
                    # Beanstandete Frage hinzufügen
                    send(client, "")

                    data = recv(client)

                    quiz = QuizDatabase("Database/quiz.db", data[-1])
                    insert = quiz.new_complain(*data)

                    send(client, insert)
                    quiz._conn.close()

                elif data == 16:
                    # Beanstandete Fragen erhalten
                    send(client, "")

                    username = recv(client)
                    
                    quiz = QuizDatabase("Database/quiz.db", username)

                    query = """
                    SELECT complained_questions.*, quiz.*
                    FROM complained_questions
                    INNER JOIN quiz
                    ON complained_questions.quiz_id = quiz.quiz_id;
                    """

                    quiz._cur.execute(query)

                    data = quiz._cur.fetchall()

                    send(client, data)
                    quiz._conn.close()

                elif data == 17:
                    # Lösche beanstandete Frage
                    send(client, "")
                    username, primarykey = recv(client)

                    quiz = QuizDatabase("Database/quiz.db", username)
                    delete = quiz.delete_complain(primarykey)

                    send(client, delete)

                    quiz._conn.close()

                elif data == 18:
                    # Editierte Userdaten speichern
                    send(client, "")
                    data = recv(client) # Erhalte Tupel (password, f_name, l_name, email, pic, picname, username)
                                        
                    person = PersonDatabase("Database/user.db")
                    
                    try:
                        # Wenn kein neues Passwort gesetzt wird, wird dieses auch nicht upgedatet
                        # Der Hash steht für eine leere Zeichenkette
                        if data[0] == "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855": 
                            query = """
                            UPDATE user 
                            SET
                                f_name = ?, 
                                l_name = ?, 
                                email = ?,
                                picture = ?,
                                picname = ?
                            WHERE username = ?
                            """

                            person._cur.execute(query, data[1:])
                        
                        else:
                            query = """
                            UPDATE user 
                            SET
                                f_name = ?, 
                                l_name = ?, 
                                email = ?,
                                picture = ?,
                                picname = ?
                            WHERE username = ?
                            """

                            person._cur.execute(query, data)
                        
                        person._conn.commit()
                        send(client, (True, ""))

                    except Exception as e:
                        send(client, (False, e))
                    
                    finally:                        
                        person._conn.close()


            except Exception as e:
                client.close()
                print(e)
                break

    def check_credentials(self, username, password_hash):
        person = PersonDatabase("Database/user.db")

        access = person.check_access(username, password_hash)
        
        if access:
            person._cur.execute("SELECT admin FROM user WHERE username = ?", (username,))
            data = person._cur.fetchone()[0]
            
            person._conn.close()

            return access, eval(data)

        else:
            person._conn.close()
            return access, False
        
    def __del__(self):
        self.sock.close()


if __name__ == "__main__":
    s = Server()
    s.run()
