from PyQt5 import QtCore, Qt
from PyQt5.QtCore import QPoint, QRect
from PyQt5.QtWidgets import QApplication, QWidget, QLabel
from PyQt5.QtGui import QIcon, QFont, QPixmap, QMovie, QLinearGradient, QPainter, QColor
import sys
from PyQt5.QtCore import QEvent, Qt, QTimer
from PyQt5.QtGui import   QPainter
from PyQt5.QtWidgets import   QWidget, QMenu


class TBQLabel(QLabel):
    def __init__(self,value):
        super().__init__(value)



     

class Window(QWidget):
    def __init__(self):
        super().__init__()

        self.setGeometry(200, 200, 1000, 750)
        self.setWindowTitle('First window')

        label = TBQLabel(self)
        label.setText("welcome to CSDN")

        # label.setNum(860)

        label.move(300, 300)
        # label.setFont(QFont("Sanserif", 20))
        # label.setStyleSheet('color:red')
        # label.connect_customized_slot(self.labelClik)

        def labelClik(self):
            print('labelClik')
            pass


app = QApplication(sys.argv)
window = Window()
window.show()
sys.exit(app.exec())