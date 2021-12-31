import sys

from PyQt5.QtWidgets import QApplication, QWidget, QLineEdit, QHBoxLayout, QVBoxLayout, QPushButton

class Calculator(QWidget):
    def __init__(self):
        super(Calculator, self).__init__()
        self.setWindowTitle('Calculator')

        self.input= QLineEdit()
        self.b_1=QPushButton('1')
        self.b_2 = QPushButton('2')
        self.b_3 = QPushButton('3')
        self.b_4 = QPushButton('4')
        self.b_5 = QPushButton('5')
        self.b_6 = QPushButton('6')
        self.b_7 = QPushButton('7')
        self.b_8 = QPushButton('8')
        self.b_9 = QPushButton('9')
        self.b_0 = QPushButton('0')
        self.b_plus = QPushButton('+')
        self.b_multiply = QPushButton('*')
        self.b_divide = QPushButton('/')
        self.b_minus = QPushButton('-')
        self.b_result = QPushButton('=')
        self.b_clc = QPushButton('clc')
        self.b_dot = QPushButton('.')

        self.main_box=QVBoxLayout()

        self.input_box=QHBoxLayout()
        self.first_box=QHBoxLayout()
        self.second_box = QHBoxLayout()
        self.third_box = QHBoxLayout()
        self.fourth_box = QHBoxLayout()

        self.main_box.addLayout(self.input_box)
        self.main_box.addLayout(self.first_box)
        self.main_box.addLayout(self.second_box)
        self.main_box.addLayout(self.third_box)
        self.main_box.addLayout(self.fourth_box)

        self.input_box.addWidget(self.input)
        self.first_box.addWidget(self.b_1)
        self.first_box.addWidget(self.b_2)
        self.first_box.addWidget(self.b_3)
        self.first_box.addWidget(self.b_plus)
        self.second_box.addWidget(self.b_4)
        self.second_box.addWidget(self.b_5)
        self.second_box.addWidget(self.b_6)
        self.second_box.addWidget(self.b_minus)
        self.third_box.addWidget(self.b_7)
        self.third_box.addWidget(self.b_8)
        self.third_box.addWidget(self.b_9)
        self.third_box.addWidget(self.b_multiply)
        self.fourth_box.addWidget(self.b_result)
        self.fourth_box.addWidget(self.b_0)
        self.fourth_box.addWidget(self.b_clc)
        self.fourth_box.addWidget(self.b_divide)
        self.first_box.addWidget(self.b_dot)

        self.setLayout(self.main_box)

        self.b_1.clicked.connect(lambda: self._addNum('1'))
        self.b_2.clicked.connect(lambda: self._addNum('2'))
        self.b_3.clicked.connect(lambda: self._addNum('3'))
        self.b_4.clicked.connect(lambda: self._addNum('4'))
        self.b_5.clicked.connect(lambda: self._addNum('5'))
        self.b_6.clicked.connect(lambda: self._addNum('6'))
        self.b_7.clicked.connect(lambda: self._addNum('7'))
        self.b_8.clicked.connect(lambda: self._addNum('8'))
        self.b_9.clicked.connect(lambda: self._addNum('9'))
        self.b_0.clicked.connect(lambda: self._addNum('0'))
        self.b_plus.clicked.connect(lambda: self._operation('+'))
        self.b_minus.clicked.connect(lambda: self._operation('-'))
        self.b_multiply.clicked.connect(lambda: self._operation('*'))
        self.b_result.clicked.connect(self._result)
        self.b_clc.clicked.connect(self._clc)
        self.b_divide.clicked.connect(lambda: self._operation('/'))
        self.b_dot.clicked.connect(lambda: self._addNum('.'))
        

    def _addNum(self, param):
        line=self.input.text()
        self.input.setText(line+param)

    def _operation(self,op):
        try:
            self.num1 = float(self.input.text())
            self.input.setText('')
        except:
            self.input.setText('Вы ввели текст')
        self.op=op

    def _result(self):
        try:
            self.num2 = float(self.input.text())
            self.input.setText('')
        except:
            self.input.setText('Вы ввели текст')
        if self.num2 == 0 and self.op == '/':
            self.input.setText('Делить на ноль нельзя!')
        else:
            if self.op == '+':
                self.input.setText(str(self.num1+self.num2))
            if self.op == '-':
                self.input.setText(str(self.num1 - self.num2))
            if self.op == '*':
                self.input.setText(str(self.num1 * self.num2))
            if self.op == '/':
                self.input.setText(str(self.num1 / self.num2))

    def _clc(self):
        self.input.setText('')

app = QApplication(sys.argv)

win = Calculator()
win.show()

sys.exit(app.exec_())