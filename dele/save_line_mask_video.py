import os
from tkinter.messagebox import askyesno

import cv2
import numpy as np

from dele.base_draw_sample_role import BaseDrawSampleRole
from dele.base_save_labelme import BaseSaveLabelMe


class SaveLineMaskVideo(BaseDrawSampleRole):

    def __init__(self,filename):
        super().__init__(filename)
        self.object_detector = cv2.createBackgroundSubtractorMOG2(history=500, varThreshold=40, detectShadows=True)
        self.tikTokFle = None
        self.isWriteState = -1


    def filter_img(self,frame):
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
        _, thresh = cv2.threshold(frame, 20, 255, cv2.THRESH_BINARY)
        thresh = cv2.erode(thresh, kernel, iterations=2)
        dilated = cv2.dilate(thresh, kernel, iterations=2)

        return dilated

    def drawVide2File(self,frame,mask,size):
        w,h=size
        outMp4url = 'out/tiktok.mp4'
        if self.isWriteState==-1:
            if os.path.exists(outMp4url):
                if askyesno('重要提示', '是否覆盖' + outMp4url + '原来导出的数据'):
                    self.isWriteState=1
                else:
                    self.isWriteState=0
            else:
                print("文件不存在")

        if self.isWriteState == 1:
            if not self.tikTokFle:
               self.tikTokFle = cv2.VideoWriter('out/tiktok.mp4', cv2.VideoWriter_fourcc(*'mp4v'), 25.0,
                                              (w,h*2))
            img = np.zeros((h*2, w, 3), np.uint8)
            cv2.rectangle(img, (50,50), (150, 150), (0, 255, 0), -1)
            img[0:h, 0:w] = frame[0:h, 0:w]
            tempImg= cv2.merge([mask, mask, mask ])
            img[h:h+h, 0:w] =tempImg [0:h, 0:w]
            self.tikTokFle.write(img)
            cv2.imshow("img", img)



        pass
    def drawImgFoVdeoTiTok(self, showLine=True, scale=0.5):
        _baseSaveLabelMe = BaseSaveLabelMe('fuck')
        waitTm = 10;
        Size480_320 = (int(self.frame_width * scale), int(self.frame_height * scale))
        cap = self.cap
        while cap.isOpened():
            # print(int(cap.get(cv2.CAP_PROP_POS_FRAMES)), '/', int(cap.get(cv2.CAP_PROP_FRAME_COUNT)))
            ret, baseframe = cap.read()

            if ret:
                frame = baseframe
                if showLine:
                    video_pos = int(cap.get(cv2.CAP_PROP_POS_FRAMES))
                    if str(video_pos) in self.outkeyDic:
                        _labelmeXml = self.outkeyDic[str(video_pos)]
                        frame = self.draw_results(baseframe, _labelmeXml)

                applymask = self.object_detector.apply(cv2.resize(baseframe, Size480_320))
                # mask = self.filter_img(applymask)
                frame=cv2.resize(frame, Size480_320)
                cv2.imshow("read_img", self.baseData.showFps(frame))
                cv2.imshow("applymask",applymask)
                # cv2.imshow("mask",mask)
                self.drawVide2File(frame,applymask,Size480_320)

            if cap.get(cv2.CAP_PROP_POS_FRAMES) >= cap.get(cv2.CAP_PROP_FRAME_COUNT):
                break

            keyNum = cv2.waitKey(int(1000/25))


            if keyNum == ord("q"):
                break

