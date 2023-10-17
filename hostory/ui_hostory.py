# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'hostory_main.ui'
##
## Created by: Qt User Interface Compiler version 6.5.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################



from PyQt5.QtCore import QRect, Qt, QCoreApplication, QMetaObject
from PyQt5.QtWidgets import QToolButton, QPushButton, QLabel, QWidget, QRadioButton, QCheckBox, QComboBox, QTimeEdit, \
    QDateEdit, QSlider, QVBoxLayout, QLineEdit

# pyside6-uic hostory_main.ui > ui_hostory.py




class Ui_HostoryWin(object):
    def setupUi(self, HostoryWin):
        if not HostoryWin.objectName():
            HostoryWin.setObjectName(u"HostoryWin")
        HostoryWin.resize(865, 887)
        self.centralwidget = QWidget(HostoryWin)
        self.centralwidget.setObjectName(u"centralwidget")
        self.historycombox = QComboBox(self.centralwidget)
        self.historycombox.addItem("")
        self.historycombox.addItem("")
        self.historycombox.addItem("")
        self.historycombox.addItem("")
        self.historycombox.addItem("")
        self.historycombox.addItem("")
        self.historycombox.addItem("")
        self.historycombox.addItem("")
        self.historycombox.setObjectName(u"historycombox")
        self.historycombox.setGeometry(QRect(640, 100, 101, 40))
        self.hikcamhisitory = QToolButton(self.centralwidget)
        self.hikcamhisitory.setObjectName(u"hikcamhisitory")
        self.hikcamhisitory.setGeometry(QRect(750, 100, 80, 40))
        self.selectfilebut = QToolButton(self.centralwidget)
        self.selectfilebut.setObjectName(u"selectfilebut")
        self.selectfilebut.setGeometry(QRect(640, 40, 91, 41))
        self.timeEdit = QTimeEdit(self.centralwidget)
        self.timeEdit.setObjectName(u"timeEdit")
        self.timeEdit.setGeometry(QRect(740, 150, 91, 22))
        self.dateEdit = QDateEdit(self.centralwidget)
        self.dateEdit.setObjectName(u"dateEdit")
        self.dateEdit.setGeometry(QRect(640, 150, 91, 22))
        self.capframe = QLabel(self.centralwidget)
        self.capframe.setObjectName(u"capframe")
        self.capframe.setGeometry(QRect(20, 30, 500, 350))
        self.capframe.setAlignment(Qt.AlignCenter)
        self.videoinfotxt = QLabel(self.centralwidget)
        self.videoinfotxt.setObjectName(u"videoinfotxt")
        self.videoinfotxt.setGeometry(QRect(10, 430, 281, 21))
        self.hikcambut = QToolButton(self.centralwidget)
        self.hikcambut.setObjectName(u"hikcambut")
        self.hikcambut.setGeometry(QRect(750, 40, 81, 41))
        self.playnext10s = QToolButton(self.centralwidget)
        self.playnext10s.setObjectName(u"playnext10s")
        self.playnext10s.setGeometry(QRect(740, 190, 81, 41))
        self.playpre10s = QToolButton(self.centralwidget)
        self.playpre10s.setObjectName(u"playpre10s")
        self.playpre10s.setGeometry(QRect(640, 190, 81, 41))
        HostoryWin.setCentralWidget(self.centralwidget)

        self.retranslateUi(HostoryWin)

        QMetaObject.connectSlotsByName(HostoryWin)
    # setupUi

    def retranslateUi(self, HostoryWin):
        HostoryWin.setWindowTitle(QCoreApplication.translate("HostoryWin", u"MainWindow", None))
        self.historycombox.setItemText(0, QCoreApplication.translate("HostoryWin", u"1\u4e2a\u5c0f\u65f6\u524d", None))
        self.historycombox.setItemText(1, QCoreApplication.translate("HostoryWin", u"2\u4e2a\u5c0f\u65f6\u524d", None))
        self.historycombox.setItemText(2, QCoreApplication.translate("HostoryWin", u"3\u4e2a\u5c0f\u65f6\u524d", None))
        self.historycombox.setItemText(3, QCoreApplication.translate("HostoryWin", u"4\u4e2a\u5c0f\u65f6\u524d", None))
        self.historycombox.setItemText(4, QCoreApplication.translate("HostoryWin", u"\u4eca\u592915\u70b9", None))
        self.historycombox.setItemText(5, QCoreApplication.translate("HostoryWin", u"\u4eca\u592916\u70b9", None))
        self.historycombox.setItemText(6, QCoreApplication.translate("HostoryWin", u"\u4eca\u592917\u70b9", None))
        self.historycombox.setItemText(7, QCoreApplication.translate("HostoryWin", u"\u4eca\u592918\u70b9", None))

        self.hikcamhisitory.setText(QCoreApplication.translate("HostoryWin", u"\u76d1\u63a7\u5f55\u50cf", None))
        self.selectfilebut.setText(QCoreApplication.translate("HostoryWin", u"\u9009\u62e9\u6587\u4ef6", None))
        self.capframe.setText(QCoreApplication.translate("HostoryWin", u"\u539f\u59cb\u89c6\u9891", None))
        self.videoinfotxt.setText(QCoreApplication.translate("HostoryWin", u"TextLabel", None))
        self.hikcambut.setText(QCoreApplication.translate("HostoryWin", u"\u65f6\u65f6\u76d1\u63a7", None))
        self.playnext10s.setText(QCoreApplication.translate("HostoryWin", u"\u5feb\u8fdb10\u79d2", None))
        self.playpre10s.setText(QCoreApplication.translate("HostoryWin", u"\u5012\u900010\u79d2", None))
    # retranslateUi

