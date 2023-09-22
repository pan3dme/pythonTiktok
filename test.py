import sys
from datetime import datetime
import cv2
import numpy as np
from PyQt5.QtCore import QEvent, Qt, QTimer, pyqtSignal, QPoint, QRect, QDate, QTime
from PyQt5.QtGui import QPixmap, QPainter, QLinearGradient, QColor, QImage
from Lesson_01.read_record_video import ReadRecordVideo
from Lesson_01.ui_mainwindow import Ui_MainWindow
from Lesson_01.video_deep_qthread import VideoDeepQthread
from PyQt5 import QtWidgets
from Lesson_01.video_run_qthread import VideoRunQThread

class MainWindow(QtWidgets.QMainWindow,Ui_MainWindow):

    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)
        self.writerVideoFile = cv2.VideoWriter("out/ccav002.mp4", cv2.VideoWriter_fourcc(*'mp4v'), 10.0,
                                               (500, 500))

        self.runQthread = None
        self.deepQthread = None
        self.readRecordVideo = None

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

        self.dateEdit.setDate(QDate.currentDate())
        self.timeEdit.setTime(QTime.currentTime())

        self.historycombox.currentIndexChanged.connect(lambda: self.on_combobox_func(self.historycombox))

    def readVideoButClik(self):
        vid_fm = (".txt")
        file_list = " *".join(vid_fm)
        file_name, _ = QtWidgets.QFileDialog.getOpenFileName(self, "choose an image or video file", "./out",
                                                             f"Files({file_list})")
        if file_name:
            self.deepQthread.pause_process=True
            self.runQthread.pause_process=True
            self.readRecordVideo=ReadRecordVideo()
            self.readRecordVideo.setFileUrl(file_name)
            self.readRecordVideo.showRecordpic.connect(self.showDeepFrame)
            self.readRecordVideo.start()




            pass
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
    def valuechange(self):
        print("current slider value=%s" % self.horizontalSlider.value())
        size = self.horizontalSlider.value()
        self.runQthread.fpsPlayNum10=size
        print(size)

    def on_combobox_func(self, combobox):
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
        self.runQthread.pause_process = True
        self.deepQthread.pause_process = True

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
    def send_video_info(self, value):
        self.videoinfolabel.setText(value)
        pass
    def show_frame_pic(self, value):
        qImage = QImage(value.data, value.shape[1], value.shape[0], QImage.Format_RGB888)
        self.capframe.setPixmap(QPixmap.fromImage(qImage))

    def showDeepFrame(self, value):
        self.saveRecordVideoByFrame(value)
        qImage = QImage(value.data, value.shape[1], value.shape[0], QImage.Format_RGB888)
        self.deepframe.setPixmap(QPixmap.fromImage(qImage))




    def send_frame(self,value):
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
        self.deepQthread.saveRecordVideoByFrame.connect(self.saveRecordVideoByFrame)
        self.deepQthread.start()

        self.runQthread = VideoRunQThread()
        self.runQthread.send_info.connect(self.send_frame)
        self.runQthread.show_pic.connect(self.show_frame_pic)

        self.runQthread.send_video_info.connect(self.send_video_info)
        self.runQthread.sendFrameInfo.connect(self.deepQthread.sendFrameInfo)

        self.runQthread.start()



    def saveRecordVideoByFrame(self,vframe):
        print('saveRecordVideoByFrame')
        vframe = np.zeros((500, 500, 3), np.uint8)
        self.writerVideoFile.write(np.zeros((500, 500, 3), np.uint8))
        cv2.imwrite( 'out/ccav.jpg', vframe)
        print('写拉文件')


    def pushSelectFile(self,value):
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

    def makeHikCam(self):
        videoBaseUrl = "D:/pythonscore/YOLOv8-DeepSort-PyQt-GUI-main/data/hikCam_001.MP4"
        return cv2.VideoCapture(videoBaseUrl)

    def runTemp(self):
        cap = self.makeHikCam()

        sendTm = 0
        if cap.isOpened():
            while cap.isOpened():
                ret, capframe = cap.read()
                if ret:
                    capframe = cv2.resize(capframe, (500, 500))
                    # capframe = np.zeros((500, 500, 3), np.uint8)
                    cv2.imshow('abc', capframe)

                    self.writerVideoFile.write(capframe)

                keyCode = cv2.waitKey(10)
                if keyCode == ord("q"):
                    break


        else:
            print('摄像头出错')

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    window.runTemp()
    # window.pushSelectFile('D:/pythontiktok/data/hikCam_001.mp4')

