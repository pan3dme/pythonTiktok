import json
import math
import os
import time

import cv2 as cv
import numpy as np

from PyQt5.QtCore import QThread, pyqtSignal

from src.models.tracking.deep_sort import DeepSort
from src.utils.general import ROOT, add_image_id
from src.models.detection.yolov8_detector_onnx import YoloDetector


class VideoDeepQthread(QThread):
    showDeepFrame = pyqtSignal(object)
    saveRecordVideoByFrame = pyqtSignal(object)

    def filter_img(self, frame):
        kernel = cv.getStructuringElement(cv.MORPH_ELLIPSE, (3, 3))
        _, thresh = cv.threshold(frame, 20, 255, cv.THRESH_BINARY)
        thresh = cv.erode(thresh, kernel, iterations=2)
        dilated = cv.dilate(thresh, kernel, iterations=2)

        return dilated

    def fillet_arr(self, arr, rect):
        for temp in arr:
            temp["bbox"] = temp["bbox"].tolist()
            (x, y, w, h) = rect
            temp["rect"] = [x, y, w, h]
        return str(json.dumps(arr))

    def makedir(self, dir_path):
        dir_path = os.path.dirname(dir_path)  # 获取路径名，删掉文件名
        bool = os.path.exists(dir_path)  # 存在返回True，不存在返回False
        if bool:
            pass
        else:
            os.makedirs(dir_path)

    def __init__(self):
        super(VideoDeepQthread, self).__init__()
        self.threadFlag = True
        self.pause_process = False
        self.confi_thr = 3.0
        self.iou_thr = 3.5
        self.model_name = "yolov8n.PT"
        self.waitFrameUrlArr = []
        self.tracker = None
        self.saveVideo = False
        self.writerVideoFile = None
        self.frameRecordIdx=0


    def sendFrameInfo(self, arr):
        # 限制一下预备等候分析的
        if len(self.waitFrameUrlArr) > 500000:
            print('有可能内存溢出，所以暂时限制最500张等待图')
            del self.waitFrameUrlArr[0]
        self.waitFrameUrlArr.append(arr)

    def set_start_config(self, model_name="yolov8n", confidence_threshold=0.35, iou_threshold=0.45):
        self.threadFlag = True
        self.confi_thr = confidence_threshold
        self.iou_thr = iou_threshold
        self.model_name = model_name
        self._init_yolo()
        self._init_tracker()

    def resetYoloDetector(self):
        self.waitFrameUrlArr.clear()
        print('resetYoloDetector')

    def _init_yolo(self):
        self.detector = YoloDetector()
        self.detector.init(
            model_path=self.model_name,
            class_txt_path=os.path.join(ROOT, "weights/classes.txt"),
            confidence_threshold=self.confi_thr,
            iou_threshold=self.iou_thr)

    def _init_tracker(self):

        self.tracker = DeepSort(
            model_path=os.path.join(ROOT, f"src/models/tracking/deep_sort/deep/checkpoint/ckpt.t7"))

    def runTemp(self, idx):

        baseFrame = self.waitFrameUrlArr[0][0]
        (x, y, w, h) = self.waitFrameUrlArr[0][1]
        del self.waitFrameUrlArr[0]

        if self.saveVideo:
            # self.saveRecordVideoByFrame.emit(cv.resize(baseFrame, (500, 350)))
            self.saveRecordVideoByFrame.emit(baseFrame)



        cutFrame = baseFrame[int(y * baseFrame.shape[0]): int(h * baseFrame.shape[0]),
                   int(x * baseFrame.shape[1]):int(w * baseFrame.shape[1])]

        model_output = self.detector.inference(cutFrame, self.confi_thr, self.iou_thr)
        model_output = self.tracker.update(
            detection_results=model_output,
            ori_img=cutFrame)
        model_output = add_image_id(model_output, idx)


        if self.saveVideo:
            (th,tw,tn)=baseFrame.shape
            addTextStr = str(self.frameRecordIdx) + "||" + self.fillet_arr(model_output, (int(x*tw), int(y*th),int( w*tw),int( h*th))) + "\n"
            self.frameRecordIdx+=1
            strUrl = "out/tiktok.txt"
            with open(strUrl, 'a') as f:
                f.write(addTextStr)

        self.draw_results(cutFrame, model_output)
        self.showDeepFrame.emit(cv.resize(baseFrame, (500, 350)))





    def run(self):

        time.sleep(1.0)
        frame_idx=0
        while self.threadFlag:
            if self.pause_process:
                time.sleep(1.0)
            else:
                if len(self.waitFrameUrlArr):
                    self.runTemp(frame_idx)
                    print('wait', len(self.waitFrameUrlArr))
                    frame_idx+=1
                    time.sleep(0.3)
                else:
                    time.sleep(1.0)

    rng = np.random.default_rng(3)
    PALLETE = rng.uniform(0, 255, size=(81, 3))
    SKELETON = [[15, 13], [13, 11], [16, 14], [14, 12], [11, 12],
                [5, 11], [6, 12], [5, 6], [5, 7], [6, 8], [7, 9],
                [8, 10], [1, 2], [0, 1], [0, 2], [1, 3], [2, 4],
                [3, 5], [4, 6]]

    def draw_results(self, image, model_results):
        img_cpy = image
        if not model_results:
            return img_cpy
        height, width, _ = img_cpy.shape
        for obj in model_results:
            x0 = round(obj["bbox"][0])
            y0 = round(obj["bbox"][1])
            x1 = round(obj["bbox"][2])
            y1 = round(obj["bbox"][3])
            id = int(obj["id"])
            class_name = obj["class"]
            confi = float(obj["confidence"])
            color = self.PALLETE[id % self.PALLETE.shape[0]]

            text = '%d-%s' % (id, class_name)
            txt_color_light = (255, 255, 255)
            txt_color_dark = (0, 0, 0)
            font = cv.FONT_HERSHEY_SIMPLEX
            FONT_SCALE = 1e-3
            THICKNESS_SCALE = 6e-4
            font_scale = min(width, height) * FONT_SCALE
            if font_scale <= 0.4:
                font_scale = 0.41
            elif font_scale > 2:
                font_scale = 2.0
            thickness = math.ceil(min(width, height) * THICKNESS_SCALE)
            txt_size = cv.getTextSize(text, font, 0.4, 1)[0]
            cv.rectangle(img_cpy, (x0, y0), (x1, y1), color, int(thickness * 5 * font_scale))
            cv.rectangle(
                img_cpy,
                (x0, y0 + 1),
                (x0 + txt_size[0] + 1, y0 + int(1.5 * txt_size[1])),
                color,
                -1)
            cv.putText(img_cpy, text, (x0, y0 + txt_size[1]), font, font_scale, txt_color_dark, thickness=thickness + 1)
            cv.putText(img_cpy, text, (x0, y0 + txt_size[1]), font, font_scale, txt_color_light, thickness=thickness)

            cv.putText(img_cpy, "{:.2f}".format(confi), (x0 + 110, y0 + txt_size[1]), font, font_scale, txt_color_dark,
                       thickness=thickness + 1)
            cv.putText(img_cpy, "{:.2f}".format(confi), (x0 + 110, y0 + txt_size[1]), font, font_scale, txt_color_light,
                       thickness=thickness)

        return img_cpy




