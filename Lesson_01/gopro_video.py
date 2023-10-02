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

        # self.player = MediaPlayer(self.video_path)
        # self.player.set_output_pix_fmt((250,250))


    # video_path = 'rtmp://192.168.31.35:1935/live/test'
    video_path = 'D:\pythontiktok\data\sound.mp4'
    player=None
    showVideoFrame=True
    def setVideoUrl(self,value):
        self.player = MediaPlayer(value)
    def setVolume(self,value):
        self.player.set_volume(value)
        pass
    def distoy(self):
        self.exit()

    def run(self):
        time.sleep(1.0)

        while self.threadFlag:
            tm = time.time()
            if self.showVideoFrame:
                frame, val = self.player.get_frame()
                if frame is not None:
                    self.showMediaFrame.emit(frame)
                else:
                    print('gopro frame err')




            tm = (time.time() - tm)
            tm=(1.0 / 29.0)-tm
            print('tm',tm)
            if tm>0:
                time.sleep(tm)



