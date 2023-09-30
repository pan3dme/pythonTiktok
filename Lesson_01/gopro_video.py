import time

import cv2
from PyQt5.QtCore import QThread, pyqtSignal
from ffpyplayer.player import MediaPlayer
class GoproVideo(QThread):
    showDeepFrame = pyqtSignal(object)

    def __init__(self):
        super(GoproVideo, self).__init__()
        self.threadFlag = True
        video_path='rtmp://192.168.31.35:1935/live/test'
        self.cap = cv2.VideoCapture(video_path)
        self.player = MediaPlayer(video_path)

        # self.cap = cv2.VideoCapture('D:/pythonscore/YOLOv8-DeepSort-PyQt-GUI-main/data/hikCam_001.MP4')
        self.pause_process = True

    def run(self):
        time.sleep(1.0)
        while self.threadFlag:


            if self.pause_process:
                cap = self.cap
                print(cap.isOpened())
                if cap.isOpened():
                    tm = time.time()
                    capFps = self.cap.get(cv2.CAP_PROP_FPS)
                    capPos = self.cap.get(cv2.CAP_PROP_POS_FRAMES)


                    ret, baseframe = cap.read()
                    if ret:
                        # cv2.imshow('abc', baseframe)
                        print('gopro run')
                        self.showDeepFrame.emit(cv2.resize(baseframe, (500, 350)))

                    tm=(time.time() - tm)+(1.0/50.0)
                    if tm<1/capFps:
                        time.sleep(1/capFps-tm)

                    print(tm,capFps,capPos)


                else:
                    time.sleep(1 / 20)
                    print('cap ie error')







            else:
                time.sleep(1.0)


