import os
from pathlib import Path

from dele.base_write_worker import BaseWriteProcessThread
from src.models.detection.yolov8_detector_onnx import YoloDetector
from src.models.tracking.deep_sort import DeepSort
from src.utils.general import add_image_id
from src.utils.visualize import draw_results

FILE = Path(__file__).resolve()
ROOT = FILE.parents[2]
class BaseYoloDeepSort(BaseWriteProcessThread):

    def __init__(self , onnxName):
        super(BaseYoloDeepSort, self).__init__()
        conf_thr = 0.3
        iou_thr = 0.45
        self.set_start_config(
            model_name=onnxName,
            confidence_threshold=conf_thr,
            iou_threshold=iou_thr)
    frame_id = 1
    def drawFrameInfo(self,frame):
        model_output = self.detector.inference(frame, self.confi_thr, self.iou_thr)

        model_output = self.tracker.update(
            detection_results=model_output,
            ori_img=frame)
        model_output = add_image_id(model_output, self.frame_id)
        frame = draw_results(frame, model_output)
        self.frame_id=self.frame_id+1
        return (model_output,frame)

    def drawOutPutToFrame(self, frame,model_output,rect):
        (tx,ty)=rect
        for temp in model_output:
            temp['bbox'][0]= temp['bbox'][0]+tx
            temp['bbox'][2]= temp['bbox'][2]+tx
            temp['bbox'][1]= temp['bbox'][1]+ty
            temp['bbox'][3]= temp['bbox'][3]+ty

        frame = draw_results(frame, model_output)
        return frame

