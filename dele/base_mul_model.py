import cv2

import dele.base_data
from dele.base_data import BaseData
from dele.base_yolo_deepsort import BaseYoloDeepSort


class BaseMulModel():

    def __init__(self,onnxName,idx):
        self.onnxName=onnxName
        self.baseYoloDeepSort = BaseYoloDeepSort(onnxName)
        self.idx=idx


    def runCap(self,capframe):
        (model_output, frame) = self.baseYoloDeepSort.drawFrameInfo(capframe)
        frame= cv2.resize(frame, (800,500))
        # cv2.imshow("mul_img"+str(self.idx), dele.base_data.instance.showFps(frame, tx=200))



        cv2.imshow(self.onnxName[-20:], dele.base_data.instance.showFps(frame, tx=200))

