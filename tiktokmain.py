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
from PyQt5.QtCore import QEvent, Qt, QTimer, pyqtSignal, QPoint, QRect, QDate, QTime
from PyQt5.QtGui import QPixmap, QPainter, QLinearGradient, QColor, QImage
from PyQt5.QtWidgets import QMainWindow, QTreeWidget, QWidget, QMenu, QLabel

from Lesson_01.mainmousekey import MainWindowMouseKey
from Lesson_01.video_deep_qthread import VideoDeepQthread

from PyQt5 import QtWidgets, QtCore

from Lesson_01.video_run_qthread import VideoRunQThread


# 主窗体类

class MyQLabel(QLabel):
    button_clicked_signal = QtCore.pyqtSignal()

    def mouseReleaseEvent(self, QMouseEvent):
        self.button_clicked_signal.emit()

    def connect_customized_slot(self, func):
        self.button_clicked_signal.connect(func)

    def paintEvent(self, event):  # 绘制重写
        line = QLinearGradient(QPoint(0, 0), QPoint(1920, 1080))
        line.setColorAt(0, Qt.black)
        line.setColorAt(1, Qt.red)
        painter = QPainter(self)
        painter.setBrush(line)
        rect2 = QRect(0, 0, 1920 - 1, 1080 - 1)
        painter.setPen(QColor(255, 255, 255))  # 画笔
        painter.drawRect(rect2)
        painter.drawEllipse(QRect(int(1920 / 2) - int(1080 / 2), 0, 1080 - 2, 1080 - 2))  # 圆
        painter.drawLine(int(1920 / 2), 0, int(1920 / 2), 1080)
        painter.drawLine(0, int(1080 / 2), 1920, int(1080 / 2))


class MainWindow(QtWidgets.QMainWindow, MainWindowMouseKey):

    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)
        self.runQthread = None
        self.deepQthread = None
        # 定义字符
        self.hello = ["Hallo Welt", "Hei maailma", "Hola Mundo", "Привет мир", "Hello world"]

        # 添加槽链接[[
        self.pushButton.clicked.connect(self.magic)
        self.reseTrackerBut.clicked.connect(self.reseTrackerButClik)
        self.toolButton.clicked.connect(self.selectFileClik)
        self.hikcambut.clicked.connect(self.hikcambutClik)
        self.hikcamhisitory.clicked.connect(self.hikcamhisitoryClik)
        self.clearbut.clicked.connect(self.clearbutClik)

        self.dateEdit.setDate(QDate.currentDate())
        self.timeEdit.setTime(QTime.currentTime())

        self.historycombox.currentIndexChanged.connect(lambda: self.on_combobox_func(self.historycombox))
        self.on_combobox_func(self.historycombox)

        self.initData()

        self.m_label = MyQLabel()
        self.m_label.connect_customized_slot(self.labelClik)

        self.horizontalSlider.valueChanged.connect(self.valuechange)

    def valuechange(self):
        print("current slider value=%s" % self.horizontalSlider.value())
        size = self.horizontalSlider.value()
        self.runQthread.fpsPlayNum10 = size
        print(size)

    def on_combobox_func(self, combobox):
        print('select', combobox.currentIndex())
        qt = QTime(QTime.currentTime().hour(), 0)
        match combobox.currentIndex():
            case 0:
                qt = QTime(QTime.currentTime().hour() - 1, 0)
            case 1:
                qt = QTime(QTime.currentTime().hour() - 2, 0)
            case 2:
                qt = QTime(QTime.currentTime().hour() - 3, 0)
            case 3:
                qt = QTime(QTime.currentTime().hour() - 4, 0)
            case 4:
                qt = QTime(15, 0)
            case 5:
                qt = QTime(16, 0)
            case 6:
                qt = QTime(17, 0)
            case 7:
                qt = QTime(18, 0)

        self.timeEdit.setTime(qt)

    def clearbutClik(self):
        print('clearbutClik')
        self.deepQthread.resetYoloDetector()
        self.runQthread.setVideoPath(None)
        time.sleep(3)
        print('重新开始')

    def hikcamhisitoryClik(self):
        time_str = self.timeEdit.time().toString('hh:mm:ss')
        date_str = self.dateEdit.date().toString('yyyy-MM-dd')
        print(f'Date: {date_str}, Time: {time_str}')
        qTime = QTime(self.timeEdit.time())
        qDate = QDate(self.dateEdit.date())

        tm = datetime(qDate.year(), qDate.month(), qDate.day(), qTime.hour(), qTime.minute(), qTime.second())
        self.runQthread.makeHikHostoryByTm(tm)
        self.deepQthread.resetYoloDetector()

    def hikcambutClik(self):
        url = "rtsp://admin:Hik123456@192.168.31.212/Streaming/Channels/2"
        self.pushSelectFile(url)
        pass

    def labelClik(self):
        print('labelClik')
        pass

    def show_frame_pic(self, arr):
        showFrame = arr[0]
        qImage = QImage(showFrame.data, showFrame.shape[1], showFrame.shape[0], QImage.Format_RGB888)
        self.capframe.setPixmap(QPixmap.fromImage(qImage))

    def showDeepFrame(self, arr):
        showFrame = arr[0]
        qImage = QImage(showFrame.data, showFrame.shape[1], showFrame.shape[0], QImage.Format_RGB888)
        self.deepframe.setPixmap(QPixmap.fromImage(qImage))

    def send_frame(self, value):
        # self.label.setText(value)
        pass

    def initData(self):
        self.deepQthread = VideoDeepQthread()

        model_name = 'D:\\ultralytics-main\\runs\detect\\train15\weights\\best.onnx'
        self.deepQthread.set_start_config(
            model_name=model_name,
            confidence_threshold=0.1,
            iou_threshold=0.15)
        self.deepQthread.showDeepFrame.connect(self.showDeepFrame)
        self.deepQthread.start()

        self.runQthread = VideoRunQThread()
        self.runQthread.send_info.connect(self.send_frame)
        self.runQthread.show_pic.connect(self.show_frame_pic)
        self.runQthread.sendFrameInfo.connect(self.deepQthread.sendFrameInfo)
        self.runQthread.start()

    def pushSelectFile(self, value):
        self.deepQthread.resetYoloDetector()
        self.runQthread.setVideoPath(value)

    def selectFileClik(self):

        vid_fm = (".avi", ".mp4")
        file_list = " *".join(vid_fm)
        file_name, _ = QtWidgets.QFileDialog.getOpenFileName(self, "choose an image or video file", "./data",
                                                             f"Files({file_list})")
        if file_name:
            # self.pushSelectFile('D:/pythonscore/UIyolov8/Lesson_01/doorsheep.mp4')
            self.pushSelectFile(file_name)

            pass

    def reseTrackerButClik(self):
        # self.deepQthread.resetYoloDetector()
        # self.runQthread.setVideoPath(None)
        pass

    def magic(self):

        self.runQthread.pause_process = not self.runQthread.pause_process
        self.deepQthread.pause_process = self.runQthread.pause_process
        cframe = cv2.resize(self.runQthread.selectROIFrame, (500, 300))
        rect = cv2.selectROI(cframe, showCrosshair=True)

        print(rect)
        pass


# pyside6-uic mainwindow.ui > ui_mainwindow.py


# from PyQt5.QtCore import QRect, Qt, QCoreApplication, QMetaObject
# from PyQt5.QtWidgets import QToolButton, QPushButton, QLabel, QWidget

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()

    sys.exit(app.exec())
