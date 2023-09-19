import json
import numpy as np

import dele.base_data
import cv2
import time
import os
import dele.base_Linkit_model
from tiktoksrc.base_tikok_gopro_thread import BaseTikTokGoproThred
from tiktoksrc.base_tiktok_deep_thread import BaseTokeDeepThread


class BaseTikTokVideo():
    def filter_img(self,frame):
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
        _, thresh = cv2.threshold(frame, 20, 255, cv2.THRESH_BINARY)
        thresh = cv2.erode(thresh, kernel, iterations=2)
        dilated = cv2.dilate(thresh, kernel, iterations=2)

        return dilated

    def fillet_arr(self,arr):
        for temp in arr:
            temp["bbox"] = temp["bbox"].tolist()
            (x,y,w,h)=self.curCapRoiRect
            temp["rect"] = [x,y,w,h]
        return str(json.dumps(arr))


    def makedir(self,dir_path):
        dir_path = os.path.dirname(dir_path)  # 获取路径名，删掉文件名
        bool = os.path.exists(dir_path)  # 存在返回True，不存在返回False
        if bool:
            pass
        else:
            os.makedirs(dir_path)

    def __init__(self,onnName='yolov8n.onnx'):

        self.writerFile = None
        os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"
        self.name = "BaseWriteVideo"

        self.CacheNum10 = 10
        self.CacheWaitArr = []

        conf_thr = 0.3
        iou_thr = 0.45



        model_name=onnName


        self.file_process_thread = BaseTokeDeepThread()
        self.file_process_thread.showFrame = cv2.imread("data/bus.jpg")  # 读取1.jpg图像
        self.file_process_thread.set_start_config(
            model_name=model_name,
            confidence_threshold=conf_thr,
            iou_threshold=iou_thr)

        self.file_process_thread.start()

        self.base_tiktok_gopro_thred=BaseTikTokGoproThred()
        # self.base_tiktok_gopro_thred.start()

        self.object_detector = cv2.createBackgroundSubtractorMOG2(history=500, varThreshold=40, detectShadows=True)

    def getType(self):
        idx= dele.base_Linkit_model.instance.selectID%5



        return  idx

    def drawTempFrame(self, capframe ,rect):
        file_process_thread = self.file_process_thread
        (x, y, w, h) = rect
        resized_img = capframe[y:h+y, x:w+x]
        applymask = self.object_detector.apply(resized_img)
        mask = self.filter_img(applymask)

        contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        needAdd=False
        for contour in contours:
            if cv2.contourArea(contour) < 100:
                continue
            else:
                needAdd = True

        self.CacheWaitArr.append([capframe, capframe[y:h+y, x:w+x]])

        if needAdd :
            # 检测到场景动态将缓存帧推到进程中 从排前面的开始
            if len(self.CacheWaitArr) > 1:
                print('一次推送', len(self.CacheWaitArr))
            while len(self.CacheWaitArr) > 0:
                file_process_thread.pushFrameToWaitArr(self.CacheWaitArr[0])
                del self.CacheWaitArr[0]
        else:
            # 超出预存的数据后将前面的帧推出
            if len(self.CacheWaitArr) > self.CacheNum10:
                del self.CacheWaitArr[0]

    writerFile=None

    isSaveFile=True
    outfileName=None
    def saveOutFileAndInfo(self,video_pos,baseframe,vframe,vinfo):
        if self.isSaveFile==False:
            return
        # 保存检测信息
        frame_height = self.curCapVideo.get(cv2.CAP_PROP_FRAME_HEIGHT)
        frame_width =  self.curCapVideo.get(cv2.CAP_PROP_FRAME_WIDTH)

        if self.writerFile is None:
            outMp4url = "out/" + self.outfileName + ".mp4"

            self.writerFile = cv2.VideoWriter(outMp4url, cv2.VideoWriter_fourcc(*'mp4v'), 25.0,
                                              (int(frame_width),int(frame_height)))

        self.writerFile.write(baseframe)
        strUrl = "out/" + self.outfileName + ".txt"
        addTextStr = str(video_pos) + "||" + self.fillet_arr(vinfo) + "\n"
        with open(strUrl, 'a') as f:
            f.write(addTextStr)

        pass
    def makeThreadWait(self,rect):
        (x, y, w, h) = rect
        file_process_thread = self.file_process_thread


        if len(file_process_thread.needShowFrameArr) > 0:
            self.saveFrameNum +=1
            video_pos, baseframe, vframe, vinfo = file_process_thread.needShowFrameArr[0]
            self.saveOutFileAndInfo(video_pos,baseframe,vframe,vinfo)
            baseframe[y:h + y, x:w + x] =vframe[0:h , 0:w]
            self.curDeesportFrame = baseframe
            del file_process_thread.needShowFrameArr[0]



    saveFrameNum = 0
    goproCap=None
    curCapframe=None
    curDeesportFrame=None
    curGoproFrame=None

    def drawToTiktokView(self):
        Size480_320 = (500, 350)

        titokImg = np.zeros((800, 500, 3), np.uint8)
        titokImg[:, :, 1] = np.ones([800, 500]) * 255

        showDeepSortFrame = dele.base_Linkit_model.instance.showDeepSortFrame
        showHikCameFrame = dele.base_Linkit_model.instance.showHikCameFrame
        ty=0
        if showHikCameFrame:
             titokImg[0:350, 0:500] = cv2.resize(self.curCapframe, Size480_320)[0:350, 0:500]
             ty=350

        if showDeepSortFrame:
            if self.curDeesportFrame is None:
                pass
            else:
                titokImg[0+ty:350+ty, 0:500] = cv2.resize(self.curDeesportFrame, Size480_320)[0:350, 0:500]
                ty = 350
            pass

        if self.base_tiktok_gopro_thred.curGoproFrame is None:
            pass
        else:
            ty = 350
            titokImg[0 + 350:350 + ty, 0:500] = cv2.resize(self.base_tiktok_gopro_thred.curGoproFrame, Size480_320)[0:350, 0:500]




        cv2.imshow('titokImg', titokImg)

    def getAliyunSlectId(self):
        return dele.base_Linkit_model.instance.selectID


    curCapVideo=None
    curCapRoiRect=None

    def setMainRect(self,rect):
        self.curCapRoiRect=rect


    curPathIdx=0
    def changeVideoPath(self):
        self.curPathIdx+=1
        if self.curPathIdx%2==1:
            videoBaseUrl = "D:/pythonscore/YOLOv8-DeepSort-PyQt-GUI-main/data/hikCam_001.MP4"
        else:
            videoBaseUrl = "rtsp://admin:Hik123456@192.168.31.212/Streaming/Channels/2"

        videoBaseUrl = "D:/pythonscore/YOLOv8-DeepSort-PyQt-GUI-main/data/hikCam_001.MP4"
        cap= cv2.VideoCapture(videoBaseUrl)
        if cap.isOpened():
            print('视频正确')
            cap.set(cv2.CAP_PROP_POS_FRAMES, 430)
            self.curCapVideo = cap
            self.runCap()
            pass
        else:
            print('更改视频地址不成功')
            pass

    def makeGoproCam(self):
        videoBaseUrl = "rtmp://192.168.31.36:1935/live/test"
        return cv2.VideoCapture(videoBaseUrl)

    testGoproCamTM=0
    def readGoproVideo(self):
        if self.goproCap is None:
            self.testGoproCamTM= time.time()
            print('请求一次Gopro的流')
            self.goproCap=self.makeGoproCam()
        if self.goproCap.isOpened():
            ret, frame = self.goproCap.read()
            if ret:
                self.curGoproFrame = frame
            else:
                print('goproRead出错')
        else:
            print('gopro不可用',time.time()-self.testGoproCamTM)

            if time.time()-self.testGoproCamTM>100:
                self.goproCap=None;


        pass
    def runCap(self):
        cap=self.curCapVideo
        rect=self.curCapRoiRect
        while cap.isOpened():
            if dele.base_Linkit_model.instance.showLockVedeo:
                dele.base_Linkit_model.instance.showLockVedeo = False
                self.changeVideoPath()
                break


            tm=time.time()
            ret, capframe = cap.read()
            if ret:
                 self.drawTempFrame(capframe,rect)
                 self.curCapframe = capframe
            else:
                print('视频播放结束')

            self.makeThreadWait(rect)

            self.printPlayInfo(cap)
            # self.readGoproVideo()

            self.drawToTiktokView()

            tm = (time.time() - tm)*1000
            tm=int((1000.0/10)-tm )
            if tm>0:
                if cv2.waitKey(tm) == ord("q"):
                    break
            else:
                if cv2.waitKey(1) == ord("q"):
                    break

    def printPlayInfo(self,cap):

            print('save', self.saveFrameNum, int(cap.get(cv2.CAP_PROP_POS_FRAMES)), '/',
                  int(cap.get(cv2.CAP_PROP_FRAME_COUNT)),
                  'waitFrame->' + str(len(self.file_process_thread.waitFrameUrlArr)))














