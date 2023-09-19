import json

import numpy as np

from dele.base_write_worker import BaseWriteProcessThread
import dele.base_data
import cv2

import time
import os
import dele.base_Linkit_model
from tkinter import *
from tkinter.messagebox import *


class BaseWriteVideo():
    def filter_img(self,frame):
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
        _, thresh = cv2.threshold(frame, 20, 255, cv2.THRESH_BINARY)
        thresh = cv2.erode(thresh, kernel, iterations=2)
        dilated = cv2.dilate(thresh, kernel, iterations=2)

        return dilated




    def fillet_arr(self,arr):
        for temp in arr:
            temp["bbox"] = temp["bbox"].tolist()
            (x, y, w, h) = self.curCapRoiRect
            temp["rect"] = [x, y, w, h]
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

        # conf_thr = 0.3
        # iou_thr = 0.45
        conf_thr = 0.1
        iou_thr = 0.15
        # 官方系统版本//yolov8n.onnx
        # model_name = 'D:\pythonscore\YOLOv8-DeepSort-PyQt-GUI-main\weights/detection/yolov8n.onnx'
        # model_name = 'D:\\ultralytics-main\\runs\detect\\train10\weights\\best.onnx'
        model_name=onnName

        self.file_process_thread = BaseWriteProcessThread()
        self.file_process_thread.showFrame = cv2.imread("data/bus.jpg")  # 读取1.jpg图像
        self.file_process_thread.set_start_config(
            model_name=model_name,
            confidence_threshold=conf_thr,
            iou_threshold=iou_thr)

        self.file_process_thread.start()

        self.object_detector = cv2.createBackgroundSubtractorMOG2(history=500, varThreshold=40, detectShadows=True)


    def runCap(self,cap, saveName ,frame_width,frame_height,scale=None,showmask=False):
        if scale==None:
            scale=600.0/frame_width

        print(frame_width,frame_height,scale)

        self.curCapRoiRect= (0,0,frame_width,frame_height)

        Size480_320 = (int(frame_width * scale), int(frame_height * scale))
        outMp4url = "out/"+ saveName + ".mp4"
        isSaveFile = True

        if os.path.exists(outMp4url):
             if askyesno('重要提示', '是否覆盖'+saveName+'原来导出的数据'):
                 isSaveFile = True
             else:
                 isSaveFile=False

        else:
            print("文件不存在")




        self.makedir(outMp4url)

        _saveVideoSize=(int(frame_width * 1), int(frame_height * 1))
        if frame_width>1200:
             _saveVideoSize= (int(frame_width * 1200./frame_width), int(frame_height * 1200./frame_width))

        if isSaveFile:
            self.writerFile = cv2.VideoWriter(outMp4url, cv2.VideoWriter_fourcc(*'mp4v'), 25.0,
                                              _saveVideoSize)

        file_process_thread = self.file_process_thread
        saveFrameNum = 0
        cap.set(cv2.CAP_PROP_POS_FRAMES, 430)
        cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
        while cap.isOpened():
            tm=time.time()

            ret, capframe = cap.read()
            if ret:
                if frame_width > 1000:
                    capframe= cv2.resize(capframe, _saveVideoSize)

                resized_img = cv2.resize(capframe, Size480_320)
                applymask =self.object_detector.apply(resized_img)
                mask = self.filter_img(applymask)
                willdele = cv2.resize(mask, Size480_320)
                # cv2.imshow("willdele", willdele)
                contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
                # cv2.drawContours(image=willdele, contours=contours, contourIdx=-1, color=(255, 255, 255), thickness=2)
                detections = []
                for contour in contours:
                    if cv2.contourArea(contour) < 25:
                        continue
                    (x, y, w, h) = cv2.boundingRect(contour)
                    detections.append([x, y, w, h])
                    if showmask:
                        cv2.rectangle(mask, pt1=(x, y), pt2=(x + w, y + h), color=(255, 255, 0), thickness=2)
                        cv2.rectangle(applymask, pt1=(x, y), pt2=(x + w, y + h), color=(255, 255, 0), thickness=2)

                    # print(x, y, w, h)

                cv2.imshow('resized_img', dele.base_data.instance.showFps(resized_img))
                if showmask:
                    cv2.imshow('mask', mask)
                    cv2.imshow('applymask', applymask)
                # 装帧数据存到缓存中

                # self.CacheWaitArr.append([capframe,  capframe[50:300, 100:600]])
                self.CacheWaitArr.append([capframe,  capframe])

                if len(detections) > 0:
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

            if len(file_process_thread.needShowFrameArr) > 0:
                video_pos,baseframe, vframe, vinfo = file_process_thread.needShowFrameArr[0]
                # cv2.imshow('showFrame', cv2.resize(vframe, Size480_320))
                # titokImg[0:frame_height, 0:frame_width] = vframe[0:frame_height, 0:frame_width]
                # titokImg[0+frame_height:frame_height+frame_height, 0:frame_width] =  cv2.merge([mask, mask, mask ])[0:frame_height, 0:frame_width]
                cv2.imshow('vframe', vframe)

                # cv2.imshow('showFrame', vframe)
                # dele.base_data.instance.sendArrToChuankou(vinfo)
                dele.base_Linkit_model.instance.sendArrToChuankou(vinfo)

                print('save',saveFrameNum,int(cap.get(cv2.CAP_PROP_POS_FRAMES)), '/', int(cap.get(cv2.CAP_PROP_FRAME_COUNT)),
                      'waitFrame->' + str(len(file_process_thread.waitFrameUrlArr)))
                if len(file_process_thread.needShowFrameArr) > 1:
                    saveFrameNum = saveFrameNum + 1
                    if isSaveFile:
                        self.writerFile.write(baseframe)
                        addTextStr = str(video_pos) + "||" + self.fillet_arr(vinfo) + "\n"
                        strUrl="out/" + saveName + ".txt"
                        with open(strUrl, 'a') as f:
                            f.write(addTextStr)

                    del file_process_thread.needShowFrameArr[0]
            tm = (time.time() - tm)*1000
            # 1000.0/10 为一秒播放10帧
            tm=int((1000.0/24)-tm )
            # max_val = max([tm,100])
            if tm>0:
                if cv2.waitKey(tm) == ord("q"):
                    break
            else:
                if cv2.waitKey(1) == ord("q"):
                    break













