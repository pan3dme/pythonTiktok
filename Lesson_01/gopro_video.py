import time

import cv2
from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtGui import QImage
from ffpyplayer.player import MediaPlayer
class GoproVideo(QThread):
    showMediaFrame = pyqtSignal(object)

    def __init__(self):
        super(GoproVideo, self).__init__()

        self.threadFlag = True
        self.pause_process=False

        self.player = MediaPlayer(self.video_path)
        # self.player.set_output_pix_fmt((250,250))


    video_path = 'rtmp://192.168.31.35:1935/live/test'
    # video_path = 'D:\pythontiktok\data\sound.mp4'

    def playMedialPlayerSound(self):
        pass
    def distoy(self):
        self.exit()

    def run(self):
        time.sleep(1.0)

        while self.threadFlag:
            if self.pause_process is False:
                time.sleep(1./30.)
                frame,  val = self.player.get_frame()
                if frame is not None:
                    print(val)
                    self.showMediaFrame.emit(frame)
                else:
                    print('err')


            else:
                time.sleep(0.1)


