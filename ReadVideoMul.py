


import os
from tkinter.messagebox import askyesno

import cv2
import numpy as np

from  dele.base_draw_sample_role import  BaseDrawSampleRole
from dele.save_line_mask_video import SaveLineMaskVideo

os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"


_mulArr=[]

_mulArr.append(BaseDrawSampleRole('mul_yolo'))
_mulArr.append(BaseDrawSampleRole('mul_self'))
_mulArr.append(BaseDrawSampleRole('mul_yolo2'))
# _mulArr.append(BaseDrawSampleRole('ccav'))


_baseDraw= _mulArr[0]
_scale=1

Size480_320 = (int(_baseDraw.frame_width * _scale), int(_baseDraw.frame_height * _scale))
cap =_baseDraw.cap
frame_height =cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
frame_width =cap.get(cv2.CAP_PROP_FRAME_WIDTH)

filename = 'tiktok'
isSaveFile = False
outMp4url = "out/" + filename + ".mp4"
# if os.path.exists(outMp4url):
#     if askyesno('重要提示', '是否覆盖' + filename + '原来导出的数据'):
#         isSaveFile = True
#     else:
#         isSaveFile = False
# else:
#     print("文件不存在直接保存")


if isSaveFile:
    writerFile = cv2.VideoWriter(outMp4url, cv2.VideoWriter_fourcc(*'mp4v'), 25.0,
                                      (int(frame_width)*2, int(frame_height)*2))
else:
    writerFile=None


while cap.isOpened():
    # print(int(cap.get(cv2.CAP_PROP_POS_FRAMES)), '/', int(cap.get(cv2.CAP_PROP_FRAME_COUNT)))





    ret, baseframe = cap.read()
    w,h=Size480_320
    img = np.zeros((h * 2, w*2, 3), np.uint8)
    if ret:
        frame = baseframe
        video_pos = int(cap.get(cv2.CAP_PROP_POS_FRAMES))

        for i in range(len(_mulArr)):
            taget=_mulArr[i]
            if str(video_pos) in taget.outkeyDic:
                _labelmeXml = taget.outkeyDic[str(video_pos)]
                frame = taget.draw_results(baseframe, _labelmeXml)
            frame = cv2.resize(frame, Size480_320)

            font = cv2.FONT_HERSHEY_SIMPLEX
            org = (0, 60)
            fontScale = 1
            color = (255, 255, 0)
            thickness = 1
            frame = cv2.putText(frame, 'Id:' + taget.filename, org, font, fontScale, color, thickness, cv2.LINE_AA)


            img[int(i/2.0)*h:int(i/2.0)*h+h, i%2*w:(i%2)*w+w] = frame[0:h, 0:w]

        # cv2.imshow("read_img",frame)
        cv2.imshow("total_img", img)
        # if writerFile is not None:
        #     writerFile.write(img)

    if cv2.waitKey(1000) == ord("q"):
        break




