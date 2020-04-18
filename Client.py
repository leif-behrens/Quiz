import socket
import pickle
import sqlite3
import json
import threading
import os
import sys
import time
import random
import datetime
from pathlib import Path
import hashlib

from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

from functions import *
from widgets import *


class Client(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.setMinimumSize(750, 500)
        self.setWindowTitle("Quiz")
        self.width = self.frameGeometry().width()
        self.height = self.frameGeometry().height()

        Path("./Database").mkdir(parents=True, exist_ok=True)
        Path("./Config").mkdir(parents=True, exist_ok=True)
        Path("./Temp").mkdir(parents=True, exist_ok=True)
        
        self.init_layouts()

        self.connected = False
        self.authenticated = False
        self.admin = False
        

        if os.path.exists("Config/clientsettings.json"):
            with open("Config/clientsettings.json") as f:
                try:
                    self.settings = json.load(f)
                    
                    self.login_widget_main.le_ip.setText(str(self.settings.get("serversettings").get("ip")))
                    self.login_widget_main.le_port.setText(str(self.settings.get("serversettings").get("port")))
                    self.login_widget_main.le_username.setText(str(self.settings.get("usersettings").get("username")))
                    self.login_widget_main.le_password.setText(str(self.settings.get("usersettings").get("password")))
                    
                    self.connect_to_server()

                except Exception as e:
                    self.settings = {}
                    print(e)
        else:
            self.settings = {}

        # Initialisiere Quiz-Varibalen
        self.current_index = 0
        self.correct_counter = 0
        self.questions = []
        self.answers = {}
        self.quiz_time_start = 0
        self.complained_questions = []
        self.complained_questions_current_primarykey = 0

        self.timer = QTimer(self)
        self.timer.timeout.connect(self._refresh)
        self.timer.start(10000)
        
        self.show_home()

    def connect_to_server(self):
        if not self.connected:
            if self.settings:
                
                try:
                    self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    self.client.connect((self.settings.get("serversettings").get("ip"), self.settings.get("serversettings").get("port")))
                    self.client.settimeout(3)
                    
                    self.connected = True

                    self.home_widget_main.lb_server_status.setText(f"Verbunden mit Server '{self.settings.get('serversettings').get('ip')}:{self.settings.get('serversettings').get('port')}'")
                    self.home_widget_main.lb_server_status.setStyleSheet("color: green")
                    
                    self.authentication()

                except Exception as e:
                    self.connected = False
                    self.authenticated = False
                    self.home_widget_main.lb_server_status.setText("Mit keinem Server verbunden")
                    self.home_widget_main.lb_server_status.setStyleSheet("color: red")
                    
                    self.home_widget_main.lb_login_status.setText("Nicht angemeldet")
                    self.home_widget_main.lb_login_status.setStyleSheet("color: red")
                    self.client.close()
                    
                    print(e)
    
        else:
            self.connected = False
            self.authenticated = False
            self.connect_to_server()
            self.authentication()
 
    def authentication(self):
        if self.connected:
            if self.settings:
                try:
                    # Code für Login
                    send(self.client, 5)

                    sha256 = hashlib.sha256()
                    sha256.update(self.settings.get("usersettings").get("password").encode())

                    credentials = [self.settings.get("usersettings").get("username"), sha256.hexdigest()]

                    # Pseudo
                    recv(self.client)

                    try:

                        send(self.client, credentials)

                        # access
                        response = recv(self.client)
                        self.authenticated = response[0]
                        self.admin = response[1]
                        
                        if self.authenticated:
                            self.home_widget_main.lb_login_status.setText(f"Angemeldet als '{self.settings.get('usersettings').get('username')}'")
                            self.home_widget_main.lb_login_status.setStyleSheet("color: green")
                        else:
                            self.home_widget_main.lb_login_status.setText("Nicht angemeldet")
                            self.home_widget_main.lb_login_status.setStyleSheet("color: red")
                            self.home_widget_main.lb_status.setText("Anmeldung schlug fehl")
                            self.home_widget_main.lb_status.setStyleSheet("color: red")

                    except Exception as e:
                        print(e)

                except Exception as e:
                    print(e)

    def save_new_question(self):
        if self.connected:
            if self.authenticated:
                if self.admin:
                    # Check der Eingabedaten
                    check_entry = True

                    if not self.new_question_widget_main.le_question.text().split():
                        self.new_question_widget_main.le_question.setStyleSheet("border: 1px solid red")
                        check_entry = False
                    else:
                        self.new_question_widget_main.le_question.setStyleSheet("border: 1px solid black")
                    
                    if not self.new_question_widget_main.le_correct_answer.text().split():
                        self.new_question_widget_main.le_correct_answer.setStyleSheet("border: 1px solid red")
                        check_entry = False
                    else:
                        self.new_question_widget_main.le_correct_answer.setStyleSheet("border: 1px solid black")
                    
                    if not self.new_question_widget_main.le_wrong_answer_1.text().split():
                        self.new_question_widget_main.le_wrong_answer_1.setStyleSheet("border: 1px solid red")
                        check_entry = False
                    else:
                        self.new_question_widget_main.le_wrong_answer_1.setStyleSheet("border: 1px solid black")

                    if not self.new_question_widget_main.le_wrong_answer_2.text().split():
                        self.new_question_widget_main.le_wrong_answer_2.setStyleSheet("border: 1px solid red")
                        check_entry = False
                    else:
                        self.new_question_widget_main.le_wrong_answer_2.setStyleSheet("border: 1px solid black")

                    if not self.new_question_widget_main.le_wrong_answer_3.text().split():
                        self.new_question_widget_main.le_wrong_answer_3.setStyleSheet("border: 1px solid red")
                        check_entry = False
                    else:
                        self.new_question_widget_main.le_wrong_answer_3.setStyleSheet("border: 1px solid black")

                    if not self.new_question_widget_main.le_category.text().split():
                        self.new_question_widget_main.le_category.setStyleSheet("border: 1px solid red")
                        check_entry = False
                    else:
                        self.new_question_widget_main.le_category.setStyleSheet("border: 1px solid black")
                    
                    if check_entry:
                        try:
                            send(self.client, 3)    # Code neue Frage erstellen
                            recv(self.client)   # Pseudo
                            
                            data = (self.new_question_widget_main.le_question.text(), self.new_question_widget_main.le_wrong_answer_1.text(),
                                    self.new_question_widget_main.le_wrong_answer_2.text(), self.new_question_widget_main.le_wrong_answer_3.text(),
                                    self.new_question_widget_main.le_correct_answer.text(), self.new_question_widget_main.le_category.text(), 
                                    self.login_widget_main.le_username.text())

                            send(self.client, data)

                            response = recv(self.client)
                            
                            if response[0]:
                                self.home_widget_main.lb_status.setText("Frage erfolgreich gespeichert")
                                self.home_widget_main.lb_status.setStyleSheet("color: green;")
                            else:
                                self.home_widget_main.lb_status.setText(f"Fehler ist aufgetreten: {response[1]}")
                                self.home_widget_main.lb_status.setStyleSheet("color: red;")
                        
                        except Exception as e:
                            self.connected = False
                            self.authenticated = False
                            self.home_widget_main.lb_server_status.setText("Mit keinem Server verbunden")
                            self.home_widget_main.lb_server_status.setStyleSheet("color: red")
                            
                            self.home_widget_main.lb_login_status.setText("Nicht angemeldet")
                            self.home_widget_main.lb_login_status.setStyleSheet("color: red")
                            self.client.close()
                            print(e)
                        
                        finally:                                
                            self.new_question_widget_main.le_question.clear()
                            self.new_question_widget_main.le_correct_answer.clear()
                            self.new_question_widget_main.le_wrong_answer_1.clear()
                            self.new_question_widget_main.le_wrong_answer_2.clear()
                            self.new_question_widget_main.le_wrong_answer_3.clear()
                            self.new_question_widget_main.le_category.clear()
                            self.show_home()

                    else:
                        print("Falsche Eingabe")

    def save_edit_question(self):
        if self.connected:
            if self.authenticated:
                if self.admin:
                    # Check der Eingabedaten
                    check_entry = True

                    if not self.edit_question_widget_2_main.le_edit_question.text().split():
                        self.edit_question_widget_2_main.le_edit_question.setStyleSheet("border: 1px solid red")
                        check_entry = False
                    else:
                        self.edit_question_widget_2_main.le_edit_question.setStyleSheet("border: 1px solid black")
                    
                    if not self.edit_question_widget_2_main.le_edit_correct_answer.text().split():
                        self.edit_question_widget_2_main.le_edit_correct_answer.setStyleSheet("border: 1px solid red")
                        check_entry = False
                    else:
                        self.edit_question_widget_2_main.le_edit_correct_answer.setStyleSheet("border: 1px solid black")
                    
                    if not self.edit_question_widget_2_main.le_edit_wrong_answer_1.text().split():
                        self.edit_question_widget_2_main.le_edit_wrong_answer_1.setStyleSheet("border: 1px solid red")
                        check_entry = False
                    else:
                        self.edit_question_widget_2_main.le_edit_wrong_answer_1.setStyleSheet("border: 1px solid black")

                    if not self.edit_question_widget_2_main.le_edit_wrong_answer_2.text().split():
                        self.edit_question_widget_2_main.le_edit_wrong_answer_2.setStyleSheet("border: 1px solid red")
                        check_entry = False
                    else:
                        self.edit_question_widget_2_main.le_edit_wrong_answer_2.setStyleSheet("border: 1px solid black")

                    if not self.edit_question_widget_2_main.le_edit_wrong_answer_3.text().split():
                        self.edit_question_widget_2_main.le_edit_wrong_answer_3.setStyleSheet("border: 1px solid red")
                        check_entry = False
                    else:
                        self.edit_question_widget_2_main.le_edit_wrong_answer_3.setStyleSheet("border: 1px solid black")

                    if not self.edit_question_widget_2_main.le_edit_category.text().split():
                        self.edit_question_widget_2_main.le_edit_category.setStyleSheet("border: 1px solid red")
                        check_entry = False
                    else:
                        self.edit_question_widget_2_main.le_edit_category.setStyleSheet("border: 1px solid black")
                    
                    if check_entry:
                        try:
                            send(self.client, 7)    # Code, um die editierte Frage zu speichern
                            recv(self.client)   # Pseudo

                            data = (self.edit_question_widget_2_main.le_edit_question.text(), 
                                    self.edit_question_widget_2_main.le_edit_wrong_answer_1.text(),
                                    self.edit_question_widget_2_main.le_edit_wrong_answer_2.text(),
                                    self.edit_question_widget_2_main.le_edit_wrong_answer_3.text(),
                                    self.edit_question_widget_2_main.le_edit_correct_answer.text(),
                                    self.edit_question_widget_2_main.le_edit_category.text(),
                                    self.login_widget_main.le_username.text(),
                                    self.edit_question_widget_1_main.tw_edit_question.item(self.edit_question_widget_1_main.tw_edit_question.currentRow(), 0).text())
                            
                            send(self.client, data)

                            response = recv(self.client)
                            
                            if response[0]:
                                print("Frage erfolgreich gespeichert")
                            else:
                                print(f"Fehler ist aufgetreten: {response[1]}")
                        
                        except Exception as e:
                            self.connected = False
                            self.authenticated = False
                            self.home_widget_main.lb_server_status.setText("Mit keinem Server verbunden")
                            self.home_widget_main.lb_server_status.setStyleSheet("color: red")
                            
                            self.home_widget_main.lb_login_status.setText("Nicht angemeldet")
                            self.home_widget_main.lb_login_status.setStyleSheet("color: red")
                            self.client.close()
                            print(e)
                        
                        finally:                                
                            self.new_question_widget_main.le_question.clear()
                            self.new_question_widget_main.le_correct_answer.clear()
                            self.new_question_widget_main.le_wrong_answer_1.clear()
                            self.new_question_widget_main.le_wrong_answer_2.clear()
                            self.new_question_widget_main.le_wrong_answer_3.clear()
                            self.new_question_widget_main.le_category.clear()
                            self.show_home()

                    else:
                        print("Falsche Eingabe")

    def delete_question(self):
        try:
            send(self.client, 10)   # Code für Löschen
            recv(self.client)   # Pseudo
            send(self.client, (self.login_widget_main.le_username.text(), self.edit_question_widget_1_main.tw_edit_question.item(self.edit_question_widget_1_main.tw_edit_question.currentRow(), 0).text()))     # Username und Primary Key
            response = recv(self.client)   # Bestätigung, ob die Frage gelöscht wurde
            
            if response[0]:
                self.home_widget_main.lb_status.setText("Frage gelöscht")
                self.home_widget_main.lb_status.setStyleSheet("color: green;")
            else:
                self.home_widget_main.lb_status.setText(f"Frage konnte nicht gelöscht werden. Fehler: {response[1]}")
                self.home_widget_main.lb_status.setStyleSheet("color: red;")

            self.show_home()

        except Exception as e:
            self.connected = False
            self.authenticated = False
            self.home_widget_main.lb_server_status.setText("Mit keinem Server verbunden")
            self.home_widget_main.lb_server_status.setStyleSheet("color: red")
            
            self.home_widget_main.lb_login_status.setText("Nicht angemeldet")
            self.home_widget_main.lb_login_status.setStyleSheet("color: red")

            self.home_widget_main.lb_status.setText(f"Frage konnte nicht gelöscht werden.")
            self.home_widget_main.lb_status.setStyleSheet("color: red;")

            self.show_home()

            self.client.close()
            
            print(e)

    def save_execute_config(self):
        temp_config = {"serversettings": {},
                        "usersettings": {}}
        
        temp_config["serversettings"]["ip"] = self.login_widget_main.le_ip.text()
        temp_config["serversettings"]["port"] = int(self.login_widget_main.le_port.text())
        temp_config["usersettings"]["username"] = self.login_widget_main.le_username.text()
        temp_config["usersettings"]["password"] = self.login_widget_main.le_password.text()
        
        Path("./Config").mkdir(parents=True, exist_ok=True)

        with open("Config/clientsettings.json", "w") as f:
            json.dump(temp_config, f, indent=4)
            
        self.settings = temp_config
            
        self.connect_to_server()
        
        self.show_home()

    def _start_new_quiz(self):
        try:
            # Initialisiere Quiz-Varibalen
            self.current_index = 0
            self.correct_counter = 0
            self.questions = []
            self.answers = {}
            self.quiz_time_start = time.time()

            send(self.client, 1)
            # self.client.send(pickle.dumps(1))
            recv(self.client)   # Pseudo
            # self.client.recv(2**16)
            send(self.client, self.settings.get('usersettings').get('username'))    # Username wird gesendet
            # self.client.send(pickle.dumps(self.settings.get('usersettings').get('username')))

            # Erhalte eine Liste mit Tuples für jede Frage (insgesamt 15)
            # (quiz_id, question, wrong_answer_1, wrong_answer_2, wrong_answer_3, correct_answer,
            # category, author, editor, timestamp_creation, timestamp_lastchange)
            self.questions = recv(self.client)

            if len(self.questions) == 15:                
                self.show_new_quiz_2()

            else:
                self.home_widget_main.lb_status.setText("Nicht genügend Fragen vorhanden.")
                self.home_widget_main.lb_status.setStyleSheet("color: red;")
                self.show_home()
                
            
        except Exception as e:
            self.connected = False
            self.authenticated = False
            self.home_widget_main.lb_server_status.setText("Mit keinem Server verbunden")
            self.home_widget_main.lb_server_status.setStyleSheet("color: red")
            
            self.home_widget_main.lb_login_status.setText("Nicht angemeldet")
            self.home_widget_main.lb_login_status.setStyleSheet("color: red")
            self.client.close()
            
            print(e)

    def _next(self, answer):
        self.new_quiz_widget_2_main.te_question.clear()
        
        self.answers[self.current_index] = answer
        if answer == self.questions[self.current_index][5]:
            self.correct_counter += 1

        self.current_index += 1

        if self.current_index < 15:
            current_question = self.questions[self.current_index]
            random.seed()
            random_order = list(current_question[2:6])
            random.shuffle(random_order)

            self.new_quiz_widget_2_main.lb_question_number.setText(f"Frage {self.current_index+1}")
            self.new_quiz_widget_2_main.te_question.insertPlainText(current_question[1])
            self.new_quiz_widget_2_main.te_answer_1.setText(random_order[0])
            self.new_quiz_widget_2_main.te_answer_2.setText(random_order[1])
            self.new_quiz_widget_2_main.te_answer_3.setText(random_order[2])
            self.new_quiz_widget_2_main.te_answer_4.setText(random_order[3])
        
        elif self.current_index == 15:
            self.show_results()

    def fill_highscore(self):
        self.highscore.tw_highscore.clear()
        self.highscore.tw_highscore.setColumnCount(4)
        self.highscore.tw_highscore.setRowCount(25)

        self.highscore.tw_highscore.setHorizontalHeaderLabels(["Score", "Zeit", "Username", "Datum"])

        header = self.highscore.tw_highscore.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.Stretch)
        header.setSectionResizeMode(1, QHeaderView.Stretch)
        header.setSectionResizeMode(2, QHeaderView.Stretch)
        header.setSectionResizeMode(3, QHeaderView.Stretch)

        try:
            send(self.client, 2)    # Code für Highscoreliste füllen
            data = recv(self.client)    # Daten erhalten

            for n, element in enumerate(data):
                self.highscore.tw_highscore.setItem(n, 0, QTableWidgetItem(str(element[0])))
                self.highscore.tw_highscore.setItem(n, 1, QTableWidgetItem(str(element[1])))
                self.highscore.tw_highscore.setItem(n, 2, QTableWidgetItem(str(element[2])))
                self.highscore.tw_highscore.setItem(n, 3, QTableWidgetItem(str(datetime.datetime.fromtimestamp(element[3]).strftime('%d.%m.%Y %H:%M:%S'))))            

        except Exception as e:
            self.connected = False
            self.authenticated = False
            self.home_widget_main.lb_server_status.setText("Mit keinem Server verbunden")
            self.home_widget_main.lb_server_status.setStyleSheet("color: red")
            
            self.home_widget_main.lb_login_status.setText("Nicht angemeldet")
            self.home_widget_main.lb_login_status.setStyleSheet("color: red")
            self.client.close()
            
            print(e)

    def create_account(self):
        check_entry = True

        if not self.new_account_widget_main.le_fname.text().split():
            self.new_account_widget_main.le_fname.setStyleSheet("border: 1px solid red")
            check_entry = False
        else:
            self.new_account_widget_main.le_fname.setStyleSheet("border: 1px solid black")

        if not self.new_account_widget_main.le_lname.text().split():
            self.new_account_widget_main.le_lname.setStyleSheet("border: 1px solid red")
            check_entry = False
        else:
            self.new_account_widget_main.le_lname.setStyleSheet("border: 1px solid black")

        if not self.new_account_widget_main.le_email.text().split():
            self.new_account_widget_main.le_email.setStyleSheet("border: 1px solid red")
            check_entry = False
        else:
            self.new_account_widget_main.le_email.setStyleSheet("border: 1px solid black")
        
        if not self.new_account_widget_main.le_username.text().split():
            self.new_account_widget_main.le_username.setStyleSheet("border: 1px solid red")
            check_entry = False
        else:
            self.new_account_widget_main.le_username.setStyleSheet("border: 1px solid black")

        if check_entry:
            send(self.client, 9)    # Code zum erstellen eines Accounts
            recv(self.client)   # Pseudo

            sha256 = hashlib.sha256()
            sha256.update(self.new_account_widget_main.le_password.text().encode())

            pic = b""
            pic_name = ""

            if os.path.exists(self.new_account_widget_main.path[0]):
                with open(self.new_account_widget_main.path[0], "rb") as f:
                    pic = f.read()
                    pic_name = os.path.basename(self.new_account_widget_main.path[0])
            

            data = [self.new_account_widget_main.le_username.text(), sha256.hexdigest(), 
                    self.new_account_widget_main.le_fname.text(), self.new_account_widget_main.le_lname.text(),
                    self.new_account_widget_main.le_email.text(), False, pic, pic_name]
            
            send(self.client, data)

            response = recv(self.client)

            if response[0]:
                self.new_account_widget_main.lb_status.setText("Account wurde erstellt")
                self.new_account_widget_main.lb_status.setStyleSheet("color: green;")

                self.login_widget_main.le_username.setText(self.new_account_widget_main.le_username.text())
                self.login_widget_main.le_password.setText(self.new_account_widget_main.le_password.text())

                self.new_account_widget_main.le_fname.clear()
                self.new_account_widget_main.le_lname.clear()
                self.new_account_widget_main.le_email.clear()
                self.new_account_widget_main.le_username.clear()
                self.new_account_widget_main.le_password.clear()

            else:
                if response[1] == "Username already exists":
                    self.new_account_widget_main.lb_status.setText("Der Benutzername existiert bereits")
                    self.new_account_widget_main.lb_status.setStyleSheet("color: red;")

                    self.new_account_widget_main.le_username.clear()
                    self.new_account_widget_main.le_password.clear()
                
                else:
                    self.new_account_widget_main.lb_status.setText(f"Account konnte nicht erstellt werden. Folgender Fehler ist aufgetreten: {response[1]}")
                    self.new_account_widget_main.lb_status.setStyleSheet("color: red;")

                    self.new_account_widget_main.le_fname.clear()
                    self.new_account_widget_main.le_lname.clear()
                    self.new_account_widget_main.le_email.clear()
                    self.new_account_widget_main.le_username.clear()
                    self.new_account_widget_main.le_password.clear()
        else:
            self.new_account_widget_main.lb_status.setText("Bitte alle Felder ausfüllen")
            self.new_account_widget_main.lb_status.setStyleSheet("color: red;")

    def _fill_edit_table(self):
        self.edit_question_widget_1_main.tw_edit_question.clear()
        self.edit_question_widget_1_main.tw_edit_question.setColumnCount(7)
        self.edit_question_widget_1_main.tw_edit_question.setRowCount(0)

        self.edit_question_widget_1_main.tw_edit_question.verticalHeader().hide()
        self.edit_question_widget_1_main.tw_edit_question.setHorizontalHeaderLabels(["Quiz-ID", "Frage", "Kategorie", "Autor", "Letzter Bearbeiter", "Erstellungsdatum", "Änderungsdatum"])

        header = self.edit_question_widget_1_main.tw_edit_question.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(2, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(3, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(4, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(5, QHeaderView.Stretch)
        header.setSectionResizeMode(6, QHeaderView.Stretch)

        try:
            send(self.client, 4)    # Code um alle Fragen zu erhalten
            recv(self.client)   # Pseudo
            send(self.client, (self.login_widget_main.le_username.text(), self.edit_question_widget_1_main.cb_category.currentText()))    # Username und Kategorie
            
            questions = recv(self.client)

            for d in questions:
                row_pos = self.edit_question_widget_1_main.tw_edit_question.rowCount()
                self.edit_question_widget_1_main.tw_edit_question.insertRow(row_pos)
                self.edit_question_widget_1_main.tw_edit_question.setSelectionBehavior(QAbstractItemView.SelectRows)
                self.edit_question_widget_1_main.tw_edit_question.setEditTriggers(QAbstractItemView.NoEditTriggers)

                self.edit_question_widget_1_main.tw_edit_question.setItem(row_pos, 0, QTableWidgetItem(str(d[0])))
                self.edit_question_widget_1_main.tw_edit_question.setItem(row_pos, 1, QTableWidgetItem(str(d[1])))
                self.edit_question_widget_1_main.tw_edit_question.setItem(row_pos, 2, QTableWidgetItem(str(d[2])))
                self.edit_question_widget_1_main.tw_edit_question.setItem(row_pos, 3, QTableWidgetItem(str(d[3])))
                self.edit_question_widget_1_main.tw_edit_question.setItem(row_pos, 4, QTableWidgetItem(str(d[4])))
                self.edit_question_widget_1_main.tw_edit_question.setItem(row_pos, 5, QTableWidgetItem(str(datetime.datetime.fromtimestamp(d[5]).strftime('%d.%m.%Y %H:%M:%S'))))
                self.edit_question_widget_1_main.tw_edit_question.setItem(row_pos, 6, QTableWidgetItem(str(datetime.datetime.fromtimestamp(d[6]).strftime('%d.%m.%Y %H:%M:%S'))))
                                        
        except Exception as e:
            self.connected = False
            self.authenticated = False
            self.home_widget_main.lb_server_status.setText("Mit keinem Server verbunden")
            self.home_widget_main.lb_server_status.setStyleSheet("color: red")
            
            self.home_widget_main.lb_login_status.setText("Nicht angemeldet")
            self.home_widget_main.lb_login_status.setStyleSheet("color: red")

            self.finished_widget_main.lb_database_entry.setText("Datenbank-Eintrag konnte nicht erstellt werden, da die Verbindung zum Server unterbrochen ist.")
            self.finished_widget_main.lb_database_entry.setStyleSheet("color: red;")

            self.client.close()
            
            print(e)

    def _fill_complained_questions(self):
        try:
            index = self.complaining_questions_widget_main.cb_complained_questions.currentIndex()
            self.complaining_questions_widget_main.le_complainer.setText(self.complained_questions[index][4])
            self.complaining_questions_widget_main.le_date.setText(str(datetime.datetime.fromtimestamp(self.complained_questions[index][5]).strftime('%d.%m.%Y %H:%M:%S')))
            self.complaining_questions_widget_main.te_comment.setPlainText(self.complained_questions[index][2])
            self.complaining_questions_widget_main.te_correct_answer.setPlainText(self.complained_questions[index][7])
            self.complaining_questions_widget_main.te_suggested_answer.setPlainText(self.complained_questions[index][3])

            self.complaining_questions_widget_main.te_question.setPlainText(self.complained_questions[index][7])
            self.complaining_questions_widget_main.te_wrong1.setPlainText(self.complained_questions[index][8])
            self.complaining_questions_widget_main.te_wrong2.setPlainText(self.complained_questions[index][9])
            self.complaining_questions_widget_main.te_wrong3.setPlainText(self.complained_questions[index][10])
            self.complaining_questions_widget_main.te_correct.setPlainText(self.complained_questions[index][11])
            self.complaining_questions_widget_main.le_category.setText(self.complained_questions[index][12])

            self.complained_questions_current_primarykey = self.complained_questions[index][0]
        
        except Exception as e:
            print(e)

    def _save_complained_question(self, primarykey):
        if self.complaining_questions_widget_main.cb_complained_questions.currentIndex() > -1:
            check_entry = True

            if not self.complaining_questions_widget_main.te_correct.toPlainText().split():
                check_entry = False
                
            if not self.complaining_questions_widget_main.te_wrong1.toPlainText().split():
                check_entry = False

            if not self.complaining_questions_widget_main.te_wrong2.toPlainText().split():
                check_entry = False

            if not self.complaining_questions_widget_main.te_wrong3.toPlainText().split():
                check_entry = False
            
            if not check_entry:
                self.complaining_questions_widget_main.lb_status.setText("Die Felder dürfen nicht leer sein")
                self.complaining_questions_widget_main.lb_status.setStyleSheet("color: red;")
            else:
                try:
                    send(self.client, 7)    # Editierte Frage speichern
                    recv(self.client)   # Pseudo
                    
                    data = [self.complaining_questions_widget_main.te_question.toPlainText(),
                            self.complaining_questions_widget_main.te_wrong1.toPlainText(),
                            self.complaining_questions_widget_main.te_wrong2.toPlainText(),
                            self.complaining_questions_widget_main.te_wrong3.toPlainText(),
                            self.complaining_questions_widget_main.te_correct.toPlainText(),
                            self.complaining_questions_widget_main.le_category.text(),
                            self.login_widget_main.le_username.text(), primarykey]

                    send(self.client, data)

                    response = recv(self.client)

                    if response[0]:
                        self._delete_complain(primarykey)
                    
                    else:
                        self.complaining_questions_widget_main.lb_status.setText(f"Konnte nicht gespeichert werden. Fehler: {e}")
                        self.complaining_questions_widget_main.lb_status.setStyleSheet("color: red;")

                except Exception as e:
                        self.connected = False
                        self.authenticated = False
                        self.home_widget_main.lb_server_status.setText("Mit keinem Server verbunden")
                        self.home_widget_main.lb_server_status.setStyleSheet("color: red")
                        
                        self.home_widget_main.lb_login_status.setText("Nicht angemeldet")
                        self.home_widget_main.lb_login_status.setStyleSheet("color: red")
                        self.client.close()

                        print(e)

    def _delete_complain(self, primarykey):
        try:
            send(self.client, 17)   # Code um beanstandete Frage zu löschen
            recv(self.client)   # Pseudo
            send(self.client, (self.login_widget_main.le_username.text(), primarykey))   # Username und PK wird gesendet
            
            response = recv(self.client)

            if response[0]:
                self.show_complaining_questions()   # Somit wird refreshed
            
            else:
                self.complaining_questions_widget_main.lb_status.setText(f"Beanstandete Frage konnte nicht gelöscht werden. Fehler: {response[1]}")

        except Exception as e:
                    self.connected = False
                    self.authenticated = False
                    self.home_widget_main.lb_server_status.setText("Mit keinem Server verbunden")
                    self.home_widget_main.lb_server_status.setStyleSheet("color: red")
                    
                    self.home_widget_main.lb_login_status.setText("Nicht angemeldet")
                    self.home_widget_main.lb_login_status.setStyleSheet("color: red")
                    self.client.close()

                    print(e)

    def _refresh(self):
        self.home_widget_main.lb_status.clear()
        self.admin_panel_widget_main.lb_status.clear()

    def edit_user(self):
        try:
            send(self.client, 12)   # Code um Username zu checken
            recv(self.client)   # Pseudo
            send(self.client, self.admin_panel_widget_main.le_user.text())
            
            response = recv(self.client)

            if response is None:
                self.admin_panel_widget_main.lb_status.setText("User existiert nicht.")
                self.admin_panel_widget_main.lb_status.setStyleSheet("color: red;")
            
            else:
                self.show_edit_user()

            
        except Exception as e:
            self.connected = False
            self.authenticated = False
            self.home_widget_main.lb_server_status.setText("Mit keinem Server verbunden")
            self.home_widget_main.lb_server_status.setStyleSheet("color: red")
            
            self.home_widget_main.lb_login_status.setText("Nicht angemeldet")
            self.home_widget_main.lb_login_status.setStyleSheet("color: red")
            self.client.close()
            
            print(e)

    def save_edit_user(self):
        try:
            send(self.client, 14)   # Code um geänderte Daten zu speichern
            recv(self.client)   # Pseudo

            sha256 = hashlib.sha256()
            sha256.update(self.edit_user_widget_main.le_new_password.text().strip().encode())
            
            if self.edit_user_widget_main.cb_admin.currentText() == "Ja":
                admin = "True"
            else:
                admin = "False"

            data = (sha256.hexdigest(), self.edit_user_widget_main.le_fname.text(),
                    self.edit_user_widget_main.le_lname.text(), 
                    self.edit_user_widget_main.le_email.text(),
                    admin, self.edit_user_widget_main.le_username.text())

            send(self.client, data)
            
            response = recv(self.client)

            if response[0]:
                self.show_admin_panel()
                self.admin_panel_widget_main.lb_status.setText("Änderungen wurden durchgeführt.")
                self.admin_panel_widget_main.lb_status.setStyleSheet("color: green;")
            else:
                self.show_admin_panel()
                self.admin_panel_widget_main.lb_status.setText(f"User konnte nicht bearbeitet werden. Fehler {response[1]}")
                self.admin_panel_widget_main.lb_status.setStyleSheet("color: red;")

            
        except Exception as e:
            self.connected = False
            self.authenticated = False
            self.home_widget_main.lb_server_status.setText("Mit keinem Server verbunden")
            self.home_widget_main.lb_server_status.setStyleSheet("color: red")
            
            self.home_widget_main.lb_login_status.setText("Nicht angemeldet")
            self.home_widget_main.lb_login_status.setStyleSheet("color: red")
            self.client.close()
            
            print(e)

    def _update_profile(self):
        try:
            send(self.client, 18)   # Code um geänderte Daten zu speichern
            recv(self.client)   # Pseudo

            # hashed pw
            sha256 = hashlib.sha256()
            sha256.update(self.profile_widget_main.le_new_password.text().strip().encode())

            pic = b""
            picname = ""

            if self.profile_widget_main.path[0]:
                if os.path.exists(self.profile_widget_main.path[0]):
                    with open(self.profile_widget_main.path[0], "rb") as f:
                        pic = f.read()
                    
                    picname = os.path.basename(self.profile_widget_main.path[0])
            
            data = (sha256.hexdigest(), self.profile_widget_main.le_fname.text(),
                    self.profile_widget_main.le_lname.text(), 
                    self.profile_widget_main.le_email.text(),
                    pic, picname,
                    self.login_widget_main.le_username.text())

            send(self.client, data)
            
            response = recv(self.client)

            if response[0]:
                self.show_home()
                self.home_widget_main.lb_status.setText("Änderungen wurden durchgeführt.")
                self.home_widget_main.lb_status.setStyleSheet("color: green;")
            else:
                self.show_home()
                self.home_widget_main.lb_status.setText(f"Änderungen konnten nicht gespeichert werden. Fehler {response[1]}")
                self.home_widget_main.lb_status.setStyleSheet("color: red;")

            
        except Exception as e:
            self.connected = False
            self.authenticated = False
            self.home_widget_main.lb_server_status.setText("Mit keinem Server verbunden")
            self.home_widget_main.lb_server_status.setStyleSheet("color: red")
            
            self.home_widget_main.lb_login_status.setText("Nicht angemeldet")
            self.home_widget_main.lb_login_status.setStyleSheet("color: red")
            self.client.close()
            
            print(e)


    def init_layouts(self):
        self.home_layout()
        self.new_quiz_layout_1()
        self.new_quiz_layout_2()
        self.results_layout()
        self.highscore_layout()
        self.new_question_layout()
        self.edit_question_layout_1()
        self.edit_question_layout_2()
        self.login_layout()
        self.new_account_layout()
        self.admin_panel_layout()
        self.edit_user_layout()
        self.complaining_questions_layout()
        self.profile_layout()

        self.show()

    def home_layout(self):
        self.home_widget = QWidget(self)

        self.home_widget_main = HomeWidget(self.home_widget)

        self.home_widget_main.btn_start_quiz.clicked.connect(self.show_new_quiz_1)
        self.home_widget_main.btn_show_highscore.clicked.connect(self.show_highscore)
        self.home_widget_main.btn_new_question.clicked.connect(self.show_new_question)
        self.home_widget_main.btn_edit_delete_question.clicked.connect(self.show_edit_question_1)
        self.home_widget_main.btn_login.clicked.connect(self.show_login)
        self.home_widget_main.btn_admin_panel.clicked.connect(self.show_admin_panel)
        self.home_widget_main.btn_profile.clicked.connect(self.show_profile)

        self.home_widget.hide()

    def new_quiz_layout_1(self):
        self.new_quiz_widget_1 = QWidget(self)
        
        self.new_quiz_widget_1_main = NewQuizWidget1(self.new_quiz_widget_1)
        self.new_quiz_widget_1_main.btn_start.clicked.connect(self._start_new_quiz)
        self.new_quiz_widget_1_main.btn_cancel.clicked.connect(self.show_home)


        self.new_quiz_widget_1.hide()

    def new_quiz_layout_2(self):
        self.new_quiz_widget_2 = QWidget(self)

        self.new_quiz_widget_2_main = NewQuizWidget2(self.new_quiz_widget_2)

        self.new_quiz_widget_2_main.btn_answer_1.clicked.connect(lambda: self._next(self.new_quiz_widget_2_main.te_answer_1.toPlainText()))        
        self.new_quiz_widget_2_main.btn_answer_2.clicked.connect(lambda: self._next(self.new_quiz_widget_2_main.te_answer_2.toPlainText()))        
        self.new_quiz_widget_2_main.btn_answer_3.clicked.connect(lambda: self._next(self.new_quiz_widget_2_main.te_answer_3.toPlainText()))        
        self.new_quiz_widget_2_main.btn_answer_4.clicked.connect(lambda: self._next(self.new_quiz_widget_2_main.te_answer_4.toPlainText()))        

        self.new_quiz_widget_2.hide()

    def results_layout(self):
        self.tab_result_main = QTabWidget(self)

        self.finished_widget = QWidget()
        
        self.finished_widget_main = FinishedTab(self.finished_widget)
        self.finished_widget_main.btn_home.clicked.connect(self.show_home)

        self.tab_result_main.addTab(self.finished_widget, "Beendet")

        self.tab_result_main.hide()

    def highscore_layout(self):
        self.highscore_widget = QWidget(self)

        self.highscore = HighscoreWidget(self.highscore_widget)

        self.highscore.btn_refresh.clicked.connect(self.fill_highscore)
        self.highscore.btn_home.clicked.connect(self.show_home)

        self.highscore_widget.hide()

    def new_question_layout(self):
        self.new_question_widget = QWidget(self)
        
        self.new_question_widget_main = NewQuestionWidget(self.new_question_widget)

        self.new_question_widget_main.btn_save.clicked.connect(self.save_new_question)
        self.new_question_widget_main.btn_cancel.clicked.connect(self.show_home)


        self.new_question_widget.hide()

    def edit_question_layout_1(self):
        self.edit_question_widget_1 = QWidget(self)

        self.edit_question_widget_1_main = EditQuestionWidget1(self.edit_question_widget_1)
        self.edit_question_widget_1_main.btn_home.clicked.connect(self.show_home)
        self.edit_question_widget_1_main.tw_edit_question.itemDoubleClicked.connect(self.show_edit_question_2)
        self.edit_question_widget_1_main.cb_category.currentIndexChanged.connect(self._fill_edit_table)

        self.edit_question_widget_1.hide()

    def edit_question_layout_2(self):
        self.edit_question_widget_2 = QWidget(self)
                
        self.edit_question_widget_2_main = EditQuestionWidget2(self.edit_question_widget_2)
        self.edit_question_widget_2_main.btn_save.clicked.connect(self.save_edit_question)
        self.edit_question_widget_2_main.btn_delete.clicked.connect(self.delete_question)
        self.edit_question_widget_2_main.btn_cancel.clicked.connect(self.show_home)

        self.edit_question_widget_2.hide()

    def login_layout(self):
        self.login_widget = QWidget(self)

        self.login_widget_main = LoginWidget(self.login_widget)

        self.login_widget_main.btn_save.clicked.connect(self.save_execute_config)
        self.login_widget_main.btn_cancel.clicked.connect(self.show_home)
        self.login_widget_main.btn_new_account.clicked.connect(self.show_new_account)

        self.login_widget.hide()

    def new_account_layout(self):
        self.new_account_widget = QWidget(self)

        self.new_account_widget_main = CreateAccountWidget(self.new_account_widget)
        self.new_account_widget_main.btn_ok.clicked.connect(self.create_account)
        self.new_account_widget_main.btn_cancel.clicked.connect(self.show_home)
        self.new_account_widget_main.btn_back.clicked.connect(self.show_login)


        self.new_account_widget.hide()

    def admin_panel_layout(self):
        self.admin_panel_widget = QWidget(self)

        self.admin_panel_widget_main = AdminpanelWidget(self.admin_panel_widget)
        self.admin_panel_widget_main.btn_ok.clicked.connect(self.edit_user)
        self.admin_panel_widget_main.btn_home.clicked.connect(self.show_home)
        self.admin_panel_widget_main.btn_complaining_questions.clicked.connect(self.show_complaining_questions)

        self.new_account_widget.hide()
    
    def edit_user_layout(self):
        self.edit_user_widget = QWidget(self)

        self.edit_user_widget_main = EditUserWidget(self.edit_user_widget)
        self.edit_user_widget_main.btn_home.clicked.connect(self.show_home)
        self.edit_user_widget_main.btn_back.clicked.connect(self.show_admin_panel)
        self.edit_user_widget_main.btn_save.clicked.connect(self.save_edit_user)

        self.edit_user_widget.hide()

    def complaining_questions_layout(self):
        self.complaining_questions_widget = QWidget(self)

        self.complaining_questions_widget_main = ComplainingQuestionsWidget(self.complaining_questions_widget)
        self.complaining_questions_widget_main.btn_home.clicked.connect(self.show_home)
        self.complaining_questions_widget_main.btn_back.clicked.connect(self.show_admin_panel)
        self.complaining_questions_widget_main.cb_complained_questions.currentIndexChanged.connect(self._fill_complained_questions)
        
        self.complaining_questions_widget_main.btn_save.clicked.connect(lambda: self._save_complained_question(self.complained_questions_current_primarykey))
        self.complaining_questions_widget_main.btn_delete_complained_question.clicked.connect(lambda: self._delete_complain(self.complained_questions_current_primarykey))

        self.complaining_questions_widget.hide()

    def profile_layout(self):
        self.profile_widget = QWidget(self)
        
        self.profile_widget_main = ProfileWidget(self.profile_widget)
        self.profile_widget_main.btn_home.clicked.connect(self.show_home)
        self.profile_widget_main.btn_save.clicked.connect(self._update_profile)

        self.profile_widget.hide()    

    def show_home(self):
        self.home_widget.hide()
        self.new_quiz_widget_1.hide()
        self.new_quiz_widget_2.hide()
        self.tab_result_main.hide()
        self.highscore_widget.hide()
        self.new_question_widget.hide()
        self.edit_question_widget_1.hide()
        self.edit_question_widget_2.hide()
        self.login_widget.hide()
        self.new_account_widget.hide()
        self.admin_panel_widget.hide()
        self.edit_user_widget.hide()
        self.complaining_questions_widget.hide()
        self.profile_widget.hide()
        
        self.home_widget.show()

        if not self.admin:
            self.home_widget_main.btn_new_question.hide()
            self.home_widget_main.btn_edit_delete_question.hide()
            self.home_widget_main.btn_admin_panel.hide()

        else:
            self.home_widget_main.btn_new_question.show()
            self.home_widget_main.btn_edit_delete_question.show()
            self.home_widget_main.btn_admin_panel.show()

    def show_new_quiz_1(self):
        if self.connected:
            if self.authenticated:
                self.home_widget.hide()
                self.new_quiz_widget_1.hide()
                self.new_quiz_widget_2.hide()
                self.tab_result_main.hide()
                self.highscore_widget.hide()
                self.new_question_widget.hide()
                self.edit_question_widget_1.hide()
                self.edit_question_widget_2.hide()
                self.login_widget.hide()
                self.new_account_widget.hide()
                self.admin_panel_widget.hide()
                self.edit_user_widget.hide()
                self.complaining_questions_widget.hide()
                self.profile_widget.hide()
                
                self.new_quiz_widget_1.show()

    def show_new_quiz_2(self):
        if self.connected:
            if self.authenticated:
                self.home_widget.hide()
                self.new_quiz_widget_1.hide()
                self.new_quiz_widget_2.hide()
                self.tab_result_main.hide()
                self.highscore_widget.hide()
                self.new_question_widget.hide()
                self.edit_question_widget_1.hide()
                self.edit_question_widget_2.hide()
                self.login_widget.hide()
                self.new_account_widget.hide()                        
                self.admin_panel_widget.hide()
                self.edit_user_widget.hide()
                self.complaining_questions_widget.hide()
                self.profile_widget.hide()

                self.new_quiz_widget_2.show()

                self.current_index = 0
                current_question = self.questions[self.current_index]

                random.seed()
                random_order = list(current_question[2:6])
                random.shuffle(random_order)

                self.new_quiz_widget_2_main.lb_question_number.setText(f"Frage {self.current_index+1}")
                self.new_quiz_widget_2_main.te_question.insertPlainText(current_question[1])
                self.new_quiz_widget_2_main.te_answer_1.setText(random_order[0])
                self.new_quiz_widget_2_main.te_answer_2.setText(random_order[1])
                self.new_quiz_widget_2_main.te_answer_3.setText(random_order[2])
                self.new_quiz_widget_2_main.te_answer_4.setText(random_order[3])

    def show_results(self):
        self.home_widget.hide()
        self.new_quiz_widget_1.hide()
        self.new_quiz_widget_2.hide()
        self.tab_result_main.hide()
        self.highscore_widget.hide()
        self.new_question_widget.hide()
        self.edit_question_widget_1.hide()
        self.edit_question_widget_2.hide()
        self.login_widget.hide()
        self.new_account_widget.hide()
        self.admin_panel_widget.hide()
        self.edit_user_widget.hide()
        self.complaining_questions_widget.hide()
        self.profile_widget.hide()
        
        self.tab_result_main.show()

        end_time = round(time.time() - self.quiz_time_start, 2)

        self.finished_widget_main.lb_result.setText(f"Richtige Antworten: {self.correct_counter} von 15")
        self.finished_widget_main.lb_time.setText(f"Zeit: {end_time} Sekunden")

        # Falls es bereits Tabs gibt, werden sie vorerst gelöscht
        for i in range(15, 0, -1):
            self.tab_result_main.removeTab(i)
        
        # Tabs für jedes Frage wird erstellt
        for i in range(15):
            new_tab = ResultWidget(f"Frage {i+1}", self.questions[i], self.client, self.tab_result_main)
            new_tab.fill_layout(self.answers[i])

        # Daten an Server senden, die dann in die Datenbank geschrieben wird
        try:
            send(self.client, 8)    # Code zum speichern
            recv(self.client)   # Pseudo
            data = [self.correct_counter, end_time, self.login_widget_main.le_username.text()]

            send(self.client, data)

            reply = recv(self.client)

            if reply[0]:
                self.finished_widget_main.lb_database_entry.setText("Datenbank-Eintrag wurde erstellt.")
                self.finished_widget_main.lb_database_entry.setStyleSheet("color: green;")
            else:
                self.finished_widget_main.lb_database_entry.setText("Datenbank-Eintrag konnte nicht erstellt werden.")
                self.finished_widget_main.lb_database_entry.setStyleSheet("color: red;")
            

            if reply[1] == 0:
                self.finished_widget_main.lb_personal_place.setText(f"Persönlicher Platz: Konnte nicht ermittelt werden")
            else:
                self.finished_widget_main.lb_personal_place.setText(f"Persönlicher Platz: {str(reply[1])}")

            if reply[2] == 0:
                self.finished_widget_main.lb_global_place.setText(f"Globaler Platz: Konnte nicht ermittelt werden")
            else:
                self.finished_widget_main.lb_global_place.setText(f"Globaler Platz: {str(reply[2])}")

        except Exception as e:
            self.connected = False
            self.authenticated = False
            self.home_widget_main.lb_server_status.setText("Mit keinem Server verbunden")
            self.home_widget_main.lb_server_status.setStyleSheet("color: red")
            
            self.home_widget_main.lb_login_status.setText("Nicht angemeldet")
            self.home_widget_main.lb_login_status.setStyleSheet("color: red")

            self.finished_widget_main.lb_database_entry.setText("Datenbank-Eintrag konnte nicht erstellt werden, da die Verbindung zum Server unterbrochen ist.")
            self.finished_widget_main.lb_database_entry.setStyleSheet("color: red;")

            self.client.close()
            
            print(e)

    def show_highscore(self):
        if self.connected:
            if self.authenticated:
                self.home_widget.hide()
                self.new_quiz_widget_1.hide()
                self.new_quiz_widget_2.hide()
                self.tab_result_main.hide()
                self.highscore_widget.hide()
                self.new_question_widget.hide()
                self.edit_question_widget_1.hide()
                self.edit_question_widget_2.hide()
                self.login_widget.hide()
                self.new_account_widget.hide()
                self.admin_panel_widget.hide()
                self.edit_user_widget.hide()
                self.complaining_questions_widget.hide()
                self.profile_widget.hide()

                self.highscore_widget.show()
                
                self.fill_highscore()

    def show_new_question(self):
        if self.connected:
            if self.admin:
                self.home_widget.hide()
                self.new_quiz_widget_1.hide()
                self.new_quiz_widget_2.hide()
                self.tab_result_main.hide()
                self.highscore_widget.hide()
                self.new_question_widget.hide()
                self.edit_question_widget_1.hide()
                self.edit_question_widget_2.hide()
                self.login_widget.hide()                        
                self.new_account_widget.hide()
                self.admin_panel_widget.hide()
                self.edit_user_widget.hide()
                self.complaining_questions_widget.hide()
                self.profile_widget.hide()

                self.new_question_widget.show()

                self.new_question_widget_main.le_question.clear()
                self.new_question_widget_main.le_wrong_answer_1.clear()
                self.new_question_widget_main.le_wrong_answer_2.clear()
                self.new_question_widget_main.le_wrong_answer_3.clear()
                self.new_question_widget_main.le_correct_answer.clear()
                self.new_question_widget_main.le_category.clear()

            else:
                print("Fehlende Rechte")

    def show_edit_question_1(self):
        if self.connected:
            if self.admin:
                self.home_widget.hide()
                self.new_quiz_widget_1.hide()
                self.new_quiz_widget_2.hide()
                self.tab_result_main.hide()
                self.highscore_widget.hide()
                self.new_question_widget.hide()
                self.edit_question_widget_1.hide()
                self.edit_question_widget_2.hide()
                self.login_widget.hide()
                self.new_account_widget.hide()
                self.admin_panel_widget.hide()
                self.edit_user_widget.hide()
                self.complaining_questions_widget.hide()
                self.profile_widget.hide()

                self.edit_question_widget_1.show()

                # Alle Kategorien erhalten
                try:
                    send(self.client, 11)   # Code um alle Kategorien bekommen
                    recv(self.client)   # Pseudo
                    send(self.client, self.login_widget_main.le_username.text())    # Username senden
                    categories = recv(self.client)

                    self.edit_question_widget_1_main.cb_category.clear()

                    # Combobox füllen
                    for category in categories:
                        self.edit_question_widget_1_main.cb_category.addItem(category[0])
                    
                except Exception as e:
                    self.connected = False
                    self.authenticated = False
                    self.home_widget_main.lb_server_status.setText("Mit keinem Server verbunden")
                    self.home_widget_main.lb_server_status.setStyleSheet("color: red")
                    
                    self.home_widget_main.lb_login_status.setText("Nicht angemeldet")
                    self.home_widget_main.lb_login_status.setStyleSheet("color: red")
                    self.client.close()

                    print(e)

            else:
                print("Fehlende Rechte")
    
    def show_edit_question_2(self):
        if self.connected:
            if self.admin:
                self.home_widget.hide()
                self.new_quiz_widget_1.hide()
                self.new_quiz_widget_2.hide()
                self.tab_result_main.hide()
                self.highscore_widget.hide()
                self.new_question_widget.hide()
                self.edit_question_widget_1.hide()
                self.edit_question_widget_2.hide()
                self.login_widget.hide()
                self.new_account_widget.hide()
                self.admin_panel_widget.hide()
                self.edit_user_widget.hide()
                self.complaining_questions_widget.hide()
                self.profile_widget.hide()

                self.edit_question_widget_2.show()
                
                try:
                    send(self.client, 6)    # Code um genau eine Frage mit den wichtigesten Informationen zu erhalten
                    recv(self.client) # Pseudo
                    send(self.client, (self.edit_question_widget_1_main.tw_edit_question.item(self.edit_question_widget_1_main.tw_edit_question.currentRow(), 0).text(), self.login_widget_main.le_username.text()))
                                    
                    question = recv(self.client)

                    self.edit_question_widget_2_main.le_edit_question.setText(str(question[0]))
                    self.edit_question_widget_2_main.le_edit_wrong_answer_1.setText(str(question[1]))
                    self.edit_question_widget_2_main.le_edit_wrong_answer_2.setText(str(question[2]))
                    self.edit_question_widget_2_main.le_edit_wrong_answer_3.setText(str(question[3]))
                    self.edit_question_widget_2_main.le_edit_correct_answer.setText(str(question[4]))
                    self.edit_question_widget_2_main.le_edit_category.setText(str(question[5])) 
                
                except Exception as e:
                    self.connected = False
                    self.authenticated = False
                    self.home_widget_main.lb_server_status.setText("Mit keinem Server verbunden")
                    self.home_widget_main.lb_server_status.setStyleSheet("color: red")
                    
                    self.home_widget_main.lb_login_status.setText("Nicht angemeldet")
                    self.home_widget_main.lb_login_status.setStyleSheet("color: red")
                    self.client.close()

                    print(e)
            else:
                print("Fehlende Rechte")

    def show_login(self):
        self.home_widget.hide()
        self.new_quiz_widget_1.hide()
        self.new_quiz_widget_2.hide()
        self.tab_result_main.hide()
        self.highscore_widget.hide()
        self.new_question_widget.hide()
        self.edit_question_widget_1.hide()
        self.edit_question_widget_2.hide()
        self.login_widget.hide()
        self.new_account_widget.hide()
        self.admin_panel_widget.hide()
        self.edit_user_widget.hide()
        self.complaining_questions_widget.hide()
        self.profile_widget.hide()
        
        self.login_widget.show()

    def show_new_account(self):
            self.home_widget.hide()
            self.new_quiz_widget_1.hide()
            self.new_quiz_widget_2.hide()
            self.tab_result_main.hide()
            self.highscore_widget.hide()
            self.new_question_widget.hide()
            self.edit_question_widget_1.hide()
            self.edit_question_widget_2.hide()
            self.login_widget.hide()
            self.new_account_widget.hide()
            self.admin_panel_widget.hide()
            self.edit_user_widget.hide()
            self.complaining_questions_widget.hide()
            self.profile_widget.hide()
            
            self.new_account_widget.show()

            self.new_account_widget_main.le_fname.setStyleSheet("border: 1px solid black")
            self.new_account_widget_main.le_lname.setStyleSheet("border: 1px solid black")
            self.new_account_widget_main.le_email.setStyleSheet("border: 1px solid black")
            self.new_account_widget_main.le_username.setStyleSheet("border: 1px solid black")
            self.new_account_widget_main.lb_status.clear()
            self.new_account_widget_main.lb_status.setStyleSheet("color: black;")
            self.new_account_widget_main.lb_profile_picture.clear()

    def show_admin_panel(self):
        if self.connected:
            if self.authenticated:
                self.home_widget.hide()
                self.new_quiz_widget_1.hide()
                self.new_quiz_widget_2.hide()
                self.tab_result_main.hide()
                self.highscore_widget.hide()
                self.new_question_widget.hide()
                self.edit_question_widget_1.hide()
                self.edit_question_widget_2.hide()
                self.login_widget.hide()
                self.new_account_widget.hide()
                self.admin_panel_widget.hide()
                self.edit_user_widget.hide()
                self.complaining_questions_widget.hide()
                self.profile_widget.hide()
                
                self.admin_panel_widget.show()
                
                self.admin_panel_widget_main.le_user.clear()

    def show_edit_user(self):
        if self.connected:
            if self.authenticated:
                self.home_widget.hide()
                self.new_quiz_widget_1.hide()
                self.new_quiz_widget_2.hide()
                self.tab_result_main.hide()
                self.highscore_widget.hide()
                self.new_question_widget.hide()
                self.edit_question_widget_1.hide()
                self.edit_question_widget_2.hide()
                self.login_widget.hide()
                self.new_account_widget.hide()
                self.admin_panel_widget.hide()
                self.edit_user_widget.hide()
                self.complaining_questions_widget.hide()
                self.profile_widget.hide()
                
                self.edit_user_widget.show()

                self.edit_user_widget_main.le_username.clear()
                self.edit_user_widget_main.le_fname.clear()
                self.edit_user_widget_main.le_lname.clear()
                self.edit_user_widget_main.le_email.clear()
                
                try:
                    send(self.client, 13)   # Code um alle Infos des Users zu bekommen
                    recv(self.client)   # Pseudo
                    send(self.client, self.admin_panel_widget_main.le_user.text())  # User
                    data = recv(self.client)

                    self.edit_user_widget_main.le_username.setText(data[0])
                    self.edit_user_widget_main.le_fname.setText(data[2])
                    self.edit_user_widget_main.le_lname.setText(data[3])
                    self.edit_user_widget_main.le_email.setText(data[4])

                    
                    if eval(data[5]):
                        self.edit_user_widget_main.cb_admin.setCurrentText("Ja")
                    else:
                        self.edit_user_widget_main.cb_admin.setCurrentText("Nein")
                        


                except Exception as e:
                    self.connected = False
                    self.authenticated = False
                    self.home_widget_main.lb_server_status.setText("Mit keinem Server verbunden")
                    self.home_widget_main.lb_server_status.setStyleSheet("color: red")
                    
                    self.home_widget_main.lb_login_status.setText("Nicht angemeldet")
                    self.home_widget_main.lb_login_status.setStyleSheet("color: red")
                    self.client.close()
                    
                    print(e)

    def show_complaining_questions(self):
        if self.connected:
            if self.authenticated:
                self.home_widget.hide()
                self.new_quiz_widget_1.hide()
                self.new_quiz_widget_2.hide()
                self.tab_result_main.hide()
                self.highscore_widget.hide()
                self.new_question_widget.hide()
                self.edit_question_widget_1.hide()
                self.edit_question_widget_2.hide()
                self.login_widget.hide()
                self.new_account_widget.hide()
                self.admin_panel_widget.hide()
                self.edit_user_widget.hide()
                self.complaining_questions_widget.hide()
                self.profile_widget.hide()
                
                self.complaining_questions_widget.show()

                try:
                    send(self.client, 16)
                    recv(self.client)   # Pseudo
                    send(self.client, self.login_widget_main.le_username.text())    # Username wird gesendet
                    self.complained_questions = recv(self.client)

                    self.complaining_questions_widget_main.cb_complained_questions.clear()
                    self.complaining_questions_widget_main.le_complainer.clear()
                    self.complaining_questions_widget_main.le_date.clear()
                    self.complaining_questions_widget_main.te_comment.clear()
                    self.complaining_questions_widget_main.te_correct_answer.clear()
                    self.complaining_questions_widget_main.te_suggested_answer.clear()

                    self.complaining_questions_widget_main.lb_status.clear()
                    self.complaining_questions_widget_main.te_question.clear()
                    self.complaining_questions_widget_main.te_correct.clear()
                    self.complaining_questions_widget_main.te_wrong1.clear()
                    self.complaining_questions_widget_main.te_wrong2.clear()
                    self.complaining_questions_widget_main.te_wrong3.clear()
                    self.complaining_questions_widget_main.le_category.clear()

                    for i in self.complained_questions:
                        self.complaining_questions_widget_main.cb_complained_questions.addItem(i[7])



                except Exception as e:
                    self.connected = False
                    self.authenticated = False
                    self.home_widget_main.lb_server_status.setText("Mit keinem Server verbunden")
                    self.home_widget_main.lb_server_status.setStyleSheet("color: red")
                    
                    self.home_widget_main.lb_login_status.setText("Nicht angemeldet")
                    self.home_widget_main.lb_login_status.setStyleSheet("color: red")
                    self.client.close()
                    self.show_home()

                    print(e)
    
    def show_profile(self):
        if self.connected:
            if self.authenticated:
                self.home_widget.hide()
                self.new_quiz_widget_1.hide()
                self.new_quiz_widget_2.hide()
                self.tab_result_main.hide()
                self.highscore_widget.hide()
                self.new_question_widget.hide()
                self.edit_question_widget_1.hide()
                self.edit_question_widget_2.hide()
                self.login_widget.hide()
                self.new_account_widget.hide()
                self.admin_panel_widget.hide()
                self.edit_user_widget.hide()
                self.complaining_questions_widget.hide()
                self.profile_widget.hide()
                
                self.profile_widget.show()

                self.profile_widget_main.le_fname.clear()
                self.profile_widget_main.le_lname.clear()
                self.profile_widget_main.le_email.clear()
                self.profile_widget_main.lb_profile_picture.clear()


                try:
                    send(self.client, 13)   # Code um alle Infos des Users zu erhalten
                    recv(self.client)   # Pseudo
                    send(self.client, self.login_widget_main.le_username.text())    # Username senden

                    data = recv(self.client)

                    self.profile_widget_main.le_fname.setText(str(data[2]))
                    self.profile_widget_main.le_lname.setText(str(data[3]))
                    self.profile_widget_main.le_email.setText(str(data[4]))

                    if data[6]:
                        with open(f"Temp/{data[7]}", "wb") as f:
                            f.write(data[6])
                    
                        pix = QPixmap(f"Temp/{data[7]}")
                        pix = pix.scaledToWidth(150)
                        pix = pix.scaledToHeight(250)

                        self.profile_widget_main.lb_profile_picture.setPixmap(pix)

                
                except Exception as e:
                    self.connected = False
                    self.authenticated = False
                    self.home_widget_main.lb_server_status.setText("Mit keinem Server verbunden")
                    self.home_widget_main.lb_server_status.setStyleSheet("color: red")
                    
                    self.home_widget_main.lb_login_status.setText("Nicht angemeldet")
                    self.home_widget_main.lb_login_status.setStyleSheet("color: red")
                    self.client.close()
                    self.show_home()

    def resizeEvent(self, event):
        self.width = self.frameGeometry().width()
        self.height = self.frameGeometry().height()
        
        self.home_widget.resize(self.width, self.height-25)
        self.new_quiz_widget_1.resize(self.width, self.height-25)
        self.new_quiz_widget_2.resize(self.width, self.height-25)
        self.tab_result_main.resize(self.width, self.height-25)
        self.highscore_widget.resize(self.width, self.height-25)
        self.new_question_widget.resize(self.width, self.height-25)
        self.edit_question_widget_1.resize(self.width, self.height-25)
        self.edit_question_widget_2.resize(self.width, self.height-25)
        self.login_widget.resize(self.width, self.height-25)
        self.new_account_widget.resize(self.width, self.height-25)
        self.admin_panel_widget.resize(self.width, self.height-25)
        self.edit_user_widget.resize(self.width, self.height-25)
        self.complaining_questions_widget.resize(self.width, self.height-25)
        self.profile_widget.resize(self.width, self.height-25)

    def closeEvent(self, event):
        super().closeEvent(event)
        self.client.close()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    client = Client()
    sys.exit(app.exec_())
