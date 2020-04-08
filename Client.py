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

from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *


class Client(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.setMinimumSize(600, 400)
        self.setWindowTitle("Quiz")
        self.width = self.frameGeometry().width()
        self.height = self.frameGeometry().height()
        self.init_layouts()

        self.connected = False
        self.authenticated = False
        self.admin = False

        self.conn_tries = 0
        self.auth_tries = 0        

        if os.path.exists("Config/clientsettings.json"):
            with open("Config/clientsettings.json", "r+") as f:
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

        self.timer_connect = QTimer()
        self.timer_connect.timeout.connect(self._update)
        self.timer_connect.start(5000)
            
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

                        self.lb_server_status.setText(f"Verbunden mit Server '{self.settings.get('serversettings').get('ip')}:{self.settings.get('serversettings').get('port')}'")
                        self.lb_server_status.setStyleSheet("color: green")
                        if self.settings.get("generalsettings").get("autologin"):
                            self.authentication()
                        else:
                            self.authenticated = False

                    except Exception as e:
                        self.auth_tries += 1
                        self.connected = False
                        self.authenticated = False
                        self.lb_server_status.setText("Mit keinem Server verbunden")
                        self.lb_server_status.setStyleSheet("color: red")
                        
                        self.lb_login_status.setText("Nicht angemeldet")
                        self.lb_login_status.setStyleSheet("color: red")
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
                            self.client.recv(1024)

                            credentials = [self.settings.get("usersettings").get("username"), self.settings.get("usersettings").get("password")]
                            pickled = pickle.dumps(credentials)

                            try:
                                self.client.send(pickled)
                                response = pickle.loads(self.client.recv(1024))
                                self.authenticated = response[0]
                                self.admin = response[1]
                                
                                if self.authenticated:
                                    self.lb_login_status.setText(f"Angemeldet als '{self.settings.get('usersettings').get('username')}'")
                                    self.lb_login_status.setStyleSheet("color: green")
                                else:
                                    self.lb_login_status.setText("Nicht angemeldet")
                                    self.lb_login_status.setStyleSheet("color: red")          

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

                    if not self.le_question.text().split():
                        self.le_question.setStyleSheet("border: 1px solid red")
                        check_entry = False
                    else:
                        self.le_question.setStyleSheet("border: 1px solid black")
                    
                    if not self.le_correct_answer.text().split():
                        self.le_correct_answer.setStyleSheet("border: 1px solid red")
                        check_entry = False
                    else:
                        self.le_correct_answer.setStyleSheet("border: 1px solid black")
                    
                    if not self.le_wrong_answer_1.text().split():
                        self.le_wrong_answer_1.setStyleSheet("border: 1px solid red")
                        check_entry = False
                    else:
                        self.le_wrong_answer_1.setStyleSheet("border: 1px solid black")

                    if not self.le_wrong_answer_2.text().split():
                        self.le_wrong_answer_2.setStyleSheet("border: 1px solid red")
                        check_entry = False
                    else:
                        self.le_wrong_answer_2.setStyleSheet("border: 1px solid black")

                    if not self.le_wrong_answer_3.text().split():
                        self.le_wrong_answer_3.setStyleSheet("border: 1px solid red")
                        check_entry = False
                    else:
                        self.le_wrong_answer_3.setStyleSheet("border: 1px solid black")

                    if not self.le_category.text().split():
                        self.le_category.setStyleSheet("border: 1px solid red")
                        check_entry = False
                    else:
                        self.le_category.setStyleSheet("border: 1px solid black")
                    
                    if check_entry:
                        try:
                            self.client.send(pickle.dumps(3))
                            self.client.recv(1024)

                            data = (self.le_question.text(), self.le_wrong_answer_1.text(),
                                    self.le_wrong_answer_2.text(), self.le_wrong_answer_3.text(),
                                    self.le_correct_answer.text(), self.le_category.text(), 
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
                            self.lb_server_status.setText("Mit keinem Server verbunden")
                            self.lb_server_status.setStyleSheet("color: red")
                            
                            self.lb_login_status.setText("Nicht angemeldet")
                            self.lb_login_status.setStyleSheet("color: red")
                            self.client.close()
                            print(e)
                        
                        finally:                                
                            self.le_question.clear()
                            self.le_correct_answer.clear()
                            self.le_wrong_answer_1.clear()
                            self.le_wrong_answer_2.clear()
                            self.le_wrong_answer_3.clear()
                            self.le_category.clear()
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
            self.client.recv(1024)
            self.client.send(pickle.dumps(self.settings.get('usersettings').get('username')))

            # Erhalte eine Liste mit Tuples für jede Frage (insgesamt 15)
            # (quiz_id, question, wrong_answer_1, wrong_answer_2, wrong_answer_3, correct_answer,
            # category, author, editor, timestamp_creation, timestamp_lastchange)
            self.questions = pickle.loads(self.client.recv(2**16))
            self.show_new_quiz_2()

            
        except Exception as e:
            self.connected = False
            self.authenticated = False
            self.lb_server_status.setText("Mit keinem Server verbunden")
            self.lb_server_status.setStyleSheet("color: red")
            
            self.lb_login_status.setText("Nicht angemeldet")
            self.lb_login_status.setStyleSheet("color: red")
            self.client.close()
            
            print(e)

    def _next(self, answer):
        
        self.answers[self.current_index] = answer
        if answer == self.questions[self.current_index][5]:
            self.correct_counter += 1

        self.current_index += 1

        if self.current_index < 15:            
            current_question = self.questions[self.current_index]
            random.seed()
            random_order = list(current_question[2:6])
            random.shuffle(random_order)

            self.lb_question_number.setText(f"Frage {self.current_index+1}")
            self.te_question.insertPlainText(current_question[1])
            self.te_answer_1.setText(random_order[0])
            self.te_answer_2.setText(random_order[1])
            self.te_answer_3.setText(random_order[2])
            self.te_answer_4.setText(random_order[3])
        
        elif self.current_index == 15:
            self.show_results()

    def _update(self):
        try:
            if self.settings:
                for k, v in self.settings.items():
                    pass

        except Exception as e:
            print(e)

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
            self.lb_server_status.setText("Mit keinem Server verbunden")
            self.lb_server_status.setStyleSheet("color: red")
            
            self.lb_login_status.setText("Nicht angemeldet")
            self.lb_login_status.setStyleSheet("color: red")
            self.client.close()
            
            print(e)

    def init_layouts(self):
        self.home_layout()
        self.new_quiz_layout_1()
        self.new_quiz_layout_2()
        self.results_layout()
        self.highscore_layout()
        self.new_question_layout()
        self.edit_question_layout()
        self.login_layout()

        self.show()

    def home_layout(self):
        self.home_widget = QWidget(self)
        self.home_widget.resize(self.width, self.height-25)
        vbox = QVBoxLayout()

        hbox0 = QHBoxLayout()
        lb_title = QLabel("Quiz")
        lb_title.setFont(QFont("Times New Roman", 40, QFont.Bold))
        lb_title.setAlignment(Qt.AlignCenter)
        hbox0.addWidget(lb_title)

        hbox_space = QHBoxLayout()
        hbox_space.addWidget(QLabel())

        hbox1 = QHBoxLayout()
        btn_start_quiz = QPushButton("Neues Quiz")
        btn_start_quiz.setFont(QFont("Times New Roman", 25, QFont.Cursive))
        btn_start_quiz.clicked.connect(self.show_new_quiz_1)
        hbox1.addWidget(btn_start_quiz)
        hbox1.addStretch()

        hbox2 = QHBoxLayout()
        btn_show_highscore = QPushButton("Highscoreliste")
        btn_show_highscore.setFont(QFont("Times New Roman", 25, QFont.Cursive))
        btn_show_highscore.clicked.connect(self.show_highscore)
        hbox2.addWidget(btn_show_highscore)
        hbox2.addStretch()

        hbox3 = QHBoxLayout()
        btn_new_question = QPushButton("Neue Frage erstellen")
        btn_new_question.setFont(QFont("Times New Roman", 25, QFont.Cursive))
        btn_new_question.clicked.connect(self.show_new_question)
        hbox3.addWidget(btn_new_question)
        hbox3.addStretch()

        hbox4 = QHBoxLayout()
        btn_edit_delete_question = QPushButton("Frage bearbeiten/löschen")
        btn_edit_delete_question.setFont(QFont("Times New Roman", 25, QFont.Cursive))
        btn_edit_delete_question.clicked.connect(self.show_edit_question)
        hbox4.addWidget(btn_edit_delete_question)
        hbox4.addStretch()

        hbox5 = QHBoxLayout()
        btn_login = QPushButton("Login")
        btn_login.setFont(QFont("Times New Roman", 25, QFont.Cursive))
        btn_login.clicked.connect(self.show_login)
        hbox5.addWidget(btn_login)
        hbox5.addStretch()

        hbox6 = QHBoxLayout()
        self.lb_server_status = QLabel("Zurzeit mit keinem Server verbunden")
        self.lb_server_status.setFont(QFont("Times New Roman", 12, QFont.Bold))
        self.lb_server_status.setStyleSheet("color: red")
        hbox6.addStretch()
        hbox6.addWidget(self.lb_server_status)

        hbox7 = QHBoxLayout()
        self.lb_login_status = QLabel("Nicht angemeldet")
        self.lb_login_status.setFont(QFont("Times New Roman", 12, QFont.Bold))
        self.lb_login_status.setStyleSheet("color: red")
        hbox7.addStretch()
        hbox7.addWidget(self.lb_login_status)

        vbox.addLayout(hbox0)
        vbox.addLayout(hbox_space)
        vbox.addLayout(hbox1)
        vbox.addLayout(hbox2)
        vbox.addLayout(hbox3)
        vbox.addLayout(hbox4)
        vbox.addLayout(hbox5)
        vbox.addStretch()
        vbox.addLayout(hbox6)
        vbox.addLayout(hbox7)        

        self.home_widget.setLayout(vbox)

    def new_quiz_layout_1(self):
        self.new_quiz_widget_1 = QWidget(self)
        
        vbox = QVBoxLayout()        
        
        hbox0 = QHBoxLayout()
        
        lb_new_quiz = QLabel("Neues Quiz")
        lb_new_quiz.setFont(QFont("Times New Roman", 40, QFont.Bold))
        lb_new_quiz.setAlignment(Qt.AlignCenter)
        
        hbox0.addWidget(lb_new_quiz)
        
        
        hbox_space0 = QHBoxLayout()
        hbox_space0.addWidget(QLabel())
        
        hbox_space1 = QHBoxLayout()
        hbox_space1.addWidget(QLabel())

        hbox_space2 = QHBoxLayout()
        hbox_space2.addWidget(QLabel())
        
        
        hbox1 = QHBoxLayout()

        btn_start = QPushButton("Start")
        btn_start.setFont(QFont("Times New Roman", 30, QFont.Bold))
        btn_start.clicked.connect(self._start_new_quiz)

        hbox1.addWidget(btn_start, alignment=Qt.AlignCenter)


        hbox2 = QHBoxLayout()
        btn_cancel = QPushButton("Abbrechen")
        btn_cancel.clicked.connect(self.show_home)        
        
        hbox2.addStretch()
        hbox2.addWidget(btn_cancel)
        
        
        vbox.addLayout(hbox0)
        vbox.addLayout(hbox_space0)
        vbox.addLayout(hbox_space1)
        vbox.addLayout(hbox_space2)
        vbox.addLayout(hbox1)
        vbox.addStretch()
        vbox.addLayout(hbox2)
        
        self.new_quiz_widget_1.setLayout(vbox)

        self.new_quiz_widget_1.hide()
    
    def new_quiz_layout_2(self):
        self.new_quiz_widget_2 = QWidget(self)

        vbox = QVBoxLayout()

        hbox0 = QHBoxLayout()

        self.lb_question_number = QLabel()
        self.lb_question_number.setFont(QFont("Times New Roman", 30, QFont.Bold))
        self.lb_question_number.setAlignment(Qt.AlignCenter)

        hbox0.addWidget(self.lb_question_number)

        hbox_space = QHBoxLayout()
        hbox_space.addWidget(QLabel())

        hbox1 = QHBoxLayout()

        self.te_question = QTextEdit()
        self.te_question.setFont(QFont("Times New Roman", 18, QFont.Bold))
        self.te_question.setReadOnly(True)

        hbox1.addWidget(self.te_question)


        hbox2 = QHBoxLayout()

        self.te_answer_1 = QTextEdit()
        self.te_answer_1.setDisabled(True)

        self.te_answer_2 = QTextEdit()
        self.te_answer_2.setDisabled(True)

        hbox2.addWidget(self.te_answer_1)
        hbox2.addWidget(self.te_answer_2)


        hbox3 = QHBoxLayout()

        self.btn_answer_1 = QPushButton("A")
        self.btn_answer_1.setFont(QFont("Times New Roman", 15, QFont.Cursive))
        self.btn_answer_1.clicked.connect(lambda: self._next(self.te_answer_1.toPlainText()))

        self.btn_answer_2 = QPushButton("B")
        self.btn_answer_2.setFont(QFont("Times New Roman", 15, QFont.Cursive))
        self.btn_answer_2.clicked.connect(lambda: self._next(self.te_answer_2.toPlainText()))
        
        hbox3.addWidget(self.btn_answer_1)
        hbox3.addWidget(self.btn_answer_2)


        hbox4 = QHBoxLayout()

        self.te_answer_3 = QTextEdit()
        self.te_answer_3.setDisabled(True)
        
        # self.btn_answer_3.clicked.connect(lambda: self._next(self.btn_answer_4.text()))
        
        self.te_answer_4 = QTextEdit()
        self.te_answer_4.setDisabled(True)
        
        # self.btn_answer_4.clicked.connect(lambda: self._next(self.btn_answer_4.text()))

        hbox4.addWidget(self.te_answer_3)
        hbox4.addWidget(self.te_answer_4)


        hbox5 = QHBoxLayout()

        self.btn_answer_3 = QPushButton("C")
        self.btn_answer_3.setFont(QFont("Times New Roman", 15, QFont.Cursive))
        self.btn_answer_3.clicked.connect(lambda: self._next(self.te_answer_3.toPlainText()))

        self.btn_answer_4 = QPushButton("D")
        self.btn_answer_4.setFont(QFont("Times New Roman", 15, QFont.Cursive))
        self.btn_answer_4.clicked.connect(lambda: self._next(self.te_answer_4.toPlainText()))

        hbox5.addWidget(self.btn_answer_3)
        hbox5.addWidget(self.btn_answer_4)


        hbox6 = QHBoxLayout()

        self.lb_time = QLabel()

        btn_cancel = QPushButton("Beende")
        btn_cancel.clicked.connect(self.show_home)

        hbox6.addWidget(self.lb_time)
        hbox6.addStretch()
        hbox6.addWidget(btn_cancel)

        vbox.addLayout(hbox0)
        vbox.addLayout(hbox_space)
        vbox.addLayout(hbox1)
        vbox.addLayout(hbox2)
        vbox.addLayout(hbox3)
        vbox.addStretch()
        vbox.addLayout(hbox4)
        vbox.addLayout(hbox5)
        vbox.addStretch()
        vbox.addLayout(hbox6)        

        self.new_quiz_widget_2.setLayout(vbox)
        
        self.new_quiz_widget_2.hide()

    def results_layout(self):
        self.tab_result_main = QTabWidget(self)

        self.tab_finished = QWidget()

        vbox = QVBoxLayout()

        hbox0 = QHBoxLayout()

        lb_finished = QLabel("Quiz beendet")
        lb_finished.setFont(QFont("Times New Roman", 40, QFont.Bold))
        lb_finished.setAlignment(Qt.AlignCenter)
        
        hbox0.addWidget(lb_finished)


        hbox_space = QHBoxLayout()
        hbox_space.addWidget(QLabel())
        
        hbox1 = QHBoxLayout()

        self.lb_result = QLabel()
        self.lb_result.setFont(QFont("Times New Roman", 24, QFont.Cursive))

        hbox1.addWidget(self.lb_result)

        
        hbox2 = QHBoxLayout()
        
        self.lb_time = QLabel()
        self.lb_time.setFont(QFont("Times New Roman", 24, QFont.Cursive))

        hbox2.addWidget(self.lb_time)

        
        hbox3 = QHBoxLayout()

        self.lb_personal_place = QLabel()
        self.lb_personal_place.setFont(QFont("Times New Roman", 24, QFont.Cursive))

        hbox3.addWidget(self.lb_personal_place)


        hbox4 = QHBoxLayout()

        self.lb_global_place = QLabel()
        self.lb_global_place.setFont(QFont("Times New Roman", 24, QFont.Cursive))

        hbox4.addWidget(self.lb_global_place)


        hbox = QHBoxLayout()
        
        self.lb_database_entry = QLabel()
        self.lb_database_entry.setFont(QFont("Times New Roman", 8, QFont.Cursive))
        self.lb_database_entry.setAlignment(Qt.AlignCenter)

        btn_home = QPushButton("Home")
        btn_home.clicked.connect(self.show_home)

        hbox.addWidget(self.lb_database_entry)
        hbox.addStretch()
        hbox.addWidget(btn_home)

        vbox.addLayout(hbox0)
        vbox.addLayout(hbox_space)
        vbox.addLayout(hbox1)
        vbox.addLayout(hbox2)
        vbox.addStretch()
        vbox.addLayout(hbox3)
        vbox.addLayout(hbox4)
        vbox.addStretch()
        vbox.addLayout(hbox)

        self.tab_finished.setLayout(vbox)

        self.tab_result_main.addTab(self.tab_finished, "Beendet")

        self.tab_result_main.hide()

    def highscore_layout(self):
        self.highscore_widget = QWidget(self)

        self.highscore = HighscoreWidget(self.highscore_widget, self.show_home)

        self.highscore.btn_refresh.clicked.connect(self.fill_highscore)

        self.highscore_widget.hide()

    def new_question_layout(self):
        self.new_question_widget = QWidget(self)
        self.new_question_widget.resize(self.width, self.height-25)
        
        vbox = QVBoxLayout()


        hbox0 = QHBoxLayout()
        lb_question = QLabel("Frage")
        lb_question.setFont(QFont("Times New Roman", 15, QFont.Cursive))
        self.le_question = QLineEdit()
        self.le_question.setFont(QFont("Times New Roman", 15, QFont.Cursive))        
        self.le_question.setStyleSheet("border: 1px solid black")

        hbox0.addWidget(lb_question)
        hbox0.addWidget(self.le_question)

        hbox_space = QHBoxLayout()
        hbox_space.addWidget(QLabel())


        hbox1 = QHBoxLayout()
        lb_correct_answer = QLabel("Richtige Antwort  ")
        lb_correct_answer.setFont(QFont("Times New Roman", 12, QFont.Cursive))
        self.le_correct_answer = QLineEdit()
        self.le_correct_answer.setFont(QFont("Times New Roman", 12, QFont.Cursive))        
        self.le_correct_answer.setStyleSheet("border: 1px solid black")

        lb_wrong_answer_1 = QLabel("Falsche Antwort 1")
        lb_wrong_answer_1.setFont(QFont("Times New Roman", 12, QFont.Cursive))
        self.le_wrong_answer_1 = QLineEdit()
        self.le_wrong_answer_1.setFont(QFont("Times New Roman", 12, QFont.Cursive))
        self.le_wrong_answer_1.setStyleSheet("border: 1px solid black")
        
        
        hbox1.addWidget(lb_correct_answer)
        hbox1.addWidget(self.le_correct_answer)
        hbox1.addStretch()
        hbox1.addWidget(lb_wrong_answer_1)
        hbox1.addWidget(self.le_wrong_answer_1)


        hbox2 = QHBoxLayout()
        
        lb_wrong_answer_2 = QLabel("Falsche Antwort 2")
        lb_wrong_answer_2.setFont(QFont("Times New Roman", 12, QFont.Cursive))
        self.le_wrong_answer_2 = QLineEdit()
        self.le_wrong_answer_2.setFont(QFont("Times New Roman", 12, QFont.Cursive))
        self.le_wrong_answer_2.setStyleSheet("border: 1px solid black")

        lb_wrong_answer_3 = QLabel("Falsche Antwort 3")
        lb_wrong_answer_3.setFont(QFont("Times New Roman", 12, QFont.Cursive))
        self.le_wrong_answer_3 = QLineEdit()
        self.le_wrong_answer_3.setFont(QFont("Times New Roman", 12, QFont.Cursive))
        self.le_wrong_answer_3.setStyleSheet("border: 1px solid black")

        hbox2.addWidget(lb_wrong_answer_2)
        hbox2.addWidget(self.le_wrong_answer_2)  
        hbox2.addStretch()      
        hbox2.addWidget(lb_wrong_answer_3)
        hbox2.addWidget(self.le_wrong_answer_3)


        hbox3 = QHBoxLayout()

        lb_category = QLabel("Kategorie")
        lb_category.setFont(QFont("Times New Roman", 12, QFont.Cursive))
        self.le_category = QLineEdit()
        self.le_category.setFont(QFont("Times New Roman", 12, QFont.Cursive))
        self.le_category.setStyleSheet("border: 1px solid black")

        hbox3.addWidget(lb_category)
        hbox3.addWidget(self.le_category)


        hbox4 = QHBoxLayout()

        btn_save = QPushButton("Speichern")
        btn_save.setFont(QFont("Times New Roman", 12, QFont.Cursive))
        btn_save.clicked.connect(self.save_new_question)

        btn_cancel = QPushButton("Abbrechen")
        btn_cancel.clicked.connect(self.show_home)
        btn_cancel.setFont(QFont("Times New Roman", 12, QFont.Cursive))
    	
        hbox4.addStretch()
        hbox4.addWidget(btn_save)
        hbox4.addWidget(btn_cancel)

        vbox.addLayout(hbox0)
        vbox.addLayout(hbox_space)
        vbox.addLayout(hbox1)
        vbox.addLayout(hbox2)
        vbox.addLayout(hbox3)
        vbox.addStretch()
        vbox.addLayout(hbox4)
        
        self.new_question_widget.setLayout(vbox)
        self.new_question_widget.hide()
    
    def edit_question_layout(self):
        self.edit_question_widget = QWidget(self)
        
        vbox = QVBoxLayout()        
        
        hbox = QHBoxLayout()
        btn_save = QPushButton("Speichern")
        # btn_save.clicked.connect()
        btn_cancel = QPushButton("Abbrechen")
        btn_cancel.clicked.connect(self.show_home)
        
        hbox.addStretch()
        hbox.addWidget(btn_save)
        hbox.addWidget(btn_cancel)
        
        vbox.addStretch()
        vbox.addLayout(hbox)
        
        self.edit_question_widget.setLayout(vbox)
        
        self.edit_question_widget.hide()

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
        self.edit_question_widget.hide()
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
                self.edit_question_widget.hide()
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
                self.edit_question_widget.hide()
                self.login_widget.hide()
                
                self.new_quiz_widget_2.show()

                self.current_index = 0
                current_question = self.questions[self.current_index]

                random.seed()
                random_order = list(current_question[2:6])
                random.shuffle(random_order)

                self.lb_question_number.setText(f"Frage {self.current_index+1}")
                self.te_question.insertPlainText(current_question[1])
                self.te_answer_1.setText(random_order[0])
                self.te_answer_2.setText(random_order[1])
                self.te_answer_3.setText(random_order[2])
                self.te_answer_4.setText(random_order[3])

    def show_results(self):
        self.home_widget.hide()
        self.new_quiz_widget_1.hide()
        self.new_quiz_widget_2.hide()
        self.tab_result_main.hide()
        self.highscore_widget.hide()
        self.new_question_widget.hide()
        self.edit_question_widget.hide()
        self.login_widget.hide()
        
        self.tab_result_main.show()

        end_time = round(time.time() - self.quiz_time_start, 2)

        self.lb_result.setText(f"Richtige Antworten: {self.correct_counter} von 15")
        self.lb_time.setText(f"Zeit: {end_time} Sekunden")

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

            reply = pickle.loads(self.client.recv(1024))

            if reply[0]:
                self.lb_database_entry.setText("Datenbank-Eintrag wurde erstellt.")
                self.lb_database_entry.setStyleSheet("color: green;")
            else:
                self.lb_database_entry.setText("Datenbank-Eintrag konnte nicht erstellt werden.")
                self.lb_database_entry.setStyleSheet("color: red;")
            

            if reply[1] == 0:
                self.lb_personal_place.setText(f"Persönlicher Platz: Konnte nicht ermittelt werden")
            else:
                self.lb_personal_place.setText(f"Persönlicher Platz: {str(reply[1])}")

            if reply[2] == 0:
                self.lb_global_place.setText(f"Globaler Platz: Konnte nicht ermittelt werden")
            else:
                self.lb_global_place.setText(f"Globaler Platz: {str(reply[2])}")

        except Exception as e:
            self.connected = False
            self.authenticated = False
            self.lb_server_status.setText("Mit keinem Server verbunden")
            self.lb_server_status.setStyleSheet("color: red")
            
            self.lb_login_status.setText("Nicht angemeldet")
            self.lb_login_status.setStyleSheet("color: red")

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
            self.edit_question_widget.hide()
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
                self.edit_question_widget.hide()
                self.login_widget.hide()

                self.new_question_widget.show()
            else:
                print("Fehlende Rechte")

    def show_edit_question(self):
        if self.connected:
            if self.admin:
                self.home_widget.hide()
                self.new_quiz_widget_1.hide()
                self.new_quiz_widget_2.hide()
                self.tab_result_main.hide()
                self.highscore_widget.hide()
                self.new_question_widget.hide()
                self.edit_question_widget.hide()
                self.login_widget.hide()

                self.edit_question_widget.show()
            else:
                print("Fehlende Rechte")

    def show_login(self):
        self.home_widget.hide()
        self.new_quiz_widget_1.hide()
        self.new_quiz_widget_2.hide()
        self.tab_result_main.hide()
        self.highscore_widget.hide()
        self.new_question_widget.hide()
        self.edit_question_widget.hide()
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
        self.edit_question_widget.resize(self.width, self.height-25)
        self.login_widget.resize(self.width, self.height-25)


class ResultWidget(QWidget):
    def __init__(self, tab_name, parent=None):
        """
        Neuer Tab fürs Tabwidget (parent)
        """
        super().__init__()
        
        self.tab_name = tab_name
        self.parent = parent

        self.init_layout()
        parent.addTab(self, str(tab_name))

    def init_layout(self):
        vbox = QVBoxLayout()
        
        hbox0 = QHBoxLayout()

        lb_question = QLabel(f"{self.tab_name}")
        lb_question.setFont(QFont("Times New Roman", 24, QFont.Cursive))
        lb_question.setAlignment(Qt.AlignCenter)

        hbox0.addWidget(lb_question)

        
        hbox1 = QHBoxLayout()

        self.lb_category = QLabel()
        self.lb_category.setFont(QFont("Times New Roman", 12, QFont.Cursive))

        hbox1.addWidget(self.lb_category)


        hbox2 = QHBoxLayout()

        self.te_question = QTextEdit()
        self.te_question.setFont(QFont("Times New Roman", 12, QFont.Cursive))
        self.te_question.setReadOnly(True)

        hbox2.addWidget(self.te_question)


        hbox3 = QHBoxLayout()

        self.te_answer_1 = QTextEdit()
        self.te_answer_1.setFont(QFont("Times New Roman", 12, QFont.Cursive))
        self.te_answer_1.setReadOnly(True)

        self.te_answer_2 = QTextEdit()
        self.te_answer_2.setFont(QFont("Times New Roman", 12, QFont.Cursive))
        self.te_answer_2.setReadOnly(True)

        hbox3.addWidget(self.te_answer_1)
        hbox3.addWidget(self.te_answer_2)


        hbox4 = QHBoxLayout()

        self.te_answer_3 = QTextEdit()
        self.te_answer_3.setFont(QFont("Times New Roman", 12, QFont.Cursive))
        self.te_answer_3.setReadOnly(True)

        self.te_answer_4 = QTextEdit()
        self.te_answer_4.setFont(QFont("Times New Roman", 12, QFont.Cursive))
        self.te_answer_4.setReadOnly(True)

        hbox4.addWidget(self.te_answer_3)
        hbox4.addWidget(self.te_answer_4)


        hbox5 = QHBoxLayout()

        self.lb_author_plus_date = QLabel()
        self.lb_author_plus_date.setFont(QFont("Times New Roman", 8, QFont.Cursive))

        hbox5.addWidget(self.lb_author_plus_date)


        hbox6 = QHBoxLayout()

        self.lb_last_editor_plus_date = QLabel()
        self.lb_last_editor_plus_date.setFont(QFont("Times New Roman", 8, QFont.Cursive))

        hbox6.addWidget(self.lb_last_editor_plus_date)

        
        vbox.addLayout(hbox0)
        vbox.addLayout(hbox1)
        vbox.addLayout(hbox2)
        vbox.addLayout(hbox3)
        vbox.addLayout(hbox4)
        vbox.addLayout(hbox5)
        vbox.addLayout(hbox6)

        self.setLayout(vbox)

    def fill_layout(self, question, answer):
        self.te_question.insertPlainText(question[1])

        self.lb_category.setText(f"Kategorie: {question[6]}")

        # Erste Antwort ist die Richtige
        self.te_answer_1.insertPlainText(question[5])
        #self.te_answer_1.setStyleSheet("background-color: rgb(153, 255, 153);")
        if question[5] == answer:
            self.te_answer_1.setStyleSheet("border: 3px solid green;background-color: rgb(153, 255, 153);")
        else:
            self.te_answer_1.setStyleSheet("border: 3px solid green;")
        
        self.te_answer_2.insertPlainText(question[2])
        self.te_answer_3.insertPlainText(question[3])
        self.te_answer_4.insertPlainText(question[4])

        
        if question.index(answer) == 2:
            self.te_answer_2.setStyleSheet("background-color: rgb(255, 153, 153);")

        if question.index(answer) == 3:
            self.te_answer_3.setStyleSheet("background-color: rgb(255, 153, 153);")

        if question.index(answer) == 4:
            self.te_answer_4.setStyleSheet("background-color: rgb(255, 153, 153);")

        self.lb_author_plus_date.setText(f"Frage erstellt am: {str(datetime.datetime.fromtimestamp(question[9]).strftime('%d.%m.%Y %H:%M:%S'))} von {question[7]}")
        self.lb_last_editor_plus_date.setText(f"Frage zuletzt bearbeitet am: {str(datetime.datetime.fromtimestamp(question[10]).strftime('%d.%m.%Y %H:%M:%S'))} von {question[8]}")


class HighscoreWidget(QWidget):
    def __init__(self, parent=None, home_func=None):
        super().__init__()
        
        self.parent = parent
        self.home_func = home_func

        self.init_layout()

    def init_layout(self):
        vbox = QVBoxLayout()

        hbox0 = QHBoxLayout()

        lb_highscore = QLabel("Highscore")
        lb_highscore.setFont(QFont("Times New Roman", 40, QFont.Bold))
        lb_highscore.setAlignment(Qt.AlignCenter)
        
        hbox0.addWidget(lb_highscore)


        hbox_space = QHBoxLayout()

        hbox_space.addWidget(QLabel())


        hbox1 = QHBoxLayout()

        self.tw_highscore = QTableWidget()
        self.tw_highscore.setColumnCount(4)
        self.tw_highscore.setRowCount(25)

        self.tw_highscore.setHorizontalHeaderItem(0, QTableWidgetItem("Score"))
        self.tw_highscore.setHorizontalHeaderItem(1, QTableWidgetItem("Zeit"))
        self.tw_highscore.setHorizontalHeaderItem(2, QTableWidgetItem("Username"))
        self.tw_highscore.setHorizontalHeaderItem(3, QTableWidgetItem("Datum"))
        self.tw_highscore.setEditTriggers(QAbstractItemView.NoEditTriggers)

        header = self.tw_highscore.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.Stretch)
        header.setSectionResizeMode(1, QHeaderView.Stretch)
        header.setSectionResizeMode(2, QHeaderView.Stretch)
        header.setSectionResizeMode(3, QHeaderView.Stretch)

        hbox1.addWidget(self.tw_highscore)

        
        hbox = QHBoxLayout()
        self.btn_refresh = QPushButton("Neu laden")
        
        btn_home = QPushButton("Home")
        btn_home.clicked.connect(self.home_func)

        hbox.addWidget(self.btn_refresh)
        hbox.addStretch()
        hbox.addWidget(btn_home)

        vbox.addLayout(hbox0)
        vbox.addLayout(hbox1)
        vbox.addLayout(hbox_space)
        # vbox.addStretch()
        vbox.addLayout(hbox)


        self.parent.setLayout(vbox)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    client = Client()
    sys.exit(app.exec_())
