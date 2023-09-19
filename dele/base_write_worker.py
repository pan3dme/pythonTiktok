from PyQt5.QtCore import QThread, pyqtSignal

from dele.base_data import BaseData
from src.models.detection.yolov8_detector_onnx import YoloDetector
from src.models.pose.yolov8_pose_onnx import PoseDetector
from src.models.segmentation.yolov8_seg_onnx import YOLOSeg
from src.models.tracking.deep_sort.deep_sort import DeepSort
from src.utils.general import ROOT, add_image_id
from src.utils.visualize import draw_results
import os
import cv2 as  cv
import numpy as np
import time

from PyQt5.QtGui import QImage


class BaseWriteProcessThread(QThread):


    def __init__(self):
        super(BaseWriteProcessThread, self).__init__()
        self.thread_name = "DeleProcessThread"
        self.threadFlag = False
        self.waitFrameUrlArr=[]
        self.needShowFrameArr=[]

    def pushFrameToWaitArr(self,arr):
        # 限制一下预备等候分析的
        if len(self.waitFrameUrlArr) > 500000:
            print('有可能内存溢出，所以暂时限制最500张等待图')
            del self.waitFrameUrlArr[0]
        self.waitFrameUrlArr.append(arr)

    def set_start_config(self,      model_name="yolov8n", confidence_threshold=0.35, iou_threshold=0.45):
        self.threadFlag = True
        self.pause_process = False
        self.confi_thr = confidence_threshold
        self.iou_thr = iou_threshold
        self.model_name = model_name
        self._init_yolo()
        self._init_tracker()




    def get_screen_size(self, screen_size):
        self.iw, self.ih = screen_size

    def _init_yolo(self):
        # print(os.path.join(ROOT, f"weights/detection/{self.model_name}.onnx"))

        # _url = 'D:\pythonscore\YOLOv8-DeepSort-PyQt-GUI-main\weights/detection/yolov8n.onnx'

        self.detector = YoloDetector()
        self.detector.init(
            model_path=self.model_name,
            class_txt_path=os.path.join(ROOT, "weights/classes.txt"),
            confidence_threshold=self.confi_thr,
            iou_threshold=self.iou_thr)


    def _init_tracker(self):
        self.tracker = DeepSort(
            model_path=os.path.join(ROOT, f"src/models/tracking/deep_sort/deep/checkpoint/ckpt.t7"))


    def runTemp(self,frame_id):


        baseFrame = self.waitFrameUrlArr[0][0]
        frame = self.waitFrameUrlArr[0][1]
        del self.waitFrameUrlArr[0]

        model_output = self.detector.inference(frame, self.confi_thr, self.iou_thr)

        model_output = self.tracker.update(
            detection_results=model_output,
            ori_img=frame)
        model_output = add_image_id(model_output, frame_id)

        # for track in self.tracker.tracker.tracks:
        #     if not track.is_confirmed() or track.time_since_update > 1:
        #         continue
        #     box = track.to_tlbr()
        #     print(box)

        frame = draw_results(frame, model_output)
        self.needShowFrameArr.append([frame_id, baseFrame, frame, model_output])

    def run(self):
        frame_id = 1
        while self.threadFlag:
            if self.pause_process or len(self.waitFrameUrlArr) < 1:
                time.sleep(2)
                continue
            self.runTemp(frame_id)
            frame_id += 1


    def check_image_or_video(self, media_path):
        img_fm = (".tif", ".tiff", ".jpg", ".jpeg", ".gif", ".png", ".eps", ".raw", ".cr2", ".nef", ".orf", ".sr2", ".bmp", ".ppm", ".heif")
        vid_fm = (".flv", ".avi", ".mp4", ".3gp", ".mov", ".webm", ".ogg", ".qt", ".avchd")
        media_fms = {"image": img_fm, "video": vid_fm}
        if any(media_path.lower().endswith(media_fms["image"]) for ext in media_fms["image"]):
            return "image"
        elif any(media_path.lower().endswith(media_fms["video"]) for ext in media_fms["video"]):
            return "video"
        else:
            raise TypeError("Please select an image or video")

    def convert_cv_qt(self, image, screen_height, screen_width):
        h, w, _ = image.shape
        scale = min(screen_width / w, screen_height / h)
        nw, nh = int(scale * w), int(scale * h)
        image_resized = cv.resize(image, (nw, nh))
        image_paded = np.full(shape=[screen_height, screen_width, 3], fill_value=0)
        dw, dh = (screen_width - nw) // 2, (screen_height - nh) // 2
        image_paded[dh:nh + dh, dw:nw + dw, :] = image_resized
        image_paded = cv.cvtColor(image_paded.astype('uint8'), cv.COLOR_BGR2RGBA)
        return QImage(image_paded.data, image_paded.shape[1], image_paded.shape[0], QImage.Format_RGBA8888)