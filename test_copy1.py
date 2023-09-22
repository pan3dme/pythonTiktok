



import cv2
import numpy as np
from PyQt5.QtCore import QObject


class CamWriteVideo(QObject):
    def __init__(self,onnName):
        super().__init__()
        self.writerVideoFile = cv2.VideoWriter("out/ccav006.mp4", cv2.VideoWriter_fourcc(*'mp4v'), 10.0,
                                               (500, 500))

    def makeHikCam(self):
        videoBaseUrl = "D:/pythonscore/YOLOv8-DeepSort-PyQt-GUI-main/data/hikCam_001.MP4"
        return  cv2.VideoCapture(videoBaseUrl)


    def backMsg(self , msg):
        print('backmsg')
        print(msg)

    def makeGoproCam(self):
        videoBaseUrl ="rtmp://192.168.31.36:1935/live/test"
        return cv2.VideoCapture(videoBaseUrl)

    testGoproCamT=0
    def run(self):


        cap = self.makeHikCam()




        sendTm=0
        if cap.isOpened():
            while cap.isOpened():
                ret, capframe = cap.read()
                if ret:
                    capframe=cv2.resize(capframe, (500, 500))
                    capframe = np.zeros((500,500, 3), np.uint8)
                    cv2.imshow('abc',capframe)

                    self.writerVideoFile.write(capframe)



                keyCode = cv2.waitKey(10)
                if keyCode == ord("q"):
                    break


        else:
            print('摄像头出错')



if __name__ == '__main__':
    mainWindow = CamWriteVideo('abc')


    mainWindow.run()






