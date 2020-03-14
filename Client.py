import socket
import pickle
import sqlite3
import json
import threading
import os
import sys
import time

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

        if os.path.exists("Config/clientsettings.json"):
            with open("Config/clientsettings.json", "r+") as f:
                try:
                    self.settings = json.load(f)
                    
                    self.le_ip.setText(str(self.settings.get("serversettings").get("ip")))
                    self.le_port.setText(str(self.settings.get("serversettings").get("port")))
                    self.le_username.setText(str(self.settings.get("usersettings").get("username")))
                    self.le_password.setText(str(self.settings.get("usersettings").get("password")))
                    self.cb_autologin.setChecked(self.settings.get("generalsettings").get("autologin"))
                    self.cb_remember_data.setChecked(self.settings.get("generalsettings").get("rememberdata"))

                except Exception as e:
                    self.settings = {}
                    print(e)
        else:
            self.settings = {}

        self.timer_connect = QTimer()
        self.timer_connect.timeout.connect(self.connect_to_server)
        self.timer_connect.start(5000)
            

    def connect_to_server(self):
        if not self.connected:
            if self.settings:
                if self.settings.get("generalsettings").get("autologin"):
                    try:
                        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                        self.client.connect((self.settings.get("serversettings").get("ip"), self.settings.get("serversettings").get("port")))
                        self.connected = True

                        self.authentication()
                    except Exception as e:
                        print(e)
    
    def authentication(self):
        if self.connected:
            if self.settings:
                try:
                    credentials = [self.settings.get("usersettings").get("username"), self.settings.get("usersettings").get("password")]
                    pickled = pickle.dumps(credentials)
                    
                    try:
                        self.client.send(pickled)
                        self.authenticated = pickle.loads(self.client.recv(1024))
                        print(self.authenticated)
                    except Exception as e:
                        self.connected = False
                        print(e)

                except Exception as e:
                    print(e)
                    

    def init_layouts(self):
        self.home_layout()
        self.new_quiz_layout()
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
        btn_start_quiz.clicked.connect(self.show_new_quiz)
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

        vbox.addLayout(hbox0)
        vbox.addLayout(hbox_space)
        vbox.addLayout(hbox1)
        vbox.addLayout(hbox2)
        vbox.addLayout(hbox3)
        vbox.addLayout(hbox4)
        vbox.addLayout(hbox5)
        vbox.addStretch()

        self.home_widget.setLayout(vbox)

    def new_quiz_layout(self):
        self.new_quiz_widget = QWidget(self)

        self.new_quiz_widget.hide()

    def highscore_layout(self):
        self.highscore_widget = QWidget(self)

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

        hbox0.addWidget(lb_question)
        hbox0.addWidget(self.le_question)

        hbox_space = QHBoxLayout()
        hbox_space.addWidget(QLabel())

        hbox1 = QHBoxLayout()
        lb_correct_answer = QLabel("Richtige Antwort  ")
        lb_correct_answer.setFont(QFont("Times New Roman", 12, QFont.Cursive))
        self.le_correct_answer = QLineEdit()
        self.le_correct_answer.setFont(QFont("Times New Roman", 12, QFont.Cursive))

        lb_wrong_answer_1 = QLabel("Falsche Antwort 1")
        lb_wrong_answer_1.setFont(QFont("Times New Roman", 12, QFont.Cursive))
        self.le_wrong_answer_1 = QLineEdit()
        self.le_wrong_answer_1.setFont(QFont("Times New Roman", 12, QFont.Cursive))
        
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

        lb_wrong_answer_3 = QLabel("Falsche Antwort 3")
        lb_wrong_answer_3.setFont(QFont("Times New Roman", 12, QFont.Cursive))
        self.le_wrong_answer_3 = QLineEdit()
        self.le_wrong_answer_3.setFont(QFont("Times New Roman", 12, QFont.Cursive))

        hbox2.addWidget(lb_wrong_answer_2)
        hbox2.addWidget(self.le_wrong_answer_2)  
        hbox2.addStretch()      
        hbox2.addWidget(lb_wrong_answer_3)
        hbox2.addWidget(self.le_wrong_answer_3)

        hbox3 = QHBoxLayout()

        btn_save = QPushButton("Speichern")
        btn_save.setFont(QFont("Times New Roman", 12, QFont.Cursive))
        btn_cancel = QPushButton("Abbrechen")
        btn_cancel.clicked.connect(self.show_home)
        btn_cancel.setFont(QFont("Times New Roman", 12, QFont.Cursive))
    	
        hbox3.addStretch()
        hbox3.addWidget(btn_save)
        hbox3.addWidget(btn_cancel)

        vbox.addLayout(hbox0)
        vbox.addLayout(hbox_space)
        vbox.addLayout(hbox1)
        vbox.addLayout(hbox2)
        vbox.addStretch()
        vbox.addLayout(hbox3)
        
        self.new_question_widget.setLayout(vbox)
        self.new_question_widget.hide()
    
    def edit_question_layout(self):
        self.edit_question_widget = QWidget(self)

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

        self.cb_remember_data = QCheckBox("Daten merken")
        self.cb_autologin = QCheckBox("Automatischer Login")
        
        hbox5.addWidget(self.cb_remember_data)
        hbox5.addWidget(self.cb_autologin)
        hbox5.addStretch()


        hbox6 = QHBoxLayout()
        
        btn_save = QPushButton("Speichern und Ausführen")
        #btn_save.clicked.connect()
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
        self.new_quiz_widget.hide()
        self.highscore_widget.hide()
        self.new_question_widget.hide()
        self.edit_question_widget.hide()
        self.login_widget.hide()
        
        self.home_widget.show()

    def show_new_quiz(self):
        self.home_widget.hide()
        self.new_quiz_widget.hide()
        self.highscore_widget.hide()
        self.new_question_widget.hide()
        self.edit_question_widget.hide()
        self.login_widget.hide()
        
        self.new_quiz_widget.show()

    def show_highscore(self):
        self.home_widget.hide()
        self.new_quiz_widget.hide()
        self.highscore_widget.hide()
        self.new_question_widget.hide()
        self.edit_question_widget.hide()
        self.login_widget.hide()

        self.highscore_widget.show()

    def show_new_question(self):
        self.home_widget.hide()
        self.new_quiz_widget.hide()
        self.highscore_widget.hide()
        self.new_question_widget.hide()
        self.edit_question_widget.hide()
        self.login_widget.hide()

        self.new_question_widget.show()

    def show_edit_question(self):
        self.home_widget.hide()
        self.new_quiz_widget.hide()
        self.highscore_widget.hide()
        self.new_question_widget.hide()
        self.edit_question_widget.hide()
        self.login_widget.hide()

        self.edit_question_widget.show()

    def show_login(self):
        self.home_widget.hide()
        self.new_quiz_widget.hide()
        self.highscore_widget.hide()
        self.new_question_widget.hide()
        self.edit_question_widget.hide()
        self.login_widget.hide()

        self.login_widget.show()

    def resizeEvent(self, event):        
        self.width = self.frameGeometry().width()
        self.height = self.frameGeometry().height()
        
        self.home_widget.resize(self.width, self.height-25)
        self.new_question_widget.resize(self.width, self.height-25)
        self.highscore_widget.resize(self.width, self.height-25)
        self.new_question_widget.resize(self.width, self.height-25)
        self.edit_question_widget.resize(self.width, self.height-25)
        self.login_widget.resize(self.width, self.height-25)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    client = Client()
    sys.exit(app.exec_())
