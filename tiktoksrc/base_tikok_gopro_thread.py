import cv2
from PyQt5.QtCore import QThread, pyqtSignal
import time

from ffpyplayer.player import MediaPlayer


class BaseTikTokGoproThred(QThread):
    def __init__(self):
        super(BaseTikTokGoproThred, self).__init__()

    def makeGoproCam(self):
        videoBaseUrl = "rtmp://192.168.31.36:1935/live/test"
        self.soundplayer = MediaPlayer(videoBaseUrl)
        return cv2.VideoCapture(videoBaseUrl)

    soundplayer=None
    goproCap=None
    curGoproFrame=None
    def readGoproVideo(self):
        if self.goproCap is None:
            self.testGoproCamTM = time.time()
            print('请求一次Gopro的流')
            self.goproCap = self.makeGoproCam()
            print('请求一次Gopro的流isOpened',self.goproCap.isOpened())

        if self.goproCap.isOpened():
            ret, frame = self.goproCap.read()
            audio_frame, val = self.soundplayer.get_frame()

            # print(audio_frame, val)

            if ret:
                self.curGoproFrame = frame
            else:
                print('goproRead出错')
        else:
            print('gopro不可用', time.time() - self.testGoproCamTM)
            if time.time() - self.testGoproCamTM > 20:
                self.goproCap = None;
        pass

    def run(self):
        while True:
            self.readGoproVideo()
            time.sleep(0.001)

