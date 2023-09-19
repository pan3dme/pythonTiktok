# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'mainwindow.ui'
##
## Created by: Qt User Interface Compiler version 6.5.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################


from PyQt5.QtCore import QRect, Qt, QCoreApplication, QMetaObject
from PyQt5.QtWidgets import QToolButton, QPushButton, QLabel, QWidget, QRadioButton, QCheckBox, QComboBox, QTimeEdit, \
    QDateEdit, QSlider


# pyside6-uic mainwindow.ui > ui_mainwindow.py

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(865, 887)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.capframe = QLabel(self.centralwidget)
        self.capframe.setObjectName(u"capframe")
        self.capframe.setGeometry(QRect(10, 10, 500, 350))
        self.capframe.setAlignment(Qt.AlignCenter)
        self.pushButton = QPushButton(self.centralwidget)
        self.pushButton.setObjectName(u"pushButton")
        self.pushButton.setGeometry(QRect(60, 810, 91, 41))
        self.toolButton = QToolButton(self.centralwidget)
        self.toolButton.setObjectName(u"toolButton")
        self.toolButton.setGeometry(QRect(570, 30, 81, 31))
        self.deepframe = QLabel(self.centralwidget)
        self.deepframe.setObjectName(u"deepframe")
        self.deepframe.setGeometry(QRect(10, 360, 500, 350))
        self.deepframe.setAlignment(Qt.AlignCenter)
        self.radioButton = QRadioButton(self.centralwidget)
        self.radioButton.setObjectName(u"radioButton")
        self.radioButton.setGeometry(QRect(740, 460, 95, 19))
        self.checkBox = QCheckBox(self.centralwidget)
        self.checkBox.setObjectName(u"checkBox")
        self.checkBox.setGeometry(QRect(750, 580, 80, 19))
        self.checkBox_2 = QCheckBox(self.centralwidget)
        self.checkBox_2.setObjectName(u"checkBox_2")
        self.checkBox_2.setGeometry(QRect(750, 620, 80, 19))
        self.radioButton_2 = QRadioButton(self.centralwidget)
        self.radioButton_2.setObjectName(u"radioButton_2")
        self.radioButton_2.setGeometry(QRect(740, 510, 95, 19))
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
        self.historycombox.setGeometry(QRect(650, 90, 101, 40))
        self.reseTrackerBut = QPushButton(self.centralwidget)
        self.reseTrackerBut.setObjectName(u"reseTrackerBut")
        self.reseTrackerBut.setGeometry(QRect(520, 360, 61, 51))
        self.hikcambut = QToolButton(self.centralwidget)
        self.hikcambut.setObjectName(u"hikcambut")
        self.hikcambut.setGeometry(QRect(670, 30, 81, 31))
        self.hikcamhisitory = QToolButton(self.centralwidget)
        self.hikcamhisitory.setObjectName(u"hikcamhisitory")
        self.hikcamhisitory.setGeometry(QRect(760, 90, 80, 40))
        self.dateEdit = QDateEdit(self.centralwidget)
        self.dateEdit.setObjectName(u"dateEdit")
        self.dateEdit.setGeometry(QRect(650, 140, 91, 22))
        self.timeEdit = QTimeEdit(self.centralwidget)
        self.timeEdit.setObjectName(u"timeEdit")
        self.timeEdit.setGeometry(QRect(750, 140, 91, 22))
        self.horizontalSlider = QSlider(self.centralwidget)
        self.horizontalSlider.setObjectName(u"horizontalSlider")
        self.horizontalSlider.setGeometry(QRect(650, 190, 191, 22))
        self.horizontalSlider.setMinimum(1)
        self.horizontalSlider.setMaximum(30)
        self.horizontalSlider.setValue(10)
        self.horizontalSlider.setOrientation(Qt.Horizontal)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.capframe.setText(QCoreApplication.translate("MainWindow", u"\u539f\u59cb\u89c6\u9891", None))
        self.pushButton.setText(QCoreApplication.translate("MainWindow", u"\u6682\u505c/\u64ad\u653e", None))
        self.toolButton.setText(QCoreApplication.translate("MainWindow", u"\u9009\u62e9\u6587\u4ef6", None))
        self.deepframe.setText(QCoreApplication.translate("MainWindow", u"\u8ddf\u8e2a\u68c0\u6d4b", None))
        self.radioButton.setText(QCoreApplication.translate("MainWindow", u"RadioButton", None))
        self.checkBox.setText(QCoreApplication.translate("MainWindow", u"\u663e\u793a\u539f\u89c6\u9891", None))
        self.checkBox_2.setText(QCoreApplication.translate("MainWindow", u"\u663e\u793a\u68c0\u6d4b", None))
        self.radioButton_2.setText(QCoreApplication.translate("MainWindow", u"RadioButton", None))
        self.historycombox.setItemText(0, QCoreApplication.translate("MainWindow", u"1\u4e2a\u5c0f\u65f6\u524d", None))
        self.historycombox.setItemText(1, QCoreApplication.translate("MainWindow", u"2\u4e2a\u5c0f\u65f6\u524d", None))
        self.historycombox.setItemText(2, QCoreApplication.translate("MainWindow", u"3\u4e2a\u5c0f\u65f6\u524d", None))
        self.historycombox.setItemText(3, QCoreApplication.translate("MainWindow", u"4\u4e2a\u5c0f\u65f6\u524d", None))
        self.historycombox.setItemText(4, QCoreApplication.translate("MainWindow", u"\u4eca\u592915\u70b9", None))
        self.historycombox.setItemText(5, QCoreApplication.translate("MainWindow", u"\u4eca\u592916\u70b9", None))
        self.historycombox.setItemText(6, QCoreApplication.translate("MainWindow", u"\u4eca\u592917\u70b9", None))
        self.historycombox.setItemText(7, QCoreApplication.translate("MainWindow", u"\u4eca\u592918\u70b9", None))

        self.reseTrackerBut.setText(QCoreApplication.translate("MainWindow", u"\u91cd\u65b0\u68c0\u6d4b", None))
        self.hikcambut.setText(QCoreApplication.translate("MainWindow", u"\u65f6\u65f6\u76d1\u63a7", None))
        self.hikcamhisitory.setText(QCoreApplication.translate("MainWindow", u"\u76d1\u63a7\u5f55\u50cf", None))
    # retranslateUi

