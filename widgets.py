import datetime
import sys

from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

from functions import *


class HomeWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__()

        self.parent = parent

        self.init_layout()

    def init_layout(self):
        vbox = QVBoxLayout()

        hbox0 = QHBoxLayout()
        lb_title = QLabel("Quiz")
        lb_title.setFont(QFont("Times New Roman", 40, QFont.Bold))
        lb_title.setAlignment(Qt.AlignCenter)
        hbox0.addWidget(lb_title)

        hbox_space = QHBoxLayout()
        hbox_space.addWidget(QLabel())

        hbox1 = QHBoxLayout()
        self.btn_start_quiz = QPushButton("Neues Quiz")
        self.btn_start_quiz.setFont(QFont("Times New Roman", 25, QFont.Cursive))
        hbox1.addWidget(self.btn_start_quiz)
        hbox1.addStretch()

        hbox2 = QHBoxLayout()
        self.btn_show_highscore = QPushButton("Highscoreliste")
        self.btn_show_highscore.setFont(QFont("Times New Roman", 25, QFont.Cursive))
        hbox2.addWidget(self.btn_show_highscore)
        hbox2.addStretch()

        hbox3 = QHBoxLayout()
        self.btn_new_question = QPushButton("Neue Frage erstellen")
        self.btn_new_question.setFont(QFont("Times New Roman", 25, QFont.Cursive))
        hbox3.addWidget(self.btn_new_question)
        hbox3.addStretch()

        hbox4 = QHBoxLayout()
        self.btn_edit_delete_question = QPushButton("Frage bearbeiten/löschen")
        self.btn_edit_delete_question.setFont(QFont("Times New Roman", 25, QFont.Cursive))
        hbox4.addWidget(self.btn_edit_delete_question)
        hbox4.addStretch()

        hbox5 = QHBoxLayout()
        self.btn_login = QPushButton("Login")
        self.btn_login.setFont(QFont("Times New Roman", 25, QFont.Cursive))
        hbox5.addWidget(self.btn_login)
        hbox5.addStretch()

        hbox6 = QHBoxLayout()
        self.btn_admin_panel = QPushButton("Adminpanel")
        self.btn_admin_panel.setFont(QFont("Times New Roman", 25, QFont.Cursive))
        hbox6.addWidget(self.btn_admin_panel)
        hbox6.addStretch()

        hbox7 = QHBoxLayout()
        self.lb_server_status = QLabel("Zurzeit mit keinem Server verbunden")
        self.lb_server_status.setFont(QFont("Times New Roman", 12, QFont.Bold))
        self.lb_server_status.setStyleSheet("color: red")
        hbox7.addStretch()
        hbox7.addWidget(self.lb_server_status)

        hbox8 = QHBoxLayout()
        self.lb_status = QLabel()
        self.lb_status.setFont(QFont("Times New Roman", 12, QFont.Bold))
        
        self.lb_login_status = QLabel("Nicht angemeldet")
        self.lb_login_status.setFont(QFont("Times New Roman", 12, QFont.Bold))
        self.lb_login_status.setStyleSheet("color: red")
        hbox8.addWidget(self.lb_status)
        hbox8.addStretch()
        hbox8.addWidget(self.lb_login_status)

        vbox.addLayout(hbox0)
        vbox.addLayout(hbox_space)
        vbox.addLayout(hbox1)
        vbox.addLayout(hbox2)
        vbox.addLayout(hbox3)
        vbox.addLayout(hbox4)
        vbox.addLayout(hbox5)
        vbox.addLayout(hbox6)
        vbox.addStretch()
        vbox.addLayout(hbox7)
        vbox.addLayout(hbox8)

        self.parent.setLayout(vbox)


class NewQuizWidget1(QWidget):
    def __init__(self, parent):
        super().__init__()

        self.parent = parent

        self.init_layout()

    def init_layout(self):
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

        self.btn_start = QPushButton("Start")
        self.btn_start.setFont(QFont("Times New Roman", 30, QFont.Bold))

        hbox1.addWidget(self.btn_start, alignment=Qt.AlignCenter)


        hbox2 = QHBoxLayout()
        self.btn_cancel = QPushButton("Abbrechen")  
        
        hbox2.addStretch()
        hbox2.addWidget(self.btn_cancel)
        
        
        vbox.addLayout(hbox0)
        vbox.addLayout(hbox_space0)
        vbox.addLayout(hbox_space1)
        vbox.addLayout(hbox_space2)
        vbox.addLayout(hbox1)
        vbox.addStretch()
        vbox.addLayout(hbox2)
        
        self.parent.setLayout(vbox)


class NewQuizWidget2(QWidget):
    def __init__(self, parent=None):
        super().__init__()

        self.parent = parent

        self.init_layout()

    def init_layout(self):
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

        self.btn_answer_2 = QPushButton("B")
        self.btn_answer_2.setFont(QFont("Times New Roman", 15, QFont.Cursive))
        
        hbox3.addWidget(self.btn_answer_1)
        hbox3.addWidget(self.btn_answer_2)


        hbox4 = QHBoxLayout()

        self.te_answer_3 = QTextEdit()
        self.te_answer_3.setDisabled(True)
        
        
        self.te_answer_4 = QTextEdit()
        self.te_answer_4.setDisabled(True)
        

        hbox4.addWidget(self.te_answer_3)
        hbox4.addWidget(self.te_answer_4)


        hbox5 = QHBoxLayout()

        self.btn_answer_3 = QPushButton("C")
        self.btn_answer_3.setFont(QFont("Times New Roman", 15, QFont.Cursive))
        
        self.btn_answer_4 = QPushButton("D")
        self.btn_answer_4.setFont(QFont("Times New Roman", 15, QFont.Cursive))
        
        hbox5.addWidget(self.btn_answer_3)
        hbox5.addWidget(self.btn_answer_4)


        vbox.addLayout(hbox0)
        vbox.addLayout(hbox_space)
        vbox.addLayout(hbox1)
        vbox.addLayout(hbox2)
        vbox.addLayout(hbox3)
        vbox.addStretch()
        vbox.addLayout(hbox4)
        vbox.addLayout(hbox5)
        vbox.addStretch()

        self.parent.setLayout(vbox)


class ResultWidget(QWidget):
    def __init__(self, tab_name, question, client, parent=None):
        """
        Neuer Tab fürs Tabwidget (parent)
        """
        super().__init__()
        
        self.tab_name = tab_name
        self.question = question
        self.client = client
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
        self.btn_complain_question = QPushButton("Frage beanstanden")
        self.btn_complain_question.clicked.connect(self.complain_question)

        hbox5.addWidget(self.lb_author_plus_date)
        hbox5.addStretch()
        hbox5.addWidget(self.btn_complain_question)


        hbox6 = QHBoxLayout()

        self.lb_last_editor_plus_date = QLabel()
        self.lb_last_editor_plus_date.setFont(QFont("Times New Roman", 8, QFont.Cursive))
        self.lb_status = QLabel()

        hbox6.addWidget(self.lb_last_editor_plus_date)
        hbox6.addStretch()
        hbox6.addWidget(self.lb_status)

        
        vbox.addLayout(hbox0)
        vbox.addLayout(hbox1)
        vbox.addLayout(hbox2)
        vbox.addLayout(hbox3)
        vbox.addLayout(hbox4)
        vbox.addLayout(hbox5)
        vbox.addLayout(hbox6)

        self.setLayout(vbox)

    def fill_layout(self, answer):
        self.te_question.insertPlainText(self.question[1])

        self.lb_category.setText(f"Kategorie: {self.question[6]}")

        # Erste Antwort ist die Richtige
        self.te_answer_1.insertPlainText(self.question[5])

        if self.question[5] == answer:
            self.te_answer_1.setStyleSheet("border: 3px solid green;background-color: rgb(153, 255, 153);")
        else:
            self.te_answer_1.setStyleSheet("border: 3px solid green;")
        
        self.te_answer_2.insertPlainText(self.question[2])
        self.te_answer_3.insertPlainText(self.question[3])
        self.te_answer_4.insertPlainText(self.question[4])

        
        if self.question.index(answer) == 2:
            self.te_answer_2.setStyleSheet("background-color: rgb(255, 153, 153);")

        if self.question.index(answer) == 3:
            self.te_answer_3.setStyleSheet("background-color: rgb(255, 153, 153);")

        if self.question.index(answer) == 4:
            self.te_answer_4.setStyleSheet("background-color: rgb(255, 153, 153);")

        self.lb_author_plus_date.setText(f"Frage erstellt am: {str(datetime.datetime.fromtimestamp(self.question[9]).strftime('%d.%m.%Y %H:%M:%S'))} von {self.question[7]}")
        self.lb_last_editor_plus_date.setText(f"Frage zuletzt bearbeitet am: {str(datetime.datetime.fromtimestamp(self.question[10]).strftime('%d.%m.%Y %H:%M:%S'))} von {self.question[8]}")

    def complain_question(self):        
        if not self.lb_status.text():
            try:
                self.dialog.close()
            except:
                pass

            self.dialog = ComplainingQuestionDialog(self.question, self.client, self)
            self.dialog.show()
        
        else:
            self.lb_status.setText("Report wurde schon gesendet")
            self.lb_status.setStyleSheet("color: red;")


class ComplainingQuestionDialog(QDialog):
    def __init__(self, question, client, parent=None):
        super().__init__(parent=parent)

        self.question = question
        self.client = client
        self.parent = parent

        self.init_layout()

    def init_layout(self):
        vbox = QVBoxLayout()

        hbox0 = QHBoxLayout()
        lb_question_number = QLabel("Frage beanstanden")
        lb_question_number.setFont(QFont("Times New Roman", 30, QFont.Bold))
        lb_question_number.setAlignment(Qt.AlignCenter)

        hbox0.addWidget(lb_question_number)

        hbox_space0 = QHBoxLayout()
        hbox_space0.addWidget(QLabel())

        hbox1 = QHBoxLayout()
        lb_comment = QLabel("Kommentar:")
        lb_comment.setFont(QFont("Times New Roman", 18, QFont.Bold))
        hbox1.addWidget(lb_comment)
        
        hbox2 = QHBoxLayout()
        self.te_comment = QTextEdit()
        hbox2.addWidget(self.te_comment)

        hbox_space1 = QHBoxLayout()
        hbox_space1.addWidget(QLabel())

        hbox3 = QHBoxLayout()
        lb_suggested_answer = QLabel("Vorgeschlagene Anwort:")
        lb_suggested_answer.setFont(QFont("Times New Roman", 18, QFont.Bold))
        hbox3.addWidget(lb_suggested_answer)

        hbox4 = QHBoxLayout()
        self.te_suggested_answer = QTextEdit()
        hbox4.addWidget(self.te_suggested_answer)

        hbox5 = QHBoxLayout()
        self.btn_send_complain = QPushButton("Senden")
        self.btn_send_complain.clicked.connect(self.check_entries)
        self.btn_cancel = QPushButton("Abbrechen")
        self.btn_cancel.clicked.connect(self.close)
        hbox5.addStretch()
        hbox5.addWidget(self.btn_send_complain)
        hbox5.addWidget(self.btn_cancel)


        vbox.addLayout(hbox0)
        vbox.addLayout(hbox_space0)
        vbox.addLayout(hbox1)        
        vbox.addLayout(hbox2)
        vbox.addLayout(hbox_space1)
        vbox.addLayout(hbox3)
        vbox.addLayout(hbox4)
        vbox.addLayout(hbox5)
        vbox.addStretch()

        self.setLayout(vbox)
    
    def check_entries(self):
        check = True

        if not self.te_comment.toPlainText().strip():            
            self.te_comment.setStyleSheet("border: 1px solid red;")
            check = False
        else:
            self.te_comment.setStyleSheet("border: 1px solid black;")
        
        if not self.te_suggested_answer.toPlainText().strip():            
            self.te_suggested_answer.setStyleSheet("border: 1px solid red;")
            check = False
        else:
            self.te_suggested_answer.setStyleSheet("border: 1px solid black;")

        if check:
            try:
                send(self.client, 15)   # Code um eine beanstandete Frage einzureichen
                recv(self.client)   # Pseudo

                # Daten wie folgt senden (quiz_id, comment, suggested_answer, username)
                data = (self.question[0], self.te_comment.toPlainText(),
                        self.te_suggested_answer.toPlainText(), self.question[7])

                send(self.client, data)
                
                response = recv(self.client)    # Nachricht, ob Eintrag geklappt hat
                
                
                if response[0]:
                    self.parent.lb_status.setText("Report wurde gesendet")
                    self.parent.lb_status.setStyleSheet("color: green;")

                else:
                    self.parent.lb_status.setText("Report konnte nicht gesendet werden")
                    self.parent.lb_status.setStyleSheet("color: red;")
                
                self.close()



            except Exception as e:
                self.client.close()
                print(e)


class FinishedTab(QWidget):
    def __init__(self, parent=None):
        super().__init__()

        self.parent = parent

        self.init_layout()

    def init_layout(self):
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

        self.btn_home = QPushButton("Home")

        hbox.addWidget(self.lb_database_entry)
        hbox.addStretch()
        hbox.addWidget(self.btn_home)

        vbox.addLayout(hbox0)
        vbox.addLayout(hbox_space)
        vbox.addLayout(hbox1)
        vbox.addLayout(hbox2)
        vbox.addStretch()
        vbox.addLayout(hbox3)
        vbox.addLayout(hbox4)
        vbox.addStretch()
        vbox.addLayout(hbox)

        self.parent.setLayout(vbox)


class HighscoreWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__()
        
        self.parent = parent

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
        
        self.btn_home = QPushButton("Home")

        hbox.addWidget(self.btn_refresh)
        hbox.addStretch()
        hbox.addWidget(self.btn_home)

        vbox.addLayout(hbox0)
        vbox.addLayout(hbox1)
        vbox.addLayout(hbox_space)
        # vbox.addStretch()
        vbox.addLayout(hbox)


        self.parent.setLayout(vbox)


class NewQuestionWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__()

        self.parent = parent

        self.init_layout()

    def init_layout(self):
        vbox = QVBoxLayout()

        hbox = QHBoxLayout()
        
        lb_question_ = QLabel("Neue Frage erstellen")
        lb_question_.setFont(QFont("Times New Roman", 40, QFont.Bold))
        lb_question_.setAlignment(Qt.AlignCenter)

        hbox.addWidget(lb_question_)

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

        self.btn_save = QPushButton("Speichern")
        self.btn_save.setFont(QFont("Times New Roman", 12, QFont.Cursive))

        self.btn_cancel = QPushButton("Abbrechen")
        self.btn_cancel.setFont(QFont("Times New Roman", 12, QFont.Cursive))
    	
        hbox4.addStretch()
        hbox4.addWidget(self.btn_save)
        hbox4.addWidget(self.btn_cancel)

        vbox.addLayout(hbox)
        vbox.addLayout(hbox0)
        vbox.addLayout(hbox_space)
        vbox.addLayout(hbox1)
        vbox.addLayout(hbox2)
        vbox.addLayout(hbox3)
        vbox.addStretch()
        vbox.addLayout(hbox4)
        
        self.parent.setLayout(vbox)


class EditQuestionWidget1(QWidget):
    def __init__(self, parent=None):
        super().__init__()

        self.parent = parent

        self.init_layout()

    def init_layout(self):
        vbox = QVBoxLayout()

        hbox0 = QHBoxLayout()
        lb_edit_delete_question = QLabel("Frage bearbeiten/löschen")
        lb_edit_delete_question.setFont(QFont("Times New Roman", 40, QFont.Bold))
        lb_edit_delete_question.setAlignment(Qt.AlignCenter)

        hbox0.addWidget(lb_edit_delete_question)

        hbox1 = QHBoxLayout()
        lb_category = QLabel("Kategorie")
        self.cb_category = QComboBox()
        hbox1.addWidget(lb_category)
        hbox1.addWidget(self.cb_category)
        hbox1.addStretch()

        hbox2 = QHBoxLayout()

        self.tw_edit_question = QTableWidget()
        self.tw_edit_question.setColumnCount(7)
        self.tw_edit_question.verticalHeader().hide()
        self.tw_edit_question.setHorizontalHeaderLabels(["Quiz-ID", "Frage", "Kategory", "Author", "Letzter Bearbeiter", "Erstellungsdatum", "Änderungsdatum"])
        
        header = self.tw_edit_question.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.Stretch)
        header.setSectionResizeMode(1, QHeaderView.Stretch)
        header.setSectionResizeMode(2, QHeaderView.Stretch)
        header.setSectionResizeMode(3, QHeaderView.Stretch)
        header.setSectionResizeMode(4, QHeaderView.Stretch)
        header.setSectionResizeMode(5, QHeaderView.Stretch)
        header.setSectionResizeMode(6, QHeaderView.Stretch)

        hbox2.addWidget(self.tw_edit_question)


        hbox = QHBoxLayout()
        self.btn_home = QPushButton("Home")
        hbox.addStretch()
        hbox.addWidget(self.btn_home)

        vbox.addLayout(hbox0)
        vbox.addLayout(hbox1)
        vbox.addLayout(hbox2)
        vbox.addLayout(hbox)

        self.parent.setLayout(vbox)


