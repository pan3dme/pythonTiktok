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
    QDateEdit, QSlider, QVBoxLayout, QLineEdit


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
        self.toolButton.setGeometry(QRect(650, 110, 81, 31))
        self.deepframe = QLabel(self.centralwidget)
        self.deepframe.setObjectName(u"deepframe")
        self.deepframe.setGeometry(QRect(10, 360, 500, 350))
        self.deepframe.setAlignment(Qt.AlignCenter)
        self.radioButton = QRadioButton(self.centralwidget)
        self.radioButton.setObjectName(u"radioButton")
        self.radioButton.setGeometry(QRect(720, 670, 95, 19))
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
        self.historycombox.setGeometry(QRect(650, 160, 101, 40))
        self.reseTrackerBut = QPushButton(self.centralwidget)
        self.reseTrackerBut.setObjectName(u"reseTrackerBut")
        self.reseTrackerBut.setGeometry(QRect(520, 360, 61, 51))
        self.hikcambut = QToolButton(self.centralwidget)
        self.hikcambut.setObjectName(u"hikcambut")
        self.hikcambut.setGeometry(QRect(740, 110, 81, 31))
        self.hikcamhisitory = QToolButton(self.centralwidget)
        self.hikcamhisitory.setObjectName(u"hikcamhisitory")
        self.hikcamhisitory.setGeometry(QRect(760, 160, 80, 40))
        self.dateEdit = QDateEdit(self.centralwidget)
        self.dateEdit.setObjectName(u"dateEdit")
        self.dateEdit.setGeometry(QRect(650, 210, 91, 22))
        self.timeEdit = QTimeEdit(self.centralwidget)
        self.timeEdit.setObjectName(u"timeEdit")
        self.timeEdit.setGeometry(QRect(750, 210, 91, 22))
        self.horizontalSlider = QSlider(self.centralwidget)
        self.horizontalSlider.setObjectName(u"horizontalSlider")
        self.horizontalSlider.setGeometry(QRect(650, 260, 191, 22))
        self.horizontalSlider.setMinimum(1)
        self.horizontalSlider.setMaximum(100)
        self.horizontalSlider.setValue(20)
        self.horizontalSlider.setOrientation(Qt.Horizontal)
        self.clearbut = QPushButton(self.centralwidget)
        self.clearbut.setObjectName(u"clearbut")
        self.clearbut.setGeometry(QRect(200, 810, 91, 41))
        self.videoinfolabel = QLabel(self.centralwidget)
        self.videoinfolabel.setObjectName(u"videoinfolabel")
        self.videoinfolabel.setGeometry(QRect(520, 20, 111, 31))
        self.roiBut = QToolButton(self.centralwidget)
        self.roiBut.setObjectName(u"roiBut")
        self.roiBut.setGeometry(QRect(740, 70, 81, 31))
        self.readVideoBut = QToolButton(self.centralwidget)
        self.readVideoBut.setObjectName(u"readVideoBut")
        self.readVideoBut.setGeometry(QRect(650, 70, 81, 31))
        self.showgoprovideo = QCheckBox(self.centralwidget)
        self.showgoprovideo.setObjectName(u"showgoprovideo")
        self.showgoprovideo.setGeometry(QRect(720, 540, 121, 19))
        self.showGoproSound = QCheckBox(self.centralwidget)
        self.showGoproSound.setObjectName(u"showGoproSound")
        self.showGoproSound.setGeometry(QRect(720, 570, 121, 19))
        self.layoutWidget = QWidget(self.centralwidget)
        self.layoutWidget.setObjectName(u"layoutWidget")
        self.layoutWidget.setGeometry(QRect(710, 290, 121, 223))
        self.verticalLayout = QVBoxLayout(self.layoutWidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.showprogressbar = QCheckBox(self.layoutWidget)
        self.showprogressbar.setObjectName(u"showprogressbar")

        self.verticalLayout.addWidget(self.showprogressbar)

        self.checkBoxShowRoiRect = QCheckBox(self.layoutWidget)
        self.checkBoxShowRoiRect.setObjectName(u"checkBoxShowRoiRect")

        self.verticalLayout.addWidget(self.checkBoxShowRoiRect)

        self.checkBoxShowMaskFrame = QCheckBox(self.layoutWidget)
        self.checkBoxShowMaskFrame.setObjectName(u"checkBoxShowMaskFrame")

        self.verticalLayout.addWidget(self.checkBoxShowMaskFrame)

        self.checkBoxSaveVideo = QCheckBox(self.layoutWidget)
        self.checkBoxSaveVideo.setObjectName(u"checkBoxSaveVideo")

        self.verticalLayout.addWidget(self.checkBoxSaveVideo)

        self.saveFileName = QLineEdit(self.layoutWidget)
        self.saveFileName.setObjectName(u"saveFileName")

        self.verticalLayout.addWidget(self.saveFileName)

        self.capStopCheck = QCheckBox(self.layoutWidget)
        self.capStopCheck.setObjectName(u"capStopCheck")

        self.verticalLayout.addWidget(self.capStopCheck)

        self.deepStopCheck = QCheckBox(self.layoutWidget)
        self.deepStopCheck.setObjectName(u"deepStopCheck")

        self.verticalLayout.addWidget(self.deepStopCheck)

        self.selectCamcombox = QComboBox(self.centralwidget)
        self.selectCamcombox.addItem("")
        self.selectCamcombox.addItem("")
        self.selectCamcombox.setObjectName(u"selectCamcombox")
        self.selectCamcombox.setGeometry(QRect(720, 790, 101, 40))
        self.waitDeepLenSlide = QSlider(self.centralwidget)
        self.waitDeepLenSlide.setObjectName(u"waitDeepLenSlide")
        self.waitDeepLenSlide.setGeometry(QRect(670, 20, 171, 22))
        self.waitDeepLenSlide.setMinimum(100)
        self.waitDeepLenSlide.setMaximum(5000)
        self.waitDeepLenSlide.setValue(1000)
        self.waitDeepLenSlide.setOrientation(Qt.Horizontal)
        self.waitdeepnumtxt = QLabel(self.centralwidget)
        self.waitdeepnumtxt.setObjectName(u"waitdeepnumtxt")
        self.waitdeepnumtxt.setGeometry(QRect(620, 20, 41, 21))
        self.fpsnumtxt = QLabel(self.centralwidget)
        self.fpsnumtxt.setObjectName(u"fpsnumtxt")
        self.fpsnumtxt.setGeometry(QRect(620, 260, 21, 21))
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
        self.readVideoBut.setText(QCoreApplication.translate("MainWindow", u"\u8bfb\u53d6\u8bb0\u5f55", None))
        self.showgoprovideo.setText(QCoreApplication.translate("MainWindow", u"\u663e\u793aGopro", None))
        self.showGoproSound.setText(QCoreApplication.translate("MainWindow", u"gopro\u58f0\u97f3", None))
        self.showprogressbar.setText(QCoreApplication.translate("MainWindow", u"\u663e\u793a\u89c6\u9891\u8fdb\u5ea6", None))
        self.checkBoxShowRoiRect.setText(QCoreApplication.translate("MainWindow", u"\u663e\u793a\u9009\u62e9\u533a\u57df", None))
        self.checkBoxShowMaskFrame.setText(QCoreApplication.translate("MainWindow", u"\u663e\u793a\u68c0\u6d4bmask", None))
        self.checkBoxSaveVideo.setText(QCoreApplication.translate("MainWindow", u"\u4fdd\u5b58\u8bc6\u522b\u89c6\u9891", None))
        self.saveFileName.setText(QCoreApplication.translate("MainWindow", u"tiktok.mp4", None))
        self.capStopCheck.setText(QCoreApplication.translate("MainWindow", u"\u89c6\u9891\u6682\u505c", None))
        self.deepStopCheck.setText(QCoreApplication.translate("MainWindow", u"\u68c0\u6d4b\u6682\u505c", None))
        self.selectCamcombox.setItemText(0, QCoreApplication.translate("MainWindow", u"212", None))
        self.selectCamcombox.setItemText(1, QCoreApplication.translate("MainWindow", u"231", None))

        self.waitdeepnumtxt.setText(QCoreApplication.translate("MainWindow", u"\u5185\u5b58\u6570", None))
        self.fpsnumtxt.setText(QCoreApplication.translate("MainWindow", u"fps", None))
    # retranslateUi

