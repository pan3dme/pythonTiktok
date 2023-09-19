
import cv2
import json
import os
import math
import numpy as np
from dele.base_save_labelme import BaseSaveLabelMe

import dele.base_data
class BaseDrawSampleRole():
    # passNameArr = ['sheep', 'dog', 'cow', 'cat', 'cat', 'horse']
    #
    # if not (class_name in passNameArr):
    #     if not (class_name in self.tempDeleKey):
    #         self.tempDeleKey.append(class_name)
    #         print('标记', passNameArr)
    #         print('不标记', self.tempDeleKey)
    #     continue
    cap=None
    tempDeleKey=[]
    allFrameRidByDic={}

    frame_height = None
    frame_width =None
    rng = np.random.default_rng(3)
    PALLETE = rng.uniform(0, 255, size=(81, 3))

    SKELETON = [[15, 13], [13, 11], [16, 14], [14, 12], [11, 12],
                [5, 11], [6, 12], [5, 6], [5, 7], [6, 8], [7, 9],
                [8, 10], [1, 2], [0, 1], [0, 2], [1, 3], [2, 4],
                [3, 5], [4, 6]]

    def __init__(self,filename):
        self.filename = filename
        self.initdata()
    def getAllFrameRidByDic(self,dic):
        outRidDic = {}
        for key in dic:
            for vo in dic[key]:
                idStr = str(vo['id'])
                if not (idStr in outRidDic):
                    outRidDic[idStr] = []
                outRidDic[idStr].append(vo)

        return outRidDic

    def makedir(self, dir_path):
        dir_path = os.path.dirname(dir_path)  # 获取路径名，删掉文件名
        bool = os.path.exists(dir_path)  # 存在返回True，不存在返回False
        if bool:
            pass
        else:
            os.makedirs(dir_path)

    # 保存每个角色的最代表保存到图片
    def savePicToFolder(self):
        cap = self.cap
        for key in self.allFrameRidByDic:
            drawTem = None
            for item in self.allFrameRidByDic[key]:
                if drawTem:
                    x1, y1, w1, h1 = item['bbox']
                    x2, y2, w2, h2 = drawTem['bbox']
                    if (w1 - x1) * (h1 - y1) > (w2 - x2) * (h2 - y2):
                        # print(x1, y1, w1, h1, '             ',  x2, y2, w2, h2 )
                        drawTem = item


                else:
                    drawTem = item

            if drawTem:
                cap.set(cv2.CAP_PROP_POS_FRAMES, drawTem['image_id'])
                # print(drawTem['bbox'])
                x, y, w, h = drawTem['bbox']

                x = int(x)
                y = int(y)
                w = int(w)
                h = int(h)
                if x < 0:
                    x = 0
                if y < 0:
                    y = 0

                ret, frame = cap.read()
                vid = int(cap.get(cv2.CAP_PROP_POS_FRAMES))
                if ret:
                    crop = frame[y:h, x:w]
                    fileurl = 'out/' + self.filename + '/classrid/' + str(drawTem['id']) + '.jpg'
                    self.makedir(fileurl)
                    print('截取角色指定图片',fileurl)
                    cv2.imwrite(fileurl, crop)


    def removeDisplayClass(self,value):
        return value
        _arr = []
        # 指定显示的类型
        passNameArr=['sheep','dog','cow','cat','horse','person']
        if len(value):
            for vo in value:
                class_name=vo['class']
                if not (class_name in passNameArr):
                    if not (class_name in self.tempDeleKey):
                        self.tempDeleKey.append(class_name)
                        print('标记', passNameArr)
                        print('不标记', self.tempDeleKey)
                    continue
                else:
                    _arr.append(vo)

        return _arr
    def initdata(self):
        print('读取视频标记文件', 'out/' + self.filename + '.txt')
        tempFile = open('out/' + self.filename + '.txt')
        self.tempDeleKey = []
        self.outkeyDic = {}
        for line in tempFile.readlines():
            line = line.replace("\n", "")
            lineArr = line.split("||")
            temp = json.loads(lineArr[1])
            self.outkeyDic[lineArr[0]] =  self.removeDisplayClass(temp)

        tempFile.close()

        print('读取视频文件',"out/" + self.filename + ".mp4")
        self.cap = cv2.VideoCapture("out/" + self.filename + ".mp4")

        self.frame_height =  self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
        self.frame_width =  self.cap.get(cv2.CAP_PROP_FRAME_WIDTH)
        self.allFrameRidByDic = self.getAllFrameRidByDic(self.outkeyDic)

    def draw_keypoints(self,image, keypoints, color, kpt_score_threshold=0.3, radius=4, thickness=3, skeleton=SKELETON):
        img_h, img_w, _ = image.shape
        kpts = np.array(keypoints, copy=False)
        for kpt in kpts:
            x_coord, y_coord, kpt_score = int(kpt[0]), int(kpt[1]), kpt[2]
            if kpt_score < kpt_score_threshold:
                continue
            cv2.circle(image, (int(x_coord), int(y_coord)), radius,
                       color, -1)

        for sk in skeleton:
            pos1 = (int(kpts[sk[0], 0]), int(kpts[sk[0], 1]))
            pos2 = (int(kpts[sk[1], 0]), int(kpts[sk[1], 1]))

            if (pos1[0] <= 0 or pos1[0] >= img_w or pos1[1] <= 0
                    or pos1[1] >= img_h or pos2[0] <= 0 or pos2[0] >= img_w
                    or pos2[1] <= 0 or pos2[1] >= img_h
                    or kpts[sk[0], 2] < kpt_score_threshold
                    or kpts[sk[1], 2] < kpt_score_threshold):
                continue
            cv2.line(image, pos1, pos2, color, thickness=thickness)
        return image
    def draw_results(self,image, model_results):
        img_cpy = image.copy()
        if model_results == []:
            return img_cpy
        height, width, _ = img_cpy.shape

        for obj in model_results:
            x0 = round(obj["bbox"][0])
            y0 = round(obj["bbox"][1])
            x1 = round(obj["bbox"][2])
            y1 = round(obj["bbox"][3])

            if obj["rect"] is not None:
                x0+=obj["rect"][0]
                y0+=obj["rect"][1]
                x1+=obj["rect"][0]
                y1+=obj["rect"][1]


            id = int(obj["id"])
            class_name = obj["class"]
            confi = float(obj["confidence"])



            color = self.PALLETE[id % self.PALLETE.shape[0]]

            if obj["keypoints"] != []:
                img_cpy = self.draw_keypoints(img_cpy, obj["keypoints"], color)

            text = '%d-%s-%s' % (id, class_name,str( round(confi, 3)))
            txt_color_light = (255, 255, 255)
            txt_color_dark = (0, 0, 0)
            font = cv2.FONT_HERSHEY_SIMPLEX
            FONT_SCALE = 1e-3
            THICKNESS_SCALE = 6e-4

            font_scale = min(width, height) * FONT_SCALE
            font_scale=1
            # if font_scale <= 0.4:
            #     font_scale = 0.41
            # elif font_scale > 2:
            #     font_scale = 2.0
            thickness = 2
            txt_size = cv2.getTextSize(text, font, 0.4, 1)[0]
            cv2.rectangle(img_cpy, (x0, y0), (x1, y1), color, int(thickness * 1 * font_scale))
            y0=y0-30
            # cv2.rectangle(
            #     img_cpy,
            #     (x0, y0 + 1),
            #     (x0 + txt_size[0] + 1, y0 + int(1.5 * txt_size[1])),
            #     color,
            #     -1)
            cv2.putText(img_cpy, text, (x0, y0 + txt_size[1]), font, font_scale, txt_color_dark,
                        thickness=thickness + 1)
            cv2.putText(img_cpy, text, (x0, y0 + txt_size[1]), font, font_scale, txt_color_light, thickness=thickness)
        return img_cpy

    def findLoadInfoById(self,value):
        # 获取路径数组
        outArr = []
        for key in self.outkeyDic:
            for item in self.outkeyDic[key]:
                if item["id"] == value:
                    outArr.append(item)

        if len(outArr) == 0:
            print('对应ID没有路径数据', value)
        return outArr

    def findRectByOnlyId(self,arr, value):
        outArr = []
        for item in arr:
            if item["id"] == value:
                outArr.append(item)

        return outArr

    def draw_resultsAlpha(self,image, model_results):
        img_cpy = image.copy()
        if model_results == []:
            return img_cpy
        height, width, _ = img_cpy.shape

        PALLETE=self.PALLETE
        for obj in model_results:
            x0 = round(obj["bbox"][0])
            y0 = round(obj["bbox"][1])
            x1 = round(obj["bbox"][2])
            y1 = round(obj["bbox"][3])
            id = int(obj["id"])
            class_name = obj["class"]
            confi = float(obj["confidence"])

            # print(class_name, confi,x0,y0,x1,y1,id)
            color = PALLETE[id % PALLETE.shape[0]]

            cv2.rectangle(img_cpy, (x0, y0), (x1, y1), (255, 0, 0, 100), 1)

        return img_cpy


    def drawImgFoVdeo(self,showLine=True,scale=0.5):
        _baseSaveLabelMe=BaseSaveLabelMe('readVideo')
        waitTm = int(1000/25);
        # waitTm = int(1000/1);
        Size480_320 = (int(self.frame_width * scale), int(self.frame_height * scale))
        cap=self.cap
        # cap.set(cv2.CAP_PROP_POS_FRAMES,100)
        while cap.isOpened():
            # print(int(cap.get(cv2.CAP_PROP_POS_FRAMES)), '/', int(cap.get(cv2.CAP_PROP_FRAME_COUNT)))
            ret, baseframe = cap.read()

            if ret:
                frame = baseframe
                if showLine:
                    video_pos = int(cap.get(cv2.CAP_PROP_POS_FRAMES))
                    if str(video_pos) in self.outkeyDic:
                        _labelmeXml=self.outkeyDic[str(video_pos)]
                        frame = self.draw_results(baseframe, _labelmeXml)


                cv2.imshow("read_img", dele.base_data.instance.showFps( cv2.resize(frame, Size480_320)))

                print(cap.get(cv2.CAP_PROP_POS_FRAMES),'/' , cap.get(cv2.CAP_PROP_FRAME_COUNT))

            if cap.get(cv2.CAP_PROP_POS_FRAMES) >= cap.get(cv2.CAP_PROP_FRAME_COUNT):
                cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
                pass


            keyNum = cv2.waitKey(waitTm)
            if keyNum == ord("v"):
                showLine=not showLine
            if keyNum == ord("s"):
                if waitTm==1000:
                    waitTm = int(1000/30)
                else:
                    waitTm = 1000


            if keyNum == ord("d"):
                picname = self.filename + str(int(cap.get(cv2.CAP_PROP_POS_FRAMES)))
                fileUrl = 'out/' + self.filename + '/screenshot/' + picname + '.jpg'
                self.makedir(fileUrl)
                cv2.imwrite(fileUrl, baseframe)
                _baseSaveLabelMe.saveLabelJosn(fileUrl,baseframe,_labelmeXml)

                print('drawImg', fileUrl)
                cv2.waitKey(1000)

                pass
            if keyNum == ord("q"):
                break

    def getMinMaxFramId(self,arr):
        if(len(arr)==0):
            return (0,0)
        minid=arr[0]["image_id"]
        maxid=arr[0]["image_id"]
        for temp in arr:
            if minid>temp["image_id"]:
                minid = temp["image_id"]
            if maxid<temp["image_id"]:
                maxid = temp["image_id"]


        return (minid,maxid)
    def runLineToOne(self,scale=0.5):
        ridArr = []
        for key in self.allFrameRidByDic:
            ridArr.append(int(key))

        if len(ridArr) == 0:
            print('没有路劲信息')
        else:
            print('统计到有',len(ridArr),'条独立记录信息')

        curSlectIdx=0
        selectVidNum = ridArr[curSlectIdx]
        loadArr = self.findLoadInfoById(selectVidNum)
        frameSkipNum = 0
        cap=self.cap
        Size480_320 = (int(self.frame_width * scale), int(self.frame_height * scale))

        print('接 N m 键右显示不同的路径')
        while cap.isOpened():
            if len(loadArr) > 0:
                (minid,maxid)=self.getMinMaxFramId(loadArr)

                infovo = loadArr[frameSkipNum % len(loadArr)]
                cap.set(cv2.CAP_PROP_POS_FRAMES, infovo["image_id"])

                frameSkipNum = frameSkipNum + 1
                print(minid, maxid,infovo["image_id"])

                if frameSkipNum<minid or frameSkipNum>maxid:
                    frameSkipNum=minid
                    cap.set(cv2.CAP_PROP_POS_FRAMES,frameSkipNum)



                ret, frame = cap.read()
                if ret:
                    # read_img = cv2.resize(frame, Size480_320)
                    read_img = frame
                    video_pos = int(cap.get(cv2.CAP_PROP_POS_FRAMES))

                    if str(video_pos) in self.outkeyDic:
                        self.findRectByOnlyId(self.outkeyDic[str(video_pos)], selectVidNum)
                        # read_img = self.draw_resultsAlpha(read_img, loadArr)
                        read_img = self.draw_results(read_img, self.findRectByOnlyId(self.outkeyDic[str(video_pos)], selectVidNum))
                    cv2.imshow("read_img", cv2.resize(read_img, Size480_320))

            keyCode = cv2.waitKey(300)
            if keyCode == ord("n"):
                curSlectIdx=curSlectIdx+1
                selectVidNum = ridArr[curSlectIdx % len(ridArr)]
                loadArr = self.findLoadInfoById(selectVidNum)
                print('显示', curSlectIdx % len(ridArr), '/', len(ridArr))

                pass
            if keyCode == ord("m"):
                curSlectIdx = curSlectIdx - 1
                selectVidNum = ridArr[curSlectIdx % len(ridArr)]
                loadArr = self.findLoadInfoById(selectVidNum)
                print('显示', curSlectIdx % len(ridArr), '/', len(ridArr))

                pass
            if keyCode == ord("q"):
                break