class EditQuestionWidget2(QWidget):
    def __init__(self, parent=None):
        super().__init__()

        self.parent = parent

        self.init_layout()
    
    def init_layout(self):
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

        self.btn_delete = QPushButton("Löschen")

        hbox4.addWidget(self.btn_delete)


        hbox5 = QHBoxLayout()

        self.btn_save = QPushButton("Speichern")
        self.btn_save.setFont(QFont("Times New Roman", 12, QFont.Cursive))

        self.btn_cancel = QPushButton("Abbrechen")
        self.btn_cancel.setFont(QFont("Times New Roman", 12, QFont.Cursive))
    	
        hbox5.addStretch()
        hbox5.addWidget(self.btn_save)
        hbox5.addWidget(self.btn_cancel)

        vbox.addLayout(hbox)
        vbox.addLayout(hbox0)
        vbox.addLayout(hbox_space)
        vbox.addLayout(hbox1)
        vbox.addLayout(hbox2)
        vbox.addLayout(hbox3)
        vbox.addStretch()
        vbox.addLayout(hbox4)
        vbox.addStretch()
        vbox.addLayout(hbox5)
        
        self.parent.setLayout(vbox)


class LoginWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__()

        self.parent = parent

        self.init_layout()

    def init_layout(self):
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

        
        hbox_space2 = QHBoxLayout()
        hbox_space2.addWidget(QLabel())


        hbox5 = QHBoxLayout()

        self.btn_new_account = QPushButton("Erstelle neuen Account")

        hbox5.addWidget(self.btn_new_account)
        hbox5.addStretch()


        hbox6 = QHBoxLayout()
        
        self.btn_save = QPushButton("Speichern und Ausführen")
        self.btn_cancel = QPushButton("Abbrechen")
        hbox6.addStretch()
        hbox6.addWidget(self.btn_save)
        hbox6.addWidget(self.btn_cancel)


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

        self.parent.setLayout(vbox)


class CreateAccountWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__()

        self.parent = parent

        self.init_layout()

    def init_layout(self):
        vbox_main = QVBoxLayout()

        hbox_header = QHBoxLayout()
        lb_new_account = QLabel("Neuer Account")
        lb_new_account.setFont(QFont("Times New Roman", 40, QFont.Bold))
        lb_new_account.setAlignment(Qt.AlignCenter)
        hbox_header.addWidget(lb_new_account)
        

        hbox_main = QHBoxLayout()        

        vbox0 = QVBoxLayout()

        hbox0_v0 = QHBoxLayout()
        lb_fname = QLabel("Vorname")
        hbox0_v0.addWidget(lb_fname)
        hbox0_v0.addStretch()
        
        hbox1_v0 = QHBoxLayout()
        lb_lname = QLabel("Nachname")
        hbox1_v0.addWidget(lb_lname)
        hbox1_v0.addStretch()

        hbox2_v0 = QHBoxLayout()
        lb_email = QLabel("Email")
        hbox2_v0.addWidget(lb_email)
        hbox2_v0.addStretch()

        hbox3_v0 = QHBoxLayout()
        lb_username = QLabel("Benutzername")
        hbox3_v0.addWidget(lb_username)
        hbox3_v0.addStretch()

        hbox4_v0 = QHBoxLayout()
        lb_password = QLabel("Passwort")
        hbox4_v0.addWidget(lb_password)
        hbox4_v0.addStretch()

        hbox5_v0 = QHBoxLayout()
        self.lb_status = QLabel()
        hbox5_v0.addWidget(self.lb_status)
        hbox5_v0.addStretch()


        vbox0.addLayout(hbox0_v0)
        vbox0.addLayout(hbox1_v0)
        vbox0.addLayout(hbox2_v0)
        vbox0.addLayout(hbox3_v0)
        vbox0.addLayout(hbox4_v0)
        vbox0.addLayout(hbox5_v0)


        vbox1 = QVBoxLayout()

        hbox0_v1 = QHBoxLayout()
        self.le_fname = QLineEdit()
        hbox0_v1.addWidget(self.le_fname)

        hbox1_v1 = QHBoxLayout()
        self.le_lname = QLineEdit()
        hbox1_v1.addWidget(self.le_lname)

        hbox2_v1 = QHBoxLayout()
        self.le_email = QLineEdit()
        hbox2_v1.addWidget(self.le_email)
        
        hbox3_v1 = QHBoxLayout()
        self.le_username = QLineEdit()
        hbox3_v1.addWidget(self.le_username)

        hbox4_v1 = QHBoxLayout()
        self.le_password = QLineEdit()
        self.le_password.setEchoMode(QLineEdit.Password)
        hbox4_v1.addWidget(self.le_password)

        hbox5_v1 = QHBoxLayout()
        self.btn_ok = QPushButton("OK")
        self.btn_back = QPushButton("Zurück")
        self.btn_cancel = QPushButton("Abbrechen")
        hbox5_v1.addStretch()
        hbox5_v1.addWidget(self.btn_ok)
        hbox5_v1.addWidget(self.btn_back)
        hbox5_v1.addWidget(self.btn_cancel)


        vbox1.addLayout(hbox0_v1)
        vbox1.addLayout(hbox1_v1)
        vbox1.addLayout(hbox2_v1)
        vbox1.addLayout(hbox3_v1)
        vbox1.addLayout(hbox4_v1)
        vbox1.addLayout(hbox5_v1)

        hbox_main.addLayout(vbox0)
        hbox_main.addLayout(vbox1)

        vbox_main.addLayout(hbox_header)
        vbox_main.addStretch()
        vbox_main.addLayout(hbox_main)
        vbox_main.addStretch(2)

        self.parent.setLayout(vbox_main)


class AdminpanelWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__()

        self.parent = parent

        self.init_layout()

    def init_layout(self):
        vbox = QVBoxLayout()

        hbox0 = QHBoxLayout()

        lb_adminpanel = QLabel("Adminpanel")
        lb_adminpanel.setFont(QFont("Times New Roman", 40, QFont.Bold))
        lb_adminpanel.setAlignment(Qt.AlignCenter)
        hbox0.addWidget(lb_adminpanel)

        hbox_space0 = QHBoxLayout()
        hbox_space0.addWidget(QLabel())

        hbox1 = QHBoxLayout()
        lb_user = QLabel("Username")
        self.le_user = QLineEdit()
        self.btn_ok = QPushButton("Ok")
        hbox1.addWidget(lb_user)
        hbox1.addWidget(self.le_user)
        hbox1.addWidget(self.btn_ok)
        hbox1.addStretch()


        hbox2 = QHBoxLayout()
        self.btn_complaining_questions = QPushButton("Beanstandete Fragen")
        hbox2.addWidget(self.btn_complaining_questions)
        hbox2.addStretch()


        hbox = QHBoxLayout()
        self.lb_status = QLabel()
        self.btn_home = QPushButton("Home")
        hbox.addWidget(self.lb_status)
        hbox.addStretch()
        hbox.addWidget(self.btn_home)       

        vbox.addLayout(hbox0)
        vbox.addLayout(hbox_space0)
        vbox.addLayout(hbox1)       
        vbox.addLayout(hbox2)       
        vbox.addStretch()
        vbox.addLayout(hbox)


        self.parent.setLayout(vbox)


class EditUserWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__()

        self.parent = parent

        self.init_layout()

    def init_layout(self):
        vbox = QVBoxLayout()
        
        hbox0 = QHBoxLayout()

        lb_edit_user = QLabel("Benutzer bearbeiten")
        lb_edit_user.setFont(QFont("Times New Roman", 40, QFont.Bold))
        lb_edit_user.setAlignment(Qt.AlignCenter)
        hbox0.addWidget(lb_edit_user)

        hbox_space = QHBoxLayout()
        hbox_space.addWidget(QLabel())

        
        hbox1 = QHBoxLayout()
        lb_username = QLabel("Username")
        self.le_username = QLineEdit()
        self.le_username.setDisabled(True)
        hbox1.addWidget(lb_username)
        hbox1.addWidget(self.le_username)
        hbox1.addStretch()

        hbox2 = QHBoxLayout()
        lb_email = QLabel("Email")
        self.le_email = QLineEdit()
        self.le_email.setDisabled(True)
        hbox2.addWidget(lb_email)
        hbox2.addWidget(self.le_email)
        hbox2.addStretch()

        hbox3 = QHBoxLayout()
        lb_fname = QLabel("Vorname")
        self.le_fname = QLineEdit()
        self.le_fname.setDisabled(True)
        hbox3.addWidget(lb_fname)
        hbox3.addWidget(self.le_fname)
        hbox3.addStretch()

        hbox4 = QHBoxLayout()
        lb_lname = QLabel("Nachname")
        self.le_lname = QLineEdit()
        self.le_lname.setDisabled(True)
        hbox4.addWidget(lb_lname)
        hbox4.addWidget(self.le_lname)
        hbox4.addStretch()

        hbox5 = QHBoxLayout()
        lb_password_reset = QLabel("Neues Passwort")
        self.le_new_password = QLineEdit()
        self.le_new_password.setDisabled(True)
        hbox5.addWidget(lb_password_reset)
        hbox5.addWidget(self.le_new_password)
        hbox5.addStretch()

        hbox6 = QHBoxLayout()
        lb_admin = QLabel("Admin")
        self.cb_admin = QComboBox()
        self.cb_admin.addItems(["Ja", "Nein"])
        self.cb_admin.setDisabled(True)
        hbox6.addWidget(lb_admin)
        hbox6.addWidget(self.cb_admin)
        hbox6.addStretch()

        hbox7 = QHBoxLayout()
        self.btn_save = QPushButton("Speichern")
        self.btn_edit = QPushButton("Bearbeiten aktivieren")
        self.btn_edit.clicked.connect(self.enable_disable_edit)
        hbox7.addWidget(self.btn_save)
        hbox7.addWidget(self.btn_edit)
        hbox7.addStretch()

        hbox = QHBoxLayout()
        self.btn_home = QPushButton("Home")
        self.btn_back = QPushButton("Zurück")
        hbox.addStretch()
        hbox.addWidget(self.btn_home)
        hbox.addWidget(self.btn_back)
        

        vbox.addLayout(hbox0)
        vbox.addLayout(hbox_space)
        vbox.addLayout(hbox1)
        vbox.addLayout(hbox2)
        vbox.addLayout(hbox3)
        vbox.addLayout(hbox4)
        vbox.addLayout(hbox5)
        vbox.addLayout(hbox6)
        vbox.addLayout(hbox7)
        vbox.addStretch()
        vbox.addLayout(hbox)

        self.parent.setLayout(vbox)

    def enable_disable_edit(self):
        if self.btn_edit.text() == "Bearbeiten aktivieren":
            self.btn_edit.setText("Bearbeiten deaktivieren")
            self.le_email.setDisabled(False)
            self.le_fname.setDisabled(False)
            self.le_lname.setDisabled(False)
            self.le_new_password.setDisabled(False)
            self.cb_admin.setDisabled(False)
        else:
            self.btn_edit.setText("Bearbeiten aktivieren")
            self.le_email.setDisabled(True)
            self.le_fname.setDisabled(True)
            self.le_lname.setDisabled(True)
            self.le_new_password.setDisabled(True)
            self.cb_admin.setDisabled(True)


class ComplainingQuestionsWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__()

        self.parent = parent

        self.init_layout()

    def init_layout(self):
        vbox = QVBoxLayout()

        hbox0 = QHBoxLayout()
        lb_complained_questions = QLabel("Beanstandete Fragen")
        lb_complained_questions.setFont(QFont("Times New Roman", 40, QFont.Bold))
        lb_complained_questions.setAlignment(Qt.AlignCenter)
        hbox0.addWidget(lb_complained_questions)
        
        hbox_space = QHBoxLayout()
        hbox_space.addWidget(QLabel())

        hbox1 = QHBoxLayout()
        hbox1.addWidget(QLabel("Beanstandete Frage:"))

        hbox2 = QHBoxLayout()
        self.cb_complained_questions = QComboBox()
        hbox2.addWidget(self.cb_complained_questions)

        
        hbox_main = QHBoxLayout()
        
        vbox_left = QVBoxLayout()
        
        hbox0_left = QHBoxLayout()
        lb_complainer = QLabel("Beanstander")
        self.le_complainer = QLineEdit()
        self.le_complainer.setReadOnly(True)
        hbox0_left.addWidget(lb_complainer)
        hbox0_left.addWidget(self.le_complainer)
        hbox0_left.addStretch()

        hbox1_left = QHBoxLayout()
        lb_date = QLabel("Datum")
        self.le_date = QLineEdit()
        self.le_date.setReadOnly(True)
        hbox1_left.addWidget(lb_date)
        hbox1_left.addWidget(self.le_date)
        hbox1_left.addStretch()

        hbox2_left = QHBoxLayout()
        lb_comment = QLabel("Kommentar")
        hbox2_left.addWidget(lb_comment)
        hbox2_left.addStretch()

        hbox3_left = QHBoxLayout()
        self.te_comment = QTextEdit()
        self.te_comment.setReadOnly(True)
        hbox3_left.addWidget(self.te_comment)

        hbox4_left = QHBoxLayout()
        lb_correct_answer = QLabel("Richtige Antwort")
        hbox4_left.addWidget(lb_correct_answer)

        hbox5_left = QHBoxLayout()
        self.te_correct_answer = QTextEdit()
        self.te_correct_answer.setReadOnly(True)
        hbox5_left.addWidget(self.te_correct_answer)

        hbox6_left = QHBoxLayout()
        lb_suggested_answer = QLabel("Vorgeschlagene Antwort")
        hbox6_left.addWidget(lb_suggested_answer)

        hbox7_left = QHBoxLayout()
        self.te_suggested_answer = QTextEdit()
        self.te_suggested_answer.setReadOnly(True)
        hbox7_left.addWidget(self.te_suggested_answer)

        hbox8_left = QHBoxLayout()
        self.btn_home = QPushButton("Home")
        self.btn_back = QPushButton("Zurück")
        hbox8_left.addWidget(self.btn_home)
        hbox8_left.addWidget(self.btn_back)
        hbox8_left.addStretch()

        vbox_left.addLayout(hbox0_left)
        vbox_left.addLayout(hbox1_left)
        vbox_left.addLayout(hbox2_left)
        vbox_left.addLayout(hbox3_left)
        vbox_left.addLayout(hbox4_left)
        vbox_left.addLayout(hbox5_left)
        vbox_left.addLayout(hbox6_left)
        vbox_left.addLayout(hbox7_left)
        vbox_left.addLayout(hbox8_left)
        vbox_left.addStretch()


        vbox_middle = QVBoxLayout()
        vertical_line = QFrame()
        vertical_line.setFrameShape(QFrame.VLine)
        vertical_line.setFrameShadow(QFrame.Sunken)
        vbox_middle.addWidget(vertical_line)


        vbox_right = QVBoxLayout()
        
        hbox0_right = QHBoxLayout()
        lb_question = QLabel("Frage")
        lb_question.setFont(QFont("Times New Roman", 20, QFont.Bold))
        self.lb_status = QLabel()
        hbox0_right.addWidget(lb_question)
        hbox0_right.addWidget(self.lb_status)

        hbox1_right = QHBoxLayout()
        self.te_question = QTextEdit()
        self.te_question.setReadOnly(True)
        hbox1_right.addWidget(self.te_question)

        hbox2_right = QHBoxLayout()
        self.te_correct = QTextEdit()
        self.te_correct.setStyleSheet("border: 3px solid green;")
        hbox2_right.addWidget(self.te_correct)

        hbox3_right = QHBoxLayout()
        self.te_wrong1 = QTextEdit()
        self.te_wrong1.setStyleSheet("border: 1px solid red;")
        hbox3_right.addWidget(self.te_wrong1)

        hbox4_right = QHBoxLayout()
        self.te_wrong2 = QTextEdit()
        self.te_wrong2.setStyleSheet("border: 1px solid red;")
        hbox4_right.addWidget(self.te_wrong2)
        
        hbox5_right = QHBoxLayout()
        self.te_wrong3 = QTextEdit()
        self.te_wrong3.setStyleSheet("border: 1px solid red;")
        hbox5_right.addWidget(self.te_wrong3)

        hbox6_right = QHBoxLayout()
        lb_category = QLabel("Kategorie")
        self.le_category = QLineEdit()
        hbox6_right.addWidget(lb_category)
        hbox6_right.addWidget(self.le_category)

        hbox7_right = QHBoxLayout()
        self.btn_save = QPushButton("Frage speichern")
        self.btn_delete_complained_question = QPushButton("Beanstandete Frage löschen")
        hbox7_right.addStretch()
        hbox7_right.addWidget(self.btn_save)
        hbox7_right.addWidget(self.btn_delete_complained_question)

        

        vbox_right.addLayout(hbox0_right)
        vbox_right.addLayout(hbox1_right)
        vbox_right.addLayout(hbox2_right)
        vbox_right.addLayout(hbox3_right)
        vbox_right.addLayout(hbox4_right)
        vbox_right.addLayout(hbox5_right)
        vbox_right.addLayout(hbox6_right)
        vbox_right.addLayout(hbox7_right)


        hbox_main.addLayout(vbox_left)
        hbox_main.addLayout(vbox_middle)
        hbox_main.addLayout(vbox_right)

        vbox.addLayout(hbox0)
        vbox.addLayout(hbox1)
        vbox.addLayout(hbox2)
        vbox.addLayout(hbox_main)
        vbox.addStretch()

        self.parent.setLayout(vbox)



if __name__ == "__main__":
    app = QApplication(sys.argv)
    a = ComplainingQuestionDialog()
    a.show()
    sys.exit(app.exec_())
