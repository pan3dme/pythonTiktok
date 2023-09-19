import time

import cv2


class FpsMc():
    def __init__(self):
        self.lastTm=time.time()
        self.lastUseTm=[]

    def showFps(self,image,tx=25,ty=25,scaleFont=1):
        self.lastUseTm.append(time.time()-self.lastTm)
        if len(self.lastUseTm)>30:
            del self.lastUseTm[0]
        self.lastTm = time.time()
        _totalNum=0
        for _num in self.lastUseTm:
            _totalNum=_totalNum+_num
        tm=_totalNum/len(self.lastUseTm)
        txt_color_light = (255, 255, 255)
        txt_color_dark = (255, 0, 0)
        image = cv2.putText(image, 'fps:'+str(int(1/tm)),  (tx, ty), cv2.FONT_HERSHEY_SIMPLEX, scaleFont, txt_color_light, 2 )
        image = cv2.putText(image, 'fps:'+str(int(1/tm)),  (tx, ty), cv2.FONT_HERSHEY_SIMPLEX, scaleFont, txt_color_dark, 1 )

        # cv.putText(img_cpy, text, (x0, y0 + txt_size[1]), font, font_scale, txt_color_dark, thickness=thickness + 1)
        # cv.putText(img_cpy, text, (x0, y0 + txt_size[1]), font, font_scale, txt_color_light, thickness=thickness)


        return image