
import time

import cv2
from PyQt5.QtCore import QThread, pyqtSignal

from datetime import datetime, timedelta
from dele.fps_mc import FpsMc


class HostoryRunQthread(QThread):
    sendFrameInfo = pyqtSignal(list)
    send_info = pyqtSignal(str)
    show_pic = pyqtSignal(object)
    show_frame_txt=pyqtSignal(str)
    send_video_info = pyqtSignal(str)


    def __init__(self):
        super(HostoryRunQthread, self).__init__()
        self.pause_process=False
        self.selectROIFrame=None
        self.showMaskFrame=False
        self.changeVideUrlAndSendToDeep=False
        self.roiRect=None
        self.cap=None
        self.frame_height=0
        self.frame_width  =0
        self.CacheWaitArr=[]
        self.CacheNum10=10
        self.fpsPlayNum10 = 100.0
        self.fpsMc = FpsMc()
        self.showRoiRectLine=False
        self.showProgressTxt=False
        self.hostoryStrtTm=datetime(2023, 1, 1, 1, 1, 1)
        self.object_detector = cv2.createBackgroundSubtractorMOG2(history=500, varThreshold=40, detectShadows=True)

    def setRoiRect(self,value):
        self.roiRect=value

        pass
    def filter_img(self, frame):
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
        _, thresh = cv2.threshold(frame, 20, 255, cv2.THRESH_BINARY)
        thresh = cv2.erode(thresh, kernel, iterations=2)
        dilated = cv2.dilate(thresh, kernel, iterations=2)

        return dilated
    def setVideoPath(self, url):
        self.pause_process=True
        self.cap = cv2.VideoCapture(url)
        if self.cap.isOpened():
            self.frame_width = self.cap.get(cv2.CAP_PROP_FRAME_WIDTH)
            self.frame_height = self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
            self.send_video_info.emit('w:'+str(self.frame_width)+'h:'+str(self.frame_height))
            self.pause_process = False
            self.roiRect = None
            self.changeVideUrlAndSendToDeep = True
        else:
            print('重新设置视频路径',url)


    def playNext10sFun(self):
        print('playNext10sFun')
        if self.cap.isOpened():
            print(self.cap.get(cv2.CAP_PROP_POS_FRAMES))
            self.cap.set(cv2.CAP_PROP_POS_FRAMES,100.0)
            print(self.cap.get(cv2.CAP_PROP_POS_FRAMES))



        pass


    # def exit(self):
    #     super().exit()
    #     self.cap.release()

        
    def makeHikHostoryByTm(self,tm):
        tm = datetime(2023, 10, 14, 23, 19, 0)
        self.cap = None
        cv2.waitKey(1000)

        self.hostoryStrtTm=tm
        self.pause_process=True


        self.cap = self.makeHistoryHikCamByData(tm)


        print('self.cap.isOpened()',self.cap.isOpened())



        if self.cap.isOpened():
            self.frame_width = self.cap.get(cv2.CAP_PROP_FRAME_WIDTH)
            self.frame_height = self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
            self.pause_process = False
            self.roiRect = None
            self.changeVideUrlAndSendToDeep=True
        else:
            print('重新设置视频为监控时时')

    def makeHistoryHikCamByData(self, tm):
        # tm参数为指定时间，为空就是一个小时钱的数据
        base_time = datetime.now()
        base_time += timedelta(hours=-8)
        end_time = base_time + timedelta(minutes=-1)
        start_time = tm + timedelta(hours=-8)

        print('开始的时间', start_time)
        startStr = start_time.strftime("%Y%m%dt%H%M%Sz")
        endStr = end_time.strftime("%Y%m%dt%H%M%Sz")
        print(startStr, endStr)
        url = 'rtsp://admin:Hik123456@192.168.31.212/Streaming/tracks/2?starttime=' + startStr + '&endtime=' + endStr
        print(url)
        cap = cv2.VideoCapture(url)


        return cap
    def mathToDeep(self,baseFrame,rectFrame,mask,roiRect):
        contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        detections = []
        for contour in contours:
            if cv2.contourArea(contour) < 25:
                continue
            (x, y, w, h) = cv2.boundingRect(contour)
            detections.append([x, y, w, h])

        self.CacheWaitArr.append([baseFrame,roiRect])
        if len(detections) > 0 or  self.changeVideUrlAndSendToDeep==True:
            self.changeVideUrlAndSendToDeep = False
            # 检测到场景动态将缓存帧推到进程中 从排前面的开始
            if len(self.CacheWaitArr) > 1:
                print('一次推送', len(self.CacheWaitArr))
            while len(self.CacheWaitArr) > 0:
                self.sendFrameInfo.emit(self.CacheWaitArr[0])
                del self.CacheWaitArr[0]
        else:
            if len(self.CacheWaitArr) > self.CacheNum10:
                del self.CacheWaitArr[0]

    def drawVideProgress(self, frame, str):
        (tx,ty,_)=frame.shape

        frame= cv2.putText(frame, str, (50, tx-50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
        return cv2.putText(frame, str, (50, tx-50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 1, cv2.LINE_AA)

    def showProgress(self,value):
        self.showProgressTxt=value
        pass
    def sendToUiPanle(self,frame,cap):
        if self.showProgressTxt:
            countNUm =  cap.get(cv2.CAP_PROP_FRAME_COUNT)
            if countNUm > 1:
                tempStr = str(int( cap.get(cv2.CAP_PROP_POS_FRAMES))) + '/' + str(int(countNUm))
                frame = self.drawVideProgress(frame, tempStr)

        self.show_pic.emit(cv2.resize(frame, (500, 350)))

        if cap and cap.isOpened():
            curNum = cap.get(cv2.CAP_PROP_POS_FRAMES)
            fpsNum = cap.get(cv2.CAP_PROP_FPS)
            kk = self.hostoryStrtTm + timedelta(seconds=int(curNum / fpsNum))
            self.show_frame_txt.emit(str(kk))


    def run(self):

        time.sleep(1)

        while True:
            tm=time.time()

            if self.pause_process:
                time.sleep(1)
                continue
            if self.cap:
                print(self.cap.isOpened())

            if self.cap and self.cap.isOpened():
                print(self.cap.get(cv2.CAP_PROP_POS_FRAMES))
                fps = self.cap.get(cv2.CAP_PROP_FPS)  # 计算视频的帧率
                # print(fps)
                # print(self.cap.get(cv2.CAP_PROP_POS_FRAMES),self.cap.get(cv2.CAP_PROP_FRAME_COUNT))
                ret, capframe = self.cap.read()
                if ret:
                    # 初始限制视频的尺寸
                    baseFrame = cv2.resize(capframe, (1000, 700))
                    self.selectROIFrame=baseFrame

                    if self.roiRect != None:
                        (x, y, w, h) = self.roiRect
                        rectFrame = baseFrame[int(y * baseFrame.shape[0]): int(h * baseFrame.shape[0]), int(x * baseFrame.shape[1]):int(w * baseFrame.shape[1])]
                        mask = self.object_detector.apply(rectFrame)
                    else:
                        mask = self.object_detector.apply(baseFrame)


                    mask = self.filter_img(mask)
                    if self.roiRect != None:
                        self.mathToDeep(baseFrame,rectFrame, mask,self.roiRect)
                        pass

                    showFrame=baseFrame
                    self.fpsMc.showFps(showFrame,tx=150,ty=25,scaleFont=1.7)
                    if self.roiRect !=  None and self.showRoiRectLine:
                        (x,y,w,h)=self.roiRect
                        cv2.rectangle(showFrame, (int(x * showFrame.shape[1]), int(y *showFrame.shape[0])), (int(w * showFrame.shape[1]), int(h *showFrame.shape[0])), (255, 0, 0), 1)
                    if self.showMaskFrame:
                        if self.roiRect != None:
                            tempmask = cv2.merge((mask, mask, mask))
                            (x, y, w, h) = self.roiRect
                            tx=(int(x * showFrame.shape[1]))
                            ty=(int(y * showFrame.shape[0]))
                            showFrame = cv2.resize(baseFrame, (baseFrame.shape[1], baseFrame.shape[0]))
                            showFrame[ty:tempmask.shape[0]+ty,tx:tempmask.shape[1]+tx]=tempmask[0:tempmask.shape[0],0:tempmask.shape[1]]



                            self.sendToUiPanle(showFrame,self.cap)

                        else:
                            mask = cv2.resize(mask, (500, 350))
                            tempImg = cv2.merge((mask, mask, mask))

                            self.sendToUiPanle(tempImg,self.cap)

                    else:

                        self.sendToUiPanle(showFrame,self.cap)

                waitTm = time.time() - tm
                waitTm = max(0, ( 1.0/self.fpsPlayNum10-waitTm))
                time.sleep(waitTm)

            else:
                time.sleep(1)



