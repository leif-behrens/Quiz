import datetime

from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *


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
