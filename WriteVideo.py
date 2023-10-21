import sys
import time
import cv2

from dele.base_data import BaseData
from dele.base_mul_model import BaseMulModel
from dele.base_write_video import  BaseWriteVideo
from datetime import datetime, timedelta

from dele.base_yolo_deepsort import BaseYoloDeepSort

# url = 'rtsp://admin:Hik123456@192.168.31.212/Streaming/tracks/1?starttime='+startStr+'&endtime='+endStr
# url = "rtsp://admin:Hik123456@192.168.31.212/Streaming/Channels/2"
# url = "D:\pythonscore\YOLOv8-DeepSort-PyQt-GUI-main\out\hikCam.mp4"
class CamWriteVideo(BaseWriteVideo):
    def __init__(self,onnName):
        super(CamWriteVideo, self).__init__(onnName)
    def runLocaVdeo(self,saveName):
        # 大街人走动
        # videoBaseUrl = "D:/pythonscore/YOLOv8-DeepSort-PyQt-GUI-main/data/TownCentreXVID.avi"
        # videoBaseUrl = "D:/pythonscore/YOLOv8-DeepSort-PyQt-GUI-main/data/hikCam_001.MP4"
        # videoBaseUrl = "D:/pythonscore/YOLOv8-DeepSort-PyQt-GUI-main/data/doorsheep.MP4"
        # videoBaseUrl = "D:/pythonscore/YOLOv8-DeepSort-PyQt-GUI-main/data/hikCam_001.MP4"
        videoBaseUrl = "D:/pythontiktok/data/10月20日.mp4"
        # videoBaseUrl = "D:/gopro/GX051784.MP4"
        cap = cv2.VideoCapture(videoBaseUrl)
        frame_height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
        frame_width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
        if cap.isOpened():
            self.runCap(cap,saveName, int(frame_width), int(frame_height),1.0 )
        else:
            print('视频出错')


    def runPcCamVdeo(self,saveName):

        cap = cv2.VideoCapture(0,cv2.CAP_DSHOW)
        frame_height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
        frame_width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
        if cap.isOpened():
            self.runCap(cap, saveName, frame_width, frame_height ,1)
        else:
            print('摄像头出错')

    def runHikVideo(self,saveName):

        url = "rtsp://admin:Hik123456@192.168.31.212/Streaming/Channels/2"
        cap = cv2.VideoCapture(url)

        frame_height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
        frame_width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
        if cap.isOpened():
            self.runCap(cap, saveName, int(frame_width), int(frame_height), 1)
        else:
            print('摄像头出错')



    def changeDayToTimeStr(self,tm):



        return '20230827t144000z'
    def readHikVde(self,saveName):
        # 给镜头的播放时间

        tm=datetime(2023, 9, 16, 18, 24, 40)
        cap=self.makeHistoryHikCamByData(tm)
        _baseYoloDeepSort = BaseYoloDeepSort(onnxName)

        while cap.isOpened():
            a = cap.read()
            ret, capframe = cap.read()
            if ret:
                # cv2.imshow("capframe", capframe)
                # baseFrame= capframe[0:250, 250:600]
                # capframe =  baseFrame[50:200, 50:350]
                # baseFrame=capframe[150:400, 250:850]
                baseFrame=capframe

                (model_output,frame) = _baseYoloDeepSort.drawFrameInfo(capframe)
                # self.baseData.sendArrToChuankou(model_output)
                resized_img = frame

                applymask = self.object_detector.apply(baseFrame)
                mask = self.filter_img(applymask)
                cv2.imshow("tiktok_mask", mask)


                cv2.imshow("tiktok_img", resized_img)
                # tiktok_frame=_baseYoloDeepSort.drawOutPutToFrame(baseFrame, model_output, (50, 50))
                # cv2.imshow("tiktok_frame",self.baseData.showFps(tiktok_frame, tx=200))
                print(cap.get(cv2.CAP_PROP_POS_FRAMES))

            else:
                print('capframe ret')
            keyCode=cv2.waitKey(1)
            if keyCode == ord("q"):
                break
            if keyCode == ord("r"):
                cap.set(cv2.CAP_PROP_POS_FRAMES, 5200)




        print('结束')


    def makeHistoryHikCamByData(self,tm=None):
        # tm参数为指定时间，为空就是一个小时钱的数据
        base_time = datetime.now()
        base_time += timedelta(hours=-8)
        start_time = base_time + timedelta(hours=-1)
        end_time = base_time + timedelta(minutes=-1)

        if not tm==None:
            start_time =tm+ timedelta(hours=-8)




        # 人工输入一个时间
        # start_time = datetime(2023, 8, 30, 12, 23, 40)
        # start_time += timedelta(hours=-8)
        print('开始的时间',start_time)
        startStr = start_time.strftime("%Y%m%dt%H%M%Sz")
        endStr = end_time.strftime("%Y%m%dt%H%M%Sz")
        print(startStr, endStr)
        url = 'rtsp://admin:Hik123456@192.168.31.212/Streaming/tracks/2?starttime='+startStr+'&endtime='+endStr
        print(url)
        cap = cv2.VideoCapture(url)
        return cap



    def playBaseMulModel(self):


        _arr=[]
        # _arr.append( 'D:\pythonscore\YOLOv8-DeepSort-PyQt-GUI-main\weights\detection\yolov8n.onnx')
        _arr.append( 'D:\\ultralytics-main\\runs\detect\\train15\weights\\best.onnx')
        # _arr.append('D:\\ultralytics-main\\runs\detect\\train17\weights\\best.onnx')
        _arr.append('D:\\ultralytics-main\\runs\detect\\train19\weights\\best.onnx')
        _arr.append('D:\\ultralytics-main\\runs\detect\\train20\weights\\best.onnx')


        _modelArr=[]
        for i in range(len(_arr)):
            _modelArr.append(BaseMulModel(_arr[i], i))


        # tm=datetime(2023, 8, 30, 12, 23, 40)
        # cap = self.makeHistoryHikCamByData(tm)

        url="D:\pythonscore\YOLOv8-DeepSort-PyQt-GUI-main\data\hikCam_001.mp4"
        cap = cv2.VideoCapture(url)

        cap.set(cv2.CAP_PROP_POS_FRAMES,1)


        frame_height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
        frame_width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
        Size480_320 = (int(frame_width * 1), int(frame_height * 1))

        if cap.isOpened():
            while cap.isOpened():
                ret, capframe = cap.read()
                if ret:
                    capframe = cv2.resize(capframe, Size480_320)
                    # capframe=capframe[0:250, 250:600]

                    for i in range(len(_modelArr)):
                        _modelArr[i].runCap(capframe)

                keyCode = cv2.waitKey(100)
                print(cap.get(cv2.CAP_PROP_POS_FRAMES))

                if keyCode == ord("q"):
                    break
                if keyCode == ord("r"):
                    cap.set(cv2.CAP_PROP_POS_FRAMES, 5200)

        else:
            print('摄像头出错')




if __name__ == '__main__':

    # onnxName = 'D:\\ultralytics-main\\runs\detect\\train20\weights\\best.onnx'
    onnxName='D:\pythonscore\YOLOv8-DeepSort-PyQt-GUI-main\weights\detection\yolov8n.onnx'
    mainWindow = CamWriteVideo(onnxName)
    _selectTyp=1
    match _selectTyp:
        case 1:
            mainWindow.runLocaVdeo("yolov8n")
        case 2:
            mainWindow.runPcCamVdeo("pccam002")
        case 3:
            # 读取时时摄像头
            mainWindow.runHikVideo("hikCam")
        case 4:
            # 读取摄像头的历史记录
            mainWindow.readHikVde('record01')
        case 5:
            # 显示两组ONNX的识别效果
            mainWindow.playBaseMulModel()
        case 6:
            pass
        case _:
            print('请核对要使用的功能')



