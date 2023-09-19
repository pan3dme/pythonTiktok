
import cv2
import time

import serial



class BaseData():


    def __init__(self):
        self.name = 'name'
        self.initdata()

    def initdata(self):
        print('BaseData',self.name)

    lastTm=time.time()
    lastUseTm=[]
    def showFps(self,image,tx=25,ty=25):

        self.lastUseTm.append(time.time()-self.lastTm)
        if len(self.lastUseTm)>30:
            del self.lastUseTm[0]
        self.lastTm = time.time()

        _totalNum=0
        for _num in self.lastUseTm:
            _totalNum=_totalNum+_num

        tm=_totalNum/len(self.lastUseTm)



        image = cv2.putText(image, 'fps:'+str(int(1/tm)),  (tx, ty), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2, cv2.LINE_AA)

        return image


    lastNum=0
    def sendArrToChuankou(self,arr):
        if len(arr)>0:
            for vo in arr:
                if self.lastNum < vo['id']:
                    self.lastNum = vo['id']
                    print(self.lastNum)
                    self.sendChuanKou(self.lastNum)


    def out(self):
        print('fuck')
    def sendChuanKou(self,val):
        try:
            # 端口，GNU / Linux上的/ dev / ttyUSB0 等 或 Windows上的 COM3 等
            # portx = "COM6"
            portx = "COM7"
            # 波特率，标准值之一：50,75,110,134,150,200,300,600,1200,1800,2400,4800,9600,19200,38400,57600,115200
            bps = 115200
            # 超时设置,None：永远等待操作，0为立即返回请求结果，其他值为等待超时时间(单位为秒）
            timex = 5
            # 打开串口，并得到串口对象
            ser = serial.Serial(portx, bps, timeout=timex)
            print("打开串口 ", portx)

            # while True:
            #     data = ser.readline()
            #     print(data.decode())
            #     cv2.waitKey(10)

            rcv = ser.read_all()
            if (len(rcv) > 1):
                print(rcv)

            result = ser.write((" " + str(val)).encode("gbk"))

            ser.close()  # 关闭串口


        except Exception as e:
            print("---异常---：", e)

instance = BaseData()

