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
        self.toolButton.setGeometry(QRect(650, 70, 81, 31))
        self.deepframe = QLabel(self.centralwidget)
        self.deepframe.setObjectName(u"deepframe")
        self.deepframe.setGeometry(QRect(10, 360, 500, 350))
        self.deepframe.setAlignment(Qt.AlignCenter)
        self.radioButton = QRadioButton(self.centralwidget)
        self.radioButton.setObjectName(u"radioButton")
        self.radioButton.setGeometry(QRect(720, 670, 95, 19))
        self.checkBoxShowRoiRect = QCheckBox(self.centralwidget)
        self.checkBoxShowRoiRect.setObjectName(u"checkBoxShowRoiRect")
        self.checkBoxShowRoiRect.setGeometry(QRect(720, 260, 121, 19))
        self.checkBox_2 = QCheckBox(self.centralwidget)
        self.checkBox_2.setObjectName(u"checkBox_2")
        self.checkBox_2.setGeometry(QRect(730, 750, 80, 19))
        self.radioButton_2 = QRadioButton(self.centralwidget)
        self.radioButton_2.setObjectName(u"radioButton_2")
        self.radioButton_2.setGeometry(QRect(720, 700, 95, 19))
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
        self.historycombox.setGeometry(QRect(650, 120, 101, 40))
        self.reseTrackerBut = QPushButton(self.centralwidget)
        self.reseTrackerBut.setObjectName(u"reseTrackerBut")
        self.reseTrackerBut.setGeometry(QRect(520, 360, 61, 51))
        self.hikcambut = QToolButton(self.centralwidget)
        self.hikcambut.setObjectName(u"hikcambut")
        self.hikcambut.setGeometry(QRect(740, 70, 81, 31))
        self.hikcamhisitory = QToolButton(self.centralwidget)
        self.hikcamhisitory.setObjectName(u"hikcamhisitory")
        self.hikcamhisitory.setGeometry(QRect(760, 120, 80, 40))
        self.dateEdit = QDateEdit(self.centralwidget)
        self.dateEdit.setObjectName(u"dateEdit")
        self.dateEdit.setGeometry(QRect(650, 170, 91, 22))
        self.timeEdit = QTimeEdit(self.centralwidget)
        self.timeEdit.setObjectName(u"timeEdit")
        self.timeEdit.setGeometry(QRect(750, 170, 91, 22))
        self.horizontalSlider = QSlider(self.centralwidget)
        self.horizontalSlider.setObjectName(u"horizontalSlider")
        self.horizontalSlider.setGeometry(QRect(650, 220, 191, 22))
        self.horizontalSlider.setMinimum(1)
        self.horizontalSlider.setMaximum(30)
        self.horizontalSlider.setValue(10)
        self.horizontalSlider.setOrientation(Qt.Horizontal)
        self.clearbut = QPushButton(self.centralwidget)
        self.clearbut.setObjectName(u"clearbut")
        self.clearbut.setGeometry(QRect(200, 810, 91, 41))
        self.videoinfolabel = QLabel(self.centralwidget)
        self.videoinfolabel.setObjectName(u"videoinfolabel")
        self.videoinfolabel.setGeometry(QRect(550, 20, 291, 41))
        self.roiBut = QToolButton(self.centralwidget)
        self.roiBut.setObjectName(u"roiBut")
        self.roiBut.setGeometry(QRect(740, 30, 81, 31))
        self.checkBoxShowMaskFrame = QCheckBox(self.centralwidget)
        self.checkBoxShowMaskFrame.setObjectName(u"checkBoxShowMaskFrame")
        self.checkBoxShowMaskFrame.setGeometry(QRect(720, 290, 121, 19))
        self.checkBoxSaveVideo = QCheckBox(self.centralwidget)
        self.checkBoxSaveVideo.setObjectName(u"checkBoxSaveVideo")
        self.checkBoxSaveVideo.setGeometry(QRect(720, 320, 121, 19))
        self.readVideoBut = QToolButton(self.centralwidget)
        self.readVideoBut.setObjectName(u"readVideoBut")
        self.readVideoBut.setGeometry(QRect(650, 30, 81, 31))
        self.deepStopCheck = QCheckBox(self.centralwidget)
        self.deepStopCheck.setObjectName(u"deepStopCheck")
        self.deepStopCheck.setGeometry(QRect(720, 390, 121, 19))
        self.capStopCheck = QCheckBox(self.centralwidget)
        self.capStopCheck.setObjectName(u"capStopCheck")
        self.capStopCheck.setGeometry(QRect(720, 360, 121, 19))
        self.showgoprovideo = QCheckBox(self.centralwidget)
        self.showgoprovideo.setObjectName(u"showgoprovideo")
        self.showgoprovideo.setGeometry(QRect(720, 430, 121, 19))
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
        self.checkBoxShowRoiRect.setText(QCoreApplication.translate("MainWindow", u"\u663e\u793a\u9009\u62e9\u533a\u57df", None))
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
        self.clearbut.setText(QCoreApplication.translate("MainWindow", u"\u6e05\u7406\u6240\u6709\u8fdb\u7a0b", None))
        self.videoinfolabel.setText(QCoreApplication.translate("MainWindow", u"TextLabel", None))
        self.roiBut.setText(QCoreApplication.translate("MainWindow", u"\u9009\u62e9\u533a\u57df", None))
        self.checkBoxShowMaskFrame.setText(QCoreApplication.translate("MainWindow", u"\u663e\u793a\u68c0\u6d4bmask", None))
        self.checkBoxSaveVideo.setText(QCoreApplication.translate("MainWindow", u"\u4fdd\u5b58\u8bc6\u522b\u89c6\u9891", None))
        self.readVideoBut.setText(QCoreApplication.translate("MainWindow", u"\u8bfb\u53d6\u8bb0\u5f55", None))
        self.deepStopCheck.setText(QCoreApplication.translate("MainWindow", u"\u68c0\u6d4b\u6682\u505c", None))
        self.capStopCheck.setText(QCoreApplication.translate("MainWindow", u"\u89c6\u9891\u6682\u505c", None))
        self.showgoprovideo.setText(QCoreApplication.translate("MainWindow", u"\u663e\u793aGopro", None))
    # retranslateUi

