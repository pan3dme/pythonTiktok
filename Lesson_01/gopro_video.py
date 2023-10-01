import time

import cv2
from PyQt5.QtCore import QThread, pyqtSignal
from ffpyplayer.player import MediaPlayer
class GoproVideo(QThread):
    showDeepFrame = pyqtSignal(object)

    def __init__(self):
        super(GoproVideo, self).__init__()

        self.threadFlag = True
        self.pause_process=False

        self.cap = cv2.VideoCapture(self.video_path)

    # video_path = 'rtmp://192.168.31.35:1935/live/test'
    video_path = 'D:\pythontiktok\data\sound.mp4'
    playerSound=None
    def playMedialPlayerSound(self):
        self.playerSound = MediaPlayer(self.video_path)

    def distoy(self):


        self.player.close_player()

        self.exit()

    def run(self):
        time.sleep(1.0)
        while self.threadFlag:
            if self.pause_process is False:
                cap = self.cap
                if cap.isOpened():
                    tm = time.time()
                    capFps = self.cap.get(cv2.CAP_PROP_FPS)
                    capPos = self.cap.get(cv2.CAP_PROP_POS_FRAMES)
                    ret, baseframe = cap.read()
                    if ret:
                        self.showDeepFrame.emit(cv2.resize(baseframe, (500, 350)))
                    else:
                        cap.release()

                    tm=(time.time() - tm)+(1.0/50.0)
                    if tm<1/capFps:
                        time.sleep(1/capFps-tm)
                    # print(capFps,capPos,tm)
                else:
                    cap.release()
                    time.sleep(1 / 20)
                    print('cap ie error')


            else:
                time.sleep(1.0)


