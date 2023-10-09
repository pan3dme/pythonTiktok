import json
import time

import cv2
import numpy as np
from PyQt5.QtCore import QThread, pyqtSignal

from Lesson_01.meshrolexml import MeshRoleXml


class ReadRecordVideo(QThread):
    showRecordpic = pyqtSignal(object)
    showRightRoleArr = pyqtSignal(list)
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

        MeshRoleXml.get_instance().clearData( )
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

    rng = np.random.default_rng(3)
    PALLETE = rng.uniform(0, 255, size=(81, 3))

    SKELETON = [[15, 13], [13, 11], [16, 14], [14, 12], [11, 12],
                [5, 11], [6, 12], [5, 6], [5, 7], [6, 8], [7, 9],
                [8, 10], [1, 2], [0, 1], [0, 2], [1, 3], [2, 4],
                [3, 5], [4, 6]]

    def draw_results(self, image, model_results):
        img_cpy =image
        if model_results == []:
            return img_cpy
        height, width, _ = img_cpy.shape

        for obj in model_results:
            x0 = round(obj["bbox"][0])
            y0 = round(obj["bbox"][1])
            x1 = round(obj["bbox"][2])
            y1 = round(obj["bbox"][3])

            if obj["rect"] is not None:
                x0 += obj["rect"][0]
                y0 += obj["rect"][1]
                x1 += obj["rect"][0]
                y1 += obj["rect"][1]



            id = int(obj["id"])
            class_name = obj["class"]
            confi = float(obj["confidence"])
            color = self.PALLETE[id % self.PALLETE.shape[0]]
            if obj["keypoints"] != []:
                img_cpy = self.draw_keypoints(img_cpy, obj["keypoints"], color)

            text = '%d-%s-%s' % (id, class_name, str(round(confi, 3)))
            txt_color_light = (255, 255, 255)
            txt_color_dark = (0, 0, 0)
            font = cv2.FONT_HERSHEY_SIMPLEX
            font_scale = 1
            thickness = 2
            txt_size = cv2.getTextSize(text, font, 0.4, 1)[0]
            cv2.rectangle(img_cpy, (x0, y0), (x1, y1), color, int(thickness * 1 * font_scale))
            y0 = y0 - 30

            cv2.putText(img_cpy, text, (x0, y0 + txt_size[1]), font, font_scale, txt_color_dark,
                        thickness=thickness + 1)
            cv2.putText(img_cpy, text, (x0, y0 + txt_size[1]), font, font_scale, txt_color_light, thickness=thickness)
        return img_cpy

    def clearRecord(self):
        cap = self.cap
        print(cap.isOpened())
        if cap.isOpened():
            cap.release()
            print('结束录屏播放')
            print(cap.isOpened())

    def run(self):
        time.sleep(1)
        while True:
            tm=time.time()
            if self.pause_process:
                time.sleep(1)
            else:
                cap= self.cap

                if  cap.isOpened():
                    ret, baseframe = cap.read()
                    if ret:

                        video_pos = int(cap.get(cv2.CAP_PROP_POS_FRAMES))
                        if str(video_pos) in self.outkeyDic:
                            _labelmeXml = self.outkeyDic[str(video_pos)]

                            MeshRoleXml.get_instance().pushXmlData(_labelmeXml)

                            self.draw_results(baseframe, _labelmeXml)

                        self.showRecordpic.emit(cv2.resize(baseframe, (500, 350)))
                        self.showRightRoleArr.emit(MeshRoleXml.get_instance().rightItem)


                time.sleep(1/10)