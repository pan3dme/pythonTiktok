from datetime import datetime, timedelta

import cv2

from Lesson_01.aliyunlinkitmodel import AliyunLinkModel

base_time = datetime.now()

startStr = datetime.now().strftime("%Y%m%dt%H%M")
print(startStr)

AliyunLinkModel.get_instance()

skipNum=0

while True:

    keyNum = cv2.waitKey(3000)


    AliyunLinkModel.get_instance().pingLink(skipNum)
    skipNum+=1;
    print('fuck',skipNum)

    if keyNum == ord("q"):
        break
