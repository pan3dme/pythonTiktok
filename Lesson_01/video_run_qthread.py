import json
import time

import cv2
from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtGui import QImage
from datetime import datetime, timedelta
from dele.fps_mc import FpsMc


class VideoRunQThread(QThread):
    sendFrameInfo = pyqtSignal(list)
    send_info = pyqtSignal(str)
    show_pic = pyqtSignal(QImage)

    def __init__(self):
        super(VideoRunQThread, self).__init__()
        self.pause_process=False
        self.cap=None
        self.CacheWaitArr=[]
        self.CacheNum10=10
        self.fpsPlayNum10 = 10.0
        self.fpsMc = FpsMc()
        self.object_detector = cv2.createBackgroundSubtractorMOG2(history=500, varThreshold=40, detectShadows=True)

    def filter_img(self, frame):
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
        _, thresh = cv2.threshold(frame, 20, 255, cv2.THRESH_BINARY)
        thresh = cv2.erode(thresh, kernel, iterations=2)
        dilated = cv2.dilate(thresh, kernel, iterations=2)

        return dilated
    def setVideoPath(self, url):
        self.pause_process=True
        self.cap = None
        self.cap = cv2.VideoCapture(url)
        self.pause_process = False

    def makeHikHostoryByTm(self,tm):
        # tm = datetime(2023, 9, 16, 18, 24, 40)
        self.pause_process=True
        self.cap=None
        self.cap = self.makeHistoryHikCamByData(tm)
        self.pause_process = False

    def makeHistoryHikCamByData(self,tm):
        # tm参数为指定时间，为空就是一个小时钱的数据
        base_time = datetime.now()
        base_time += timedelta(hours=-8)
        end_time = base_time + timedelta(minutes=-1)
        start_time =tm+ timedelta(hours=-8)

        print('开始的时间',start_time)
        startStr = start_time.strftime("%Y%m%dt%H%M%Sz")
        endStr = end_time.strftime("%Y%m%dt%H%M%Sz")
        print(startStr, endStr)
        url = 'rtsp://admin:Hik123456@192.168.31.212/Streaming/tracks/2?starttime='+startStr+'&endtime='+endStr
        print(url)
        cap = cv2.VideoCapture(url)
        return cap
    def mathToDeep(self,frame,mask):
        contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        detections = []
        for contour in contours:
            if cv2.contourArea(contour) < 25:
                continue
            (x, y, w, h) = cv2.boundingRect(contour)
            detections.append([x, y, w, h])

        self.CacheWaitArr.append([frame, frame])
        if len(detections) > 0:
            # 检测到场景动态将缓存帧推到进程中 从排前面的开始
            if len(self.CacheWaitArr) > 1:
                print('一次推送', len(self.CacheWaitArr))
            while len(self.CacheWaitArr) > 0:
                self.sendFrameInfo.emit(self.CacheWaitArr[0])
                del self.CacheWaitArr[0]
        else:
            if len(self.CacheWaitArr) > self.CacheNum10:
                del self.CacheWaitArr[0]


    def run(self):

        time.sleep(1)

        while True:
            tm=time.time()
            if self.pause_process:
                time.sleep(1)
                continue
            if self.cap and self.cap.isOpened():
                fps = self.cap.get(cv2.CAP_PROP_FPS)  # 计算视频的帧率
                # print(fps)
                # print(self.cap.get(cv2.CAP_PROP_POS_FRAMES),self.cap.get(cv2.CAP_PROP_FRAME_COUNT))
                ret, capframe = self.cap.read()
                if ret:
                    baseFrame = cv2.resize(capframe, (500,350))
                    rectFrame = cv2.resize(capframe, (500,350))

                    applymask = self.object_detector.apply(baseFrame)
                    mask = self.filter_img(applymask)

                    self.mathToDeep(rectFrame,mask)

                    show=baseFrame

                    self.fpsMc.showFps(show,tx=150,ty=25,scaleFont=0.7)

                    showImage = QImage(show.data, show.shape[1], show.shape[0], QImage.Format_RGB888)
                    self.show_pic.emit(showImage)

                skipNum = time.time() - tm
                skipNum = max(0, ( 1.0/self.fpsPlayNum10-skipNum))

                time.sleep(skipNum)


            else:
                time.sleep(1)



