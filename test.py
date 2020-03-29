import sys
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QWidget
 
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QGridLayout
from PyQt5.QtWidgets import QLineEdit
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QVBoxLayout
 
from functools import partial
 
ERROR_MSG = 'ERROR'
 
# Create a subclass of QMainWindow to setup the calculator's GUI
class PyCalcUI(QMainWindow):
    def __init__(self):
        super().__init__()
        # set Window size properties+
        self.setWindowTitle('Sven´s PyCalculator')
        self.setFixedSize(280, 225) # Fixed Window size. Not resizeble.
        self.mainLayout = QVBoxLayout()
        self._centralWidget = QWidget(self)
        self.setCentralWidget(self._centralWidget)
        self._centralWidget.setLayout(self.mainLayout)
        # Create the display and the buttons
        self._createDisplay()
        self._createButtons()
 
    def _createDisplay(self):
        # Create Display widget
        self.display = QLineEdit() #QlineEdit object as display widget
        # set Display properties
        self.display.setFixedHeight(35)
        self.display.setAlignment(Qt.AlignRight)
        self.display.setReadOnly(True) #set to read-only to avoid editing
        # add the display to general layout
        self.mainLayout.addWidget(self.display) #adds display to calcs general layout
 
    def _createButtons(self):
        # create the buttons
        self.buttons = {} # empty dictionary
        butttonsLayout = QGridLayout() #to store labels and relative postions on the grid layout
        # button text, position on the QGridLayout
        buttons = {'7': (0, 0),
                   '8': (0, 1),
                   '9': (0, 2),
                   '/': (0, 3),
                   'C': (0, 4),
                   '4': (1, 0),
                   '5': (1, 1),
                   '6': (1, 2),
                   '*': (1, 3),
                   '(': (1, 4),
                   '1': (2, 0),
                   '2': (2, 1),
                   '3': (2, 2),
                   '-': (2, 3),
                   ')': (2, 4),
                   '0': (3, 0),
                   '00': (3, 1),
                   '.': (3, 2),
                   '+': (3, 3),
                   '=': (3, 4),
                   }
        # create the buttons and add them to grid
        for btnText, pos in buttons.items(): #create the buttons and add them to self.buttons and buttonsLayout
            self.buttons[btnText] = QPushButton(btnText)
            self.buttons[btnText].setFixedSize(40, 40)
            butttonsLayout.addWidget(self.buttons[btnText], pos[0], pos[1])
            self.mainLayout.addLayout(butttonsLayout)
 
    def setDisplayText(self, text): # uses .setText() to set and update the displays content
        self.display.setText(text)
        self.display.setFocus() #set cursors focus to display
 
    def displayText(self):
        return self.display.text() # getter method that returns the displays current content. When user clicks on = procram will return value of .displayText()
 
    def clearDisplay(self):
        self.setDisplayText('') # sets displays content to an empty string so the user can input a new calculation
 
class PyCalcCtrl:
    def __init__(self, model, view):
        # Controller initializer
        self._evaluate = model
        self._view = view
        self._connectSignals()
 
    def _calculateResult(self):
        result = self._evaluate(expression=self._view.displayText())
        self._view.setDisplayText(result)
 
    def _buildExpression(self, sub_exp):
        #ERROR_MSG = 'ERROR'
        if self._view.displayText() == ERROR_MSG:
            self._view.clearDisplay()
 
        #buildExpression to handle the creation of math expressions, updates the calculators display in response to input
        expression = self._view.displayText() + sub_exp
        self._view.setDisplayText(expression)
 
    def _connectSignals(self):
        # connect signals and slots
        for btnText, btn in self._view.buttons.items():
            if btnText not in {'=', 'C'}:
                btn.clicked.connect(partial(self._buildExpression, btnText))
 
        self._view.buttons['='].clicked.connect(self._calculateResult)
        self._view.display.returnPressed.connect(self._calculateResult)
        self._view.buttons['C'].clicked.connect(self._view.clearDisplay) #method to clear up the text on the display
 
def evaluateExpression(expression):
    """Evaluate an expression."""
    try:
        result = str(eval(expression, {}, {}))
    except Exception:
        result = ERROR_MSG
 
    return result
 
def main():
    # Create an instance of QApplication
    pycalc = QApplication(sys.argv)
    # Show the calculator's GUI
    view = PyCalcUI()
    view.show()
    # Create instances of the model and the controller
    model = evaluateExpression
    PyCalcCtrl(model=model, view=view)
    # Execute calculator's main loop
    sys.exit(pycalc.exec_())
 
if __name__ == '__main__':

        main()
