# -*- coding: utf-8 -*-#
# File:     main.py
# Author:   se7enXF
# Github:   se7enXF
# Date:     2019/2/19
# Note:     使用QtDesigner高效绘制界面，并使用PySide调用

import sys
import random
import time
from datetime import datetime

import cv2
import numpy as np
from PyQt5.QtCore import QEvent, Qt, QTimer, pyqtSignal, QPoint, QRect, QDate, QTime
from PyQt5.QtGui import QPixmap, QPainter, QLinearGradient, QColor, QImage
from PyQt5.QtWidgets import QMainWindow, QTreeWidget, QWidget, QMenu, QLabel

from hostory.hostoryrunqthread import HostoryRunQthread
from hostory.ui_hostory import Ui_HostoryWin

from PyQt5 import QtWidgets, QtCore


class MainWindow(QtWidgets.QMainWindow,Ui_HostoryWin):

    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)

        self.dateEdit.setDate(QDate.currentDate())
        self.timeEdit.setTime(QTime.currentTime())


        self.historycombox.currentIndexChanged.connect(self.on_combobox_func)
        self.selectfilebut.clicked.connect(self.selectFileClik)
        self.hikcamhisitory.clicked.connect(self.hikcamhisitoryClik)
        self.hikcambut.clicked.connect(self.hikcambutClik)
        self.playnext10s.clicked.connect(self.playnext10sClik)

        self.on_combobox_func()

        self.hostoryRun=None

    def playnext10sClik(self):
        self.hostoryRun.playNext10sFun()
        pass
    def hikcambutClik(self):
        url = "rtsp://admin:Hik123456@192.168.31.212/Streaming/Channels/2"

        pass

    def show_frame_txt(self, value):
        self.videoinfotxt.setText(value)
        pass

    def show_frame_pic(self, value):
        qImage = QImage(value.data, value.shape[1], value.shape[0], QImage.Format_BGR888)
        self.capframe.setPixmap(QPixmap.fromImage(qImage))
    def hikcamhisitoryClik(self):

        if self.hostoryRun is not  None:
            # self.hostoryRun.terminate()
            print('清理原来进程')

        if self.hostoryRun is None:
            self.hostoryRun = HostoryRunQthread()
            self.hostoryRun.show_pic.connect(self.show_frame_pic)
            self.hostoryRun.show_frame_txt.connect(self.show_frame_txt)
            self.hostoryRun.start()

            print('创建视频播放进程')
        else:
            self.hostoryRun.pause_process = True


        time_str = self.timeEdit.time().toString('hh:mm:ss')
        date_str = self.dateEdit.date().toString('yyyy-MM-dd')
        print(f'Date: {date_str}, Time: {time_str}')
        qTime = QTime(self.timeEdit.time())
        qDate = QDate(self.dateEdit.date())

        tm = datetime(qDate.year(), qDate.month(), qDate.day(), qTime.hour(), qTime.minute(), qTime.second())
        self.hostoryRun.makeHikHostoryByTm(tm)






    def selectFileClik(self):
        vid_fm = ( ".avi", ".mp4" )
        file_list = " *".join( vid_fm)
        file_name, _ = QtWidgets.QFileDialog.getOpenFileName(self, "choose an image or video file", "./data",
                                                             f"Files({file_list})")
        if file_name:
            # self.pushSelectFile(file_name)
            print(file_name)
            pass
    def on_combobox_func(self):
        combobox=self.historycombox
        print('select',combobox.currentIndex())
        qt= QTime(QTime.currentTime().hour() , 0)
        match combobox.currentIndex():
            case 0:
                qt= QTime(QTime.currentTime().hour() - 1, 0)
            case 1:
                qt = QTime(QTime.currentTime().hour() - 2, 0)
            case 2:
                qt = QTime(QTime.currentTime().hour()-3, 0)
            case 3:
                qt = QTime(QTime.currentTime().hour()-4, 0)
            case 4:
                qt = QTime(15, 0)
            case 5:
                qt = QTime(16, 0)
            case 6:
                qt = QTime(17, 0)
            case 7:
                qt = QTime(18, 0)

        self.timeEdit.setTime(qt)

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()

    sys.exit(app.exec())
