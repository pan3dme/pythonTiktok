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

from Lesson_01.aliyunlinkitmodel import AliyunLinkModel
from Lesson_01.gopro_video import GoproVideo
from Lesson_01.mainmousekey import MainWindowMouseKey
from Lesson_01.read_record_video import ReadRecordVideo
from Lesson_01.ui_mainwindow import Ui_MainWindow
from Lesson_01.video_deep_qthread import VideoDeepQthread

from PyQt5 import QtWidgets, QtCore

from Lesson_01.video_run_qthread import VideoRunQThread


class MainWindow(QtWidgets.QMainWindow,Ui_MainWindow):

    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)
        self.runQthread=None
        self.deepQthread=None
        self.readRecordVideo=None
        self.writerVideoFile =None
        self.goproVideo=None




        self.pushButton.clicked.connect(self.magic)
        self.reseTrackerBut.clicked.connect(self.reseTrackerButClik)
        self.toolButton.clicked.connect(self.selectFileClik)
        self.hikcambut.clicked.connect(self.hikcambutClik)
        self.hikcamhisitory.clicked.connect(self.hikcamhisitoryClik)
        self.readVideoBut.clicked.connect(self.readVideoButClik)
        self.clearbut.clicked.connect(self.clearbutClik)
        self.roiBut.clicked.connect(self.selectROIButClik)
        self.checkBoxShowRoiRect.clicked.connect(self.checkBoxShowRoiRectClik)
        self.checkBoxShowMaskFrame.clicked.connect(self.checkBoxShowMaskFrameClik)
        self.checkBoxSaveVideo.clicked.connect(self.checkBoxSaveVideoClik)
        self.capStopCheck.clicked.connect(self.capStopCheckClik)
        self.deepStopCheck.clicked.connect(self.deepStopCheckClik)
        self.showgoprovideo.clicked.connect(self.showgoprovideoClik)
        self.showGoproSound.clicked.connect(self.showGoproSoundClik)
        self.showprogressbar.clicked.connect(self.showprogressbarClik)





        self.dateEdit.setDate(QDate.currentDate())
        self.timeEdit.setTime(QTime.currentTime())

        self.saveFileName.setText( datetime.now().strftime("%Y%m%dt%H%M")+'.mp4')

        self.historycombox.currentIndexChanged.connect(self.on_combobox_func)
        self.on_combobox_func()

        self.horizontalSlider.valueChanged.connect(self.horizontalSliderChange)
        self.waitDeepLenSlide.valueChanged.connect(self.waitDeepLenSlideChange)


        self.selectCamcombox.currentIndexChanged.connect(self.selectCamcomboxfunc)
        self.selectCamcomboxfunc()

        self.initData()

    def showprogressbarClik(self):
        isDown = self.showprogressbar.isChecked()

        self.runQthread.showProgress(isDown)
        print(isDown)
        pass
    def showGoproSoundClik(self):
        isDown = self.showGoproSound.isChecked()
        if self.goproVideo is not None:
            if isDown:
                self.goproVideo.setVolume(0)
                print('播放声音')

            else:
                self.goproVideo.setVolume(1)
                pass

    def showgoprovideoClik(self):

        isDown=self.showgoprovideo.isChecked()
        print('showgoprovideoClik', isDown)
        if isDown:
            if self.goproVideo is None:
                print('创建进程GoproVideo')
                self.goproVideo = GoproVideo()
                # 'D:\pythontiktok\data\sound.mp4'
                # 'rtmp://192.168.31.35:1935/live/test'
                self.goproVideo.setVideoUrl('rtmp://192.168.31.35:1935/live/test')
                self.goproVideo.showMediaFrame.connect(self.showMediaFrame)
                self.goproVideo.start()



        else:
            if self.goproVideo is not None:

                 pass





        pass
    def stopAllQthread(self):
        print('清理所有进程')
        self.runQthread.pause_process = True
        self.deepQthread.resetYoloDetector()

        if self.readRecordVideo is not None:
            self.readRecordVideo.pause_process=True
            self.readRecordVideo.clearRecord()


        pass

    def readVideoButClik(self):
        vid_fm = (".txt")
        file_list = " *".join(vid_fm)
        file_name, _ = QtWidgets.QFileDialog.getOpenFileName(self, "choose an image or video file", "./out",
                                                             f"Files({file_list})")
        if file_name:
            self.stopAllQthread()

            self.readRecordVideo=ReadRecordVideo()
            self.readRecordVideo.setFileUrl(file_name)
            self.readRecordVideo.showRecordpic.connect(self.show_frame_pic)
            self.readRecordVideo.showRightRoleArr.connect(self.showRightRoleArr)
            self.readRecordVideo.start()


            pass
        pass
    def deepStopCheckClik(self):
        self.deepQthread.pause_process=self.deepStopCheck.isChecked()
        print(self.deepStopCheck.isChecked())
        pass
    def capStopCheckClik(self):

        self.runQthread.pause_process = self.capStopCheck.isChecked()
        print(self.capStopCheck.isChecked(),self.runQthread.pause_process )
        pass
    def checkBoxSaveVideoClik(self):
        self.deepQthread.saveVideo=self.checkBoxSaveVideo.isChecked()
        pass
    def checkBoxShowMaskFrameClik(self):
        self.runQthread.showMaskFrame = self.checkBoxShowMaskFrame.isChecked()

    def checkBoxShowRoiRectClik(self):
        # print('select', self.checkBoxShowRoiRect.isChecked())
        self.runQthread.showRoiRectLine=self.checkBoxShowRoiRect.isChecked()

        pass
    def selectROIButClik(self):

        cframe = cv2.resize(self.runQthread.selectROIFrame, (500, 300))
        (x,y,w,h) = cv2.selectROI('cframe', cframe, False, False)



        print((x/500,y/300,w/500,h/300))
        self.runQthread.setRoiRect((x/500,y/300,(x+w)/500,(y+h)/300))
        self.checkBoxShowRoiRect.setChecked(True)
        self.runQthread.showRoiRectLine = True



        pass
    def waitDeepLenSlideChange(self):
        self.runQthread.waitDeepMaxLen=self.waitDeepLenSlide.value()
        self.waitdeepnumtxt.setText("%s张" % self.waitDeepLenSlide.value())

    def horizontalSliderChange(self):
        self.runQthread.fpsPlayNum10=self.horizontalSlider.value()
        self.fpsnumtxt.setText("%sfps" % self.horizontalSlider.value())


    def selectCamcomboxfunc(self):
        combobox = self.selectCamcombox

        if combobox.currentIndex()==0:
            AliyunLinkModel.get_instance().hikUrl = AliyunLinkModel.get_instance().urlArr[0]
        else:
            AliyunLinkModel.get_instance().hikUrl = AliyunLinkModel.get_instance().urlArr[1]

        print(AliyunLinkModel.get_instance().hikUrl)

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

    def clearbutClik(self):
        print('clearbutClik')
        self.stopAllQthread()

    def hikcamhisitoryClik(self):
        self.stopAllQthread()
        time_str = self.timeEdit.time().toString('hh:mm:ss')
        date_str = self.dateEdit.date().toString('yyyy-MM-dd')
        print(f'Date: {date_str}, Time: {time_str}')
        qTime = QTime(self.timeEdit.time())
        qDate = QDate(self.dateEdit.date())

        tm = datetime(qDate.year(), qDate.month(), qDate.day(), qTime.hour(), qTime.minute(), qTime.second())
        self.runQthread.makeHikHostoryByTm(tm)
        self.deepQthread.resetYoloDetector()


    def hikcambutClik(self):

        # url="rtsp://"+AliyunLinkModel.get_instance().hikUrl+"/Streaming/Channels/2"
        url="rtsp://"+AliyunLinkModel.get_instance().hikUrl+"/Streaming/Channels/1?transport=tcp"
        self.pushSelectFile(url)
        pass
    def send_video_info(self, value):
        self.videoinfolabel.setText(value)
        pass
    def showWaitItemLen(self, value):
        if self.runQthread is not  None:
            self.runQthread.setDeepWaitLen(value)
        pass
    def showRightRoleArr(self, value):
        # print('showRightRoleArr',value)
        AliyunLinkModel.get_instance().pingLink(len(value)+10)
        pass
    def show_frame_pic(self, value):
        qImage = QImage(value.data, value.shape[1], value.shape[0], QImage.Format_BGR888)
        self.capframe.setPixmap(QPixmap.fromImage(qImage))



    def showMediaFrame(self, value):

        img, t = value
        qimg = QImage(bytes(img.to_bytearray()[0]), img.get_size()[0], img.get_size()[1],
                           QImage.Format_RGB888)
        qimg=qimg.scaled(500, 350, QtCore.Qt.KeepAspectRatio)
        self.deepframe.setPixmap(QPixmap.fromImage(qimg))


    def showDeepFrame(self, value):

        qImage = QImage(value.data, value.shape[1], value.shape[0], QImage.Format_BGR888)

        self.deepframe.setPixmap(QPixmap.fromImage(qImage))




    def send_frame(self,value):
        # self.label.setText(value)
        pass

    def initData(self):
        self.deepQthread = VideoDeepQthread()
        model_name = 'D:\\ultralytics-main\\runs\detect\\train15\weights\\best.onnx'
        model_name = 'D:\pythonscore\YOLOv8-DeepSort-PyQt-GUI-main\weights\detection\yolov8n.onnx'
        self.deepQthread.set_start_config(
            model_name=model_name,
            confidence_threshold=0.1,
            iou_threshold=0.15)
        self.deepQthread.showDeepFrame.connect(self.showDeepFrame)
        self.deepQthread.showRightRoleArr.connect(self.showRightRoleArr)
        self.deepQthread.showWaitItemLen.connect(self.showWaitItemLen)
        self.deepQthread.saveRecordVideoByFrame.connect(self.saveRecordVideoByFrame)
        self.deepQthread.saveRecordTxtByStr.connect(self.saveRecordTxtByStr)
        self.deepQthread.start()

        self.runQthread = VideoRunQThread()
        self.showprogressbar.setChecked(True)
        self.showprogressbarClik()
        self.runQthread.send_info.connect(self.send_frame)
        self.runQthread.show_pic.connect(self.show_frame_pic)

        self.runQthread.send_video_info.connect(self.send_video_info)
        self.runQthread.sendFrameInfo.connect(self.deepQthread.sendFrameInfo)




        self.runQthread.start()

        AliyunLinkModel.get_instance()



    saveFileShape=None
    def saveRecordTxtByStr(self,value):
        filename=self.saveFileName.text().replace('.mp4','.txt')
        strUrl = "out/"+filename
        with open(strUrl, 'a') as f:
            f.write(value)

    def saveRecordVideoByFrame(self,vframe):

        filename = self.saveFileName.text()
        (th, tw, tn) = vframe.shape
        if self.writerVideoFile is None:
            self.saveFileShape=(th, tw, tn)
            self.writerVideoFile = cv2.VideoWriter("out/"+filename, cv2.VideoWriter_fourcc(*'mp4v'), 10.0,
                                                   (tw,th))
        else:
            (sh, sw, sn) = self.saveFileShape
            if not (sh== th and sw==tw):
                print('重新创建视频保存')
                self.writerVideoFile.release()
                self.writerVideoFile=None
                self.saveRecordVideoByFrame(vframe)

                return

        self.writerVideoFile.write(vframe)



    def pushSelectFile(self,value):
        print(value)
        self.stopAllQthread()
        self.deepQthread.resetYoloDetector()
        self.runQthread.setVideoPath(value)

    def selectFileClik(self):
        vid_fm = ( ".avi", ".mp4" )
        file_list = " *".join( vid_fm)
        file_name, _ = QtWidgets.QFileDialog.getOpenFileName(self, "choose an image or video file", "./data",
                                                             f"Files({file_list})")
        if file_name:
            self.pushSelectFile(file_name)
            pass

    def reseTrackerButClik(self):
        # self.deepQthread.resetYoloDetector()
        # self.runQthread.setVideoPath(None)
        pass
    def magic(self):

        self.runQthread.pause_process=not self.runQthread.pause_process
        self.deepQthread.pause_process=self.runQthread.pause_process

        pass

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    window.pushSelectFile('D:/pythontiktok/data/hikCam_001.mp4')
    sys.exit(app.exec())
