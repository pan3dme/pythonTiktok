import json
import time

import cv2
from PyQt5.QtCore import QThread, pyqtSignal


class ReadRecordVideo(QThread):
    showRecordpic = pyqtSignal(object)
    def __init__(self):
        super(ReadRecordVideo, self).__init__()

        self.pause_process = False
        self.filePathUrl=''
    def getAllFrameRidByDic(self,dic):
        outRidDic = {}
        for key in dic:
            for vo in dic[key]:
                idStr = str(vo['id'])
                if not (idStr in outRidDic):
                    outRidDic[idStr] = []
                outRidDic[idStr].append(vo)

        return outRidDic
    def removeDisplayClass(self, value):
        return value
        _arr = []
        # 指定显示的类型
        passNameArr = ['sheep', 'dog', 'cow', 'cat', 'horse', 'person']
        if len(value):
            for vo in value:
                class_name = vo['class']
                if not (class_name in passNameArr):
                    if not (class_name in self.tempDeleKey):
                        self.tempDeleKey.append(class_name)
                        print('标记', passNameArr)
                        print('不标记', self.tempDeleKey)
                    continue
                else:
                    _arr.append(vo)

        return _arr
    def setFileUrl(self,value):
        print(value)
        self.filePathUrl=value


        tempFile = open(self.filePathUrl)
        self.tempDeleKey = []
        self.outkeyDic = {}
        for line in tempFile.readlines():
            line = line.replace("\n", "")
            lineArr = line.split("||")
            temp = json.loads(lineArr[1])
            self.outkeyDic[lineArr[0]] = self.removeDisplayClass(temp)

        tempFile.close()
        print(self.filePathUrl.replace('.txt','.mp4'))
        self.cap = cv2.VideoCapture(self.filePathUrl.replace('.txt','.mp4'))
        self.frame_height = self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
        self.frame_width = self.cap.get(cv2.CAP_PROP_FRAME_WIDTH)
        self.allFrameRidByDic = self.getAllFrameRidByDic(self.outkeyDic)
        self.pause_process=False
    def run(self):
        time.sleep(1)
        while True:
            print('ReadRecordVideo run')
            tm=time.time()
            if self.pause_process:
                time.sleep(1)
            else:
                cap= self.cap
                print(cap.isOpened())
                if  cap.isOpened():
                    ret, baseframe = cap.read()
                    if ret:
                        self.showRecordpic.emit(cv2.resize(baseframe, (500, 350)))
                        print('recorde run')




                time.sleep(1)