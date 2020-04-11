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
        

        self.init_layouts()

        self.connected = False
        self.authenticated = False
        self.admin = False

        self.conn_tries = 0
        self.auth_tries = 0        

        if os.path.exists("Config/clientsettings.json"):
            with open("Config/clientsettings.json") as f:
                try:
                    self.settings = json.load(f)
                    
                    self.le_ip.setText(str(self.settings.get("serversettings").get("ip")))
                    self.le_port.setText(str(self.settings.get("serversettings").get("port")))
                    self.le_username.setText(str(self.settings.get("usersettings").get("username")))
                    self.le_password.setText(str(self.settings.get("usersettings").get("password")))
                    self.cb_autologin.setChecked(self.settings.get("generalsettings").get("autologin"))
                    self.cb_autoconnect.setChecked(self.settings.get("generalsettings").get("autoconnect"))
                    
                    if self.settings.get("generalsettings").get("autoconnect"):
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

    def connect_to_server(self):
        if not self.connected:
            if self.settings:
                
                if self.auth_tries >= 3:
                    pass

                else:
                    try:
                        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                        self.client.connect((self.settings.get("serversettings").get("ip"), self.settings.get("serversettings").get("port")))
                        self.client.settimeout(3)
                        
                        self.connected = True

                        self.home_widget_main.lb_server_status.setText(f"Verbunden mit Server '{self.settings.get('serversettings').get('ip')}:{self.settings.get('serversettings').get('port')}'")
                        self.home_widget_main.lb_server_status.setStyleSheet("color: green")
                        if self.settings.get("generalsettings").get("autologin"):
                            self.authentication()
                        else:
                            self.authenticated = False

                    except Exception as e:
                        self.auth_tries += 1
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
            self.auth_tries = 0
            self.conn_tries = 0
            self.connect_to_server()
            self.authentication()
             
    def authentication(self):
        if self.connected:
            if not self.authenticated:
                if self.settings:
                    
                    if self.auth_tries >= 3:
                        pass

                    else:
                        try:
                            self.client.send(pickle.dumps(5))
                            self.client.recv(2**16)

                            credentials = [self.settings.get("usersettings").get("username"), self.settings.get("usersettings").get("password")]
                            pickled = pickle.dumps(credentials)

                            try:
                                self.client.send(pickled)
                                response = pickle.loads(self.client.recv(2**16))
                                self.authenticated = response[0]
                                self.admin = response[1]
                                
                                if self.authenticated:
                                    self.home_widget_main.lb_login_status.setText(f"Angemeldet als '{self.settings.get('usersettings').get('username')}'")
                                    self.home_widget_main.lb_login_status.setStyleSheet("color: green")
                                else:
                                    self.home_widget_main.lb_login_status.setText("Nicht angemeldet")
                                    self.home_widget_main.lb_login_status.setStyleSheet("color: red")          

                            except Exception as e:
                                self.auth_tries += 1    
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
                            self.client.send(pickle.dumps(3))
                            self.client.recv(2**16)

                            data = (self.new_question_widget_main.le_question.text(), self.new_question_widget_main.le_wrong_answer_1.text(),
                                    self.new_question_widget_main.le_wrong_answer_2.text(), self.new_question_widget_main.le_wrong_answer_3.text(),
                                    self.new_question_widget_main.le_correct_answer.text(), self.new_question_widget_main.le_category.text(), 
                                    self.le_username.text())
                                               
                            self.client.send(pickle.dumps(data))

                            response = pickle.loads(self.client.recv(4096))
                            
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

    def save_edit_question(self):
        if self.connected:
            if self.authenticated:
                if self.admin:
                    # Check der Eingabedaten
                    check_entry = True

                    if not self.le_edit_question.text().split():
                        self.le_edit_question.setStyleSheet("border: 1px solid red")
                        check_entry = False
                    else:
                        self.le_edit_question.setStyleSheet("border: 1px solid black")
                    
                    if not self.le_edit_correct_answer.text().split():
                        self.le_edit_correct_answer.setStyleSheet("border: 1px solid red")
                        check_entry = False
                    else:
                        self.le_edit_correct_answer.setStyleSheet("border: 1px solid black")
                    
                    if not self.le_edit_wrong_answer_1.text().split():
                        self.le_edit_wrong_answer_1.setStyleSheet("border: 1px solid red")
                        check_entry = False
                    else:
                        self.le_edit_wrong_answer_1.setStyleSheet("border: 1px solid black")

                    if not self.le_edit_wrong_answer_2.text().split():
                        self.le_edit_wrong_answer_2.setStyleSheet("border: 1px solid red")
                        check_entry = False
                    else:
                        self.le_edit_wrong_answer_2.setStyleSheet("border: 1px solid black")

                    if not self.le_edit_wrong_answer_3.text().split():
                        self.le_edit_wrong_answer_3.setStyleSheet("border: 1px solid red")
                        check_entry = False
                    else:
                        self.le_edit_wrong_answer_3.setStyleSheet("border: 1px solid black")

                    if not self.le_edit_category.text().split():
                        self.le_edit_category.setStyleSheet("border: 1px solid red")
                        check_entry = False
                    else:
                        self.le_edit_category.setStyleSheet("border: 1px solid black")
                    
                    if check_entry:
                        try:
                            self.client.send(pickle.dumps(7))
                            self.client.recv(2**16)

                            data = (self.le_edit_question.text(), 
                                    self.le_edit_wrong_answer_1.text(),
                                    self.le_edit_wrong_answer_2.text(),
                                    self.le_edit_wrong_answer_3.text(),
                                    self.le_edit_correct_answer.text(),
                                    self.le_edit_category.text(),
                                    self.le_username.text(),
                                    self.edit_question_widget_1_main.tw_edit_question.item(self.edit_question_widget_1_main.tw_edit_question.currentRow(), 0).text())
                            
                            self.client.send(pickle.dumps(data))

                            response = pickle.loads(self.client.recv(4096))
                            
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

    def save_execute_config(self):
        if os.path.exists("Config/clientsettings.json"):
            try:
                temp_config = {"serversettings": {},
                               "usersettings": {},
                               "generalsettings": {}}
                
                temp_config["serversettings"]["ip"] = self.le_ip.text()
                temp_config["serversettings"]["port"] = int(self.le_port.text())
                temp_config["usersettings"]["username"] = self.le_username.text()
                temp_config["usersettings"]["password"] = self.le_password.text()
                temp_config["generalsettings"]["autologin"] = self.cb_autologin.isChecked()
                temp_config["generalsettings"]["autoconnect"] = self.cb_autoconnect.isChecked()
                
                with open("Config/clientsettings.json", "w") as f:
                    json.dump(temp_config, f, indent=4)
                    
                self.settings = temp_config
                    
                self.connect_to_server()
                
                self.show_home()
                    
            except Exception as e:
                self.settings = {}
                print(e)
        else:
            self.settings = {}
    
    def _start_new_quiz(self):
        try:
            # Initialisiere Quiz-Varibalen
            self.current_index = 0
            self.correct_counter = 0
            self.questions = []
            self.answers = {}
            self.quiz_time_start = time.time()

            self.client.send(pickle.dumps(1))
            self.client.recv(2**16)
            self.client.send(pickle.dumps(self.settings.get('usersettings').get('username')))

            # Erhalte eine Liste mit Tuples für jede Frage (insgesamt 15)
            # (quiz_id, question, wrong_answer_1, wrong_answer_2, wrong_answer_3, correct_answer,
            # category, author, editor, timestamp_creation, timestamp_lastchange)
            self.questions = pickle.loads(self.client.recv(2**16))
            self.show_new_quiz_2()

            
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
            self.client.send(pickle.dumps(2))
            data = pickle.loads(self.client.recv(2**16))

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

        self.show()

    def home_layout(self):
        self.home_widget = QWidget(self)

        self.home_widget_main = HomeWidget(self.home_widget)

        self.home_widget_main.btn_start_quiz.clicked.connect(self.show_new_quiz_1)
        self.home_widget_main.btn_show_highscore.clicked.connect(self.show_highscore)
        self.home_widget_main.btn_new_question.clicked.connect(self.show_new_question)
        self.home_widget_main.btn_edit_delete_question.clicked.connect(self.show_edit_question_1)
        self.home_widget_main.btn_login.clicked.connect(self.show_login)

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

        self.tab_finished_main = QWidget()
        
        self.tab_finished = FinishedTab(self.tab_finished_main)
        self.tab_finished.btn_home.clicked.connect(self.show_home)

        self.tab_result_main.addTab(self.tab_finished_main, "Beendet")

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

        self.edit_question_widget_1_main = EditQuestionLayout(self.edit_question_widget_1)
        self.edit_question_widget_1_main.btn_home.clicked.connect(self.show_home)
        self.edit_question_widget_1_main.tw_edit_question.itemDoubleClicked.connect(self.show_edit_question_2)

        self.edit_question_widget_1.hide()

    def edit_question_layout_2(self):
        self.edit_question_widget_2 = QWidget(self)
                
        vbox = QVBoxLayout()

        hbox = QHBoxLayout()

        lb_question_ = QLabel("Frage bearbeiten/löschen")
        lb_question_.setFont(QFont("Times New Roman", 40, QFont.Bold))
        lb_question_.setAlignment(Qt.AlignCenter)

        hbox.addWidget(lb_question_)


        hbox0 = QHBoxLayout()
        lb_question = QLabel("Frage")
        lb_question.setFont(QFont("Times New Roman", 15, QFont.Cursive))

        self.le_edit_question = QLineEdit()
        self.le_edit_question.setFont(QFont("Times New Roman", 15, QFont.Cursive))        
        self.le_edit_question.setStyleSheet("border: 1px solid black")

        hbox0.addWidget(lb_question)
        hbox0.addWidget(self.le_edit_question)

        hbox_space = QHBoxLayout()
        hbox_space.addWidget(QLabel())


        hbox1 = QHBoxLayout()
        lb_correct_answer = QLabel("Richtige Antwort  ")
        lb_correct_answer.setFont(QFont("Times New Roman", 12, QFont.Cursive))
        self.le_edit_correct_answer = QLineEdit()
        self.le_edit_correct_answer.setFont(QFont("Times New Roman", 12, QFont.Cursive))        
        self.le_edit_correct_answer.setStyleSheet("border: 1px solid black")

        lb_wrong_answer_1 = QLabel("Falsche Antwort 1")
        lb_wrong_answer_1.setFont(QFont("Times New Roman", 12, QFont.Cursive))
        self.le_edit_wrong_answer_1 = QLineEdit()
        self.le_edit_wrong_answer_1.setFont(QFont("Times New Roman", 12, QFont.Cursive))
        self.le_edit_wrong_answer_1.setStyleSheet("border: 1px solid black")
        
        
        hbox1.addWidget(lb_correct_answer)
        hbox1.addWidget(self.le_edit_correct_answer)
        hbox1.addStretch()
        hbox1.addWidget(lb_wrong_answer_1)
        hbox1.addWidget(self.le_edit_wrong_answer_1)


        hbox2 = QHBoxLayout()
        
        lb_wrong_answer_2 = QLabel("Falsche Antwort 2")
        lb_wrong_answer_2.setFont(QFont("Times New Roman", 12, QFont.Cursive))
        self.le_edit_wrong_answer_2 = QLineEdit()
        self.le_edit_wrong_answer_2.setFont(QFont("Times New Roman", 12, QFont.Cursive))
        self.le_edit_wrong_answer_2.setStyleSheet("border: 1px solid black")

        lb_wrong_answer_3 = QLabel("Falsche Antwort 3")
        lb_wrong_answer_3.setFont(QFont("Times New Roman", 12, QFont.Cursive))
        self.le_edit_wrong_answer_3 = QLineEdit()
        self.le_edit_wrong_answer_3.setFont(QFont("Times New Roman", 12, QFont.Cursive))
        self.le_edit_wrong_answer_3.setStyleSheet("border: 1px solid black")

        hbox2.addWidget(lb_wrong_answer_2)
        hbox2.addWidget(self.le_edit_wrong_answer_2)  
        hbox2.addStretch()      
        hbox2.addWidget(lb_wrong_answer_3)
        hbox2.addWidget(self.le_edit_wrong_answer_3)


        hbox3 = QHBoxLayout()

        lb_category = QLabel("Kategorie")
        lb_category.setFont(QFont("Times New Roman", 12, QFont.Cursive))
        self.le_edit_category = QLineEdit()
        self.le_edit_category.setFont(QFont("Times New Roman", 12, QFont.Cursive))
        self.le_edit_category.setStyleSheet("border: 1px solid black")

        hbox3.addWidget(lb_category)
        hbox3.addWidget(self.le_edit_category)


        hbox4 = QHBoxLayout()

        btn_save = QPushButton("Speichern")
        btn_save.setFont(QFont("Times New Roman", 12, QFont.Cursive))
        btn_save.clicked.connect(self.save_edit_question)

        btn_cancel = QPushButton("Abbrechen")
        btn_cancel.clicked.connect(self.show_home)
        btn_cancel.setFont(QFont("Times New Roman", 12, QFont.Cursive))
    	
        hbox4.addStretch()
        hbox4.addWidget(btn_save)
        hbox4.addWidget(btn_cancel)

        vbox.addLayout(hbox)
        vbox.addLayout(hbox0)
        vbox.addLayout(hbox_space)
        vbox.addLayout(hbox1)
        vbox.addLayout(hbox2)
        vbox.addLayout(hbox3)
        vbox.addStretch()
        vbox.addLayout(hbox4)
        
        self.edit_question_widget_2.setLayout(vbox)

        self.edit_question_widget_2.hide()

    def login_layout(self):
        self.login_widget = QWidget(self)

        vbox = QVBoxLayout()
        

        hbox0 = QHBoxLayout()

        lb_login = QLabel("Login")
        lb_login.setFont(QFont("Times New Roman", 40, QFont.Bold))
        lb_login.setAlignment(Qt.AlignCenter)
        hbox0.addWidget(lb_login)

        hbox_space0 = QHBoxLayout()
        hbox_space0.addWidget(QLabel())


        hbox1 = QHBoxLayout()
        
        lb_server = QLabel("Server IP")
        lb_server.setFont(QFont("Times New Roman", 15, QFont.Cursive))
        self.le_ip = QLineEdit()

        hbox1.addWidget(lb_server)
        hbox1.addWidget(self.le_ip)
        hbox1.addStretch()
        

        hbox2 = QHBoxLayout()

        lb_port = QLabel("Port")
        lb_port.setFont(QFont("Times New Roman", 15, QFont.Cursive))
        self.le_port = QLineEdit()

        hbox2.addWidget(lb_port)
        hbox2.addWidget(self.le_port)
        hbox2.addStretch(1)


        hbox_space1 = QHBoxLayout()
        hbox_space1.addWidget(QLabel())


        hbox3 = QHBoxLayout()

        lb_username = QLabel("Benutzername")
        lb_username.setFont(QFont("Times New Roman", 15, QFont.Cursive))
        self.le_username = QLineEdit()

        hbox3.addWidget(lb_username)
        hbox3.addWidget(self.le_username)
        hbox3.addStretch()


        hbox4 = QHBoxLayout()

        lb_password = QLabel("Passwort")
        lb_password.setFont(QFont("Times New Roman", 15, QFont.Cursive))
        self.le_password = QLineEdit()
        self.le_password.setEchoMode(QLineEdit.Password)

        hbox4.addWidget(lb_password)
        hbox4.addWidget(self.le_password)
        hbox4.addStretch()


        hbox5 = QHBoxLayout()

        self.cb_autologin = QCheckBox("Automatischer Login")
        self.cb_autoconnect = QCheckBox("Automatisch Verbindung zum Server aufbauen")
        
        hbox5.addWidget(self.cb_autologin)
        hbox5.addWidget(self.cb_autoconnect)
        hbox5.addStretch()


        hbox6 = QHBoxLayout()
        
        btn_save = QPushButton("Speichern und Ausführen")
        btn_save.clicked.connect(self.save_execute_config)
        btn_cancel = QPushButton("Abbrechen")
        btn_cancel.clicked.connect(self.show_home)
        hbox6.addStretch()
        hbox6.addWidget(btn_save)
        hbox6.addWidget(btn_cancel)


        vbox.addLayout(hbox0)
        vbox.addLayout(hbox_space0)
        vbox.addLayout(hbox1)
        vbox.addLayout(hbox2)
        vbox.addLayout(hbox_space1)
        vbox.addLayout(hbox3)
        vbox.addLayout(hbox4)
        vbox.addLayout(hbox5)

        vbox.addStretch()

        vbox.addLayout(hbox6)

        self.login_widget.setLayout(vbox)

        self.login_widget.hide()
    
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
        
        self.home_widget.show()

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
        
        self.tab_result_main.show()

        end_time = round(time.time() - self.quiz_time_start, 2)

        self.tab_finished.lb_result.setText(f"Richtige Antworten: {self.correct_counter} von 15")
        self.tab_finished.lb_time.setText(f"Zeit: {end_time} Sekunden")

        # Falls es bereits Tabs gibt, werden sie vorerst gelöscht
        for i in range(15, 0, -1):
            self.tab_result_main.removeTab(i)
        
        # Tabs für jedes Frage wird erstellt
        for i in range(15):
            new_tab = ResultWidget(f"Frage {i+1}", self.tab_result_main)
            new_tab.fill_layout(self.questions[i], self.answers[i])
        

        # Daten an Server senden, die dann in die Datenbank geschrieben wird
        try:
            data = [self.correct_counter, end_time, self.le_username.text()]
            self.client.send(pickle.dumps(data))

            reply = pickle.loads(self.client.recv(2**16))

            if reply[0]:
                self.tab_finished.lb_database_entry.setText("Datenbank-Eintrag wurde erstellt.")
                self.tab_finished.lb_database_entry.setStyleSheet("color: green;")
            else:
                self.tab_finished.lb_database_entry.setText("Datenbank-Eintrag konnte nicht erstellt werden.")
                self.tab_finished.lb_database_entry.setStyleSheet("color: red;")
            

            if reply[1] == 0:
                self.tab_finished.lb_personal_place.setText(f"Persönlicher Platz: Konnte nicht ermittelt werden")
            else:
                self.tab_finished.lb_personal_place.setText(f"Persönlicher Platz: {str(reply[1])}")

            if reply[2] == 0:
                self.tab_finished.lb_global_place.setText(f"Globaler Platz: Konnte nicht ermittelt werden")
            else:
                self.tab_finished.lb_global_place.setText(f"Globaler Platz: {str(reply[2])}")

        except Exception as e:
            self.connected = False
            self.authenticated = False
            self.home_widget_main.lb_server_status.setText("Mit keinem Server verbunden")
            self.home_widget_main.lb_server_status.setStyleSheet("color: red")
            
            self.home_widget_main.lb_login_status.setText("Nicht angemeldet")
            self.home_widget_main.lb_login_status.setStyleSheet("color: red")

            self.lb_database_entry.setText("Datenbank-Eintrag konnte nicht erstellt werden, da die Verbindung zum Server unterbrochen ist.")
            self.lb_database_entry.setStyleSheet("color: red;")

            self.client.close()
            
            print(e)

    def show_highscore(self):
        if self.connected:
            self.home_widget.hide()
            self.new_quiz_widget_1.hide()
            self.new_quiz_widget_2.hide()
            self.tab_result_main.hide()
            self.highscore_widget.hide()
            self.new_question_widget.hide()
            self.edit_question_widget_1.hide()
            self.edit_question_widget_2.hide()
            self.login_widget.hide()

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

                self.new_question_widget.show()
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

                self.edit_question_widget_1.show()

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
                    self.client.send(pickle.dumps(4))
                    self.client.recv(2**16)  # Pseudo
                    self.client.send(pickle.dumps(self.le_username.text()))
                    
                    all_questions = pickle.loads(self.client.recv(2**30))

                    for d in all_questions:
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

                    self.lb_database_entry.setText("Datenbank-Eintrag konnte nicht erstellt werden, da die Verbindung zum Server unterbrochen ist.")
                    self.lb_database_entry.setStyleSheet("color: red;")

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

                self.edit_question_widget_2.show()
                
                self.client.send(pickle.dumps(6))
                self.client.recv(2**16) # Pseudo
                self.client.send(pickle.dumps((self.edit_question_widget_1_main.tw_edit_question.item(self.edit_question_widget_1_main.tw_edit_question.currentRow(), 0).text(), self.le_username.text())))
                
                question = pickle.loads(self.client.recv(2**16))

                self.le_edit_question.setText(str(question[0]))
                self.le_edit_wrong_answer_1.setText(str(question[1]))
                self.le_edit_wrong_answer_2.setText(str(question[2]))
                self.le_edit_wrong_answer_3.setText(str(question[3]))
                self.le_edit_correct_answer.setText(str(question[4]))
                self.le_edit_category.setText(str(question[5])) 
            
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
        
        self.login_widget.show()

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


if __name__ == "__main__":
    app = QApplication(sys.argv)
    client = Client()
    sys.exit(app.exec_())
