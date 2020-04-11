import datetime

from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *


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

        hbox1.addWidget(self.tw_edit_question)


        hbox = QHBoxLayout()
        self.btn_home = QPushButton("Home")
        hbox.addStretch()
        hbox.addWidget(self.btn_home)

        vbox.addLayout(hbox0)
        vbox.addLayout(hbox1)
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


        hbox5 = QHBoxLayout()

        self.cb_autologin = QCheckBox("Automatischer Login")
        self.cb_autoconnect = QCheckBox("Automatisch Verbindung zum Server aufbauen")
        
        hbox5.addWidget(self.cb_autologin)
        hbox5.addWidget(self.cb_autoconnect)
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
