from src.qt.stream.video_capture import CameraCaptureThread
from src.qt.stream.visualize import VideoVisualizationThread
from src.qt.stream.ai_worker import AiWorkerThread
from src.ui.main_window import Ui_MainWindow
from src.qt.video.video_worker import FileProcessThread
from PyQt5 import QtGui, QtWidgets
from PyQt5.QtCore import Qt
import cv2
import sys
import numpy as np
import socket

import os

import sys
import cv2
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

import numpy as np
import matplotlib.pyplot as plt
from PyQt5.uic import loadUi

os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"


class MainWindow( ):
    def __init__(self, parent=None):
        self.file_process_thread = FileProcessThread()
        self.model_name = "yolov8n"
        self.ai_task = "object_detection"
        self.file_name = "D:/pythonscore/YOLOv8-DeepSort-PyQt-GUI-main/data/TownCentreXVID.avi"
        self.conf_thr = 0.3
        self.iou_thr = 0.45
        self.frame_interval = 0

    def QImage_to_Opencv(self, qimg):
        print('-----QImage_to_Opencv-----')
        tmp = qimg
        # 使用numpy创建空的图象
        cv_image = np.zeros((tmp.height(), tmp.width(), 3), dtype=np.uint8)
        print('begin cv_image type:', type(cv_image))
        for row in range(0, tmp.height()):
            for col in range(0, tmp.width()):
                r = qRed(tmp.pixel(col, row))
                g = qGreen(tmp.pixel(col, row))
                b = qBlue(tmp.pixel(col, row))
                # cv_image[row, col, 0] = r
                # cv_image[row, col, 1] = g
                # cv_image[row, col, 2] = b
                cv_image[row, col, 0] = b
                cv_image[row, col, 1] = g
                cv_image[row, col, 2] = r
        print('end cv_image type:', type(cv_image))
        # cv2.imwrite('./QImage_to_Opencv.jpg', cv_image)
        return cv_image

    def update_display_frame(self, showImage):
        # image = cv2.imread("bus.jpg")  # 读取1.jpg图像
        # cv2.namedWindow("image")  # 创建一个image的窗口
        cv2.imshow("image", self.QImage_to_Opencv(showImage))  # 显示图像





    def show(self):
        self.file_process_thread.set_start_config(
            video_path=self.file_name,
            ai_task=self.ai_task,
            screen_size=[480, 480],
            model_name=self.model_name,
            confidence_threshold=self.conf_thr,
            iou_threshold=self.iou_thr,
            frame_interval=self.frame_interval)


        self.file_process_thread.send_display_frame.connect(self.update_display_frame)
        self.file_process_thread.start()
        # image = cv2.imread("bus.jpg")  # 读取1.jpg图像
        # self.file_process_thread.pushCvImageToArr(image)








if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    mainWindow = MainWindow()
    cap = cv2.VideoCapture("D:/pythonscore/YOLOv8-DeepSort-PyQt-GUI-main/IMG_9498.MP4")
    frame_height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
    frame_width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)

    while cap.isOpened():
        ret, frame = cap.read()
        if ret:
            resized_img = cv2.resize(frame, (int(frame_width * 0.3), int(frame_height * 0.3)))
            cv2.imshow('Baseframe', resized_img)
            # self.file_process_thread.pushCvImageToArr(resized_img)

        if cap.get(cv2.CAP_PROP_POS_FRAMES) >= cap.get(cv2.CAP_PROP_FRAME_COUNT):
            cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
            pass

        if cv2.waitKey(10) == ord("q"):
            break

    mainWindow.show()
    sys.exit(app.exec_())
