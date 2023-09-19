import os
from tkinter.messagebox import askyesno

import cv2

from tiktoksrc.base_tiktok_video import BaseTikTokVideo

class CamWriteVideo(BaseTikTokVideo):
    def __init__(self,onnName):
        super(CamWriteVideo, self).__init__(onnName)

    def makeHikCam(self):
        # videoBaseUrl = "rtsp://admin:Hik123456@192.168.31.212/Streaming/Channels/2"
        videoBaseUrl = "D:/pythonscore/YOLOv8-DeepSort-PyQt-GUI-main/data/hikCam_001.MP4"
        return  cv2.VideoCapture(videoBaseUrl)



    def runLocaVdeo(self,saveName):
        self.outfileName=saveName
        outMp4url = "out/" + self.outfileName + ".mp4"
        if os.path.exists(outMp4url):
            if askyesno('重要提示', '是否覆盖' + saveName + '原来导出的数据'):
                self.isSaveFile = True
            else:
                self.isSaveFile = False

        else:
            print("文件不存在")

        cap = self.makeHikCam()
        if cap.isOpened():
            print('当前的视频的帧率：',cap.get(cv2.CAP_PROP_FPS))
            ret, capframe = cap.read()
            capframe = cv2.putText(capframe, 'Plase Select Roi Aer', (120, 120), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2,
                                cv2.LINE_AA)
            rect = cv2.selectROI(capframe, showCrosshair=True)
            cv2.destroyAllWindows()
            (x, y, w, h) = rect
            if w>200 and h>100:
                self.setMainRect(rect)
                self.changeVideoPath()
            else:
                print('选择区域不规范')

        else:
            print('视频出错')



if __name__ == '__main__':

    onnxName = 'D:\\ultralytics-main\\runs\detect\\train15\weights\\best.onnx'
    # onnxName = 'D:\pythonscore\YOLOv8-DeepSort-PyQt-GUI-main\weights\detection\yolov8m.onnx'

    mainWindow = CamWriteVideo(onnxName)
    mainWindow.runLocaVdeo("mul_yolo2")
    cv2.destroyAllWindows()



