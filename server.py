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


HEADER = 64

class Server:
    def __init__(self):
        
        if os.path.exists("Config/serversettings.json"):
            with open("Config/serversettings.json") as f:
                config = json.load(f)
            
            self.ip = config.get("serversettings").get("ip")
            self.port = config.get("serversettings").get("port")
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.bind((self.ip, self.port))

        else:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.bind(("localhost", 50000))

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

                if data == 1:
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
                    # Alle Fragen erhalten
                    send(client, "")
                    user = recv(client) # Username empfangen

                    quiz = QuizDatabase("Database/quiz.db", user)
                    query = """
                    SELECT quiz_id, question, category, author, editor, timestamp_creation, timestamp_lastchange
                    FROM quiz ORDER BY quiz_id ASC
                    """
                    quiz._cur.execute(query)

                    send(client, quiz._cur.fetchall()) # Sende alle Fragen an Client
                
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

                    executed = quiz.change_question(*updated)
                    
                    send(client, executed)

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
