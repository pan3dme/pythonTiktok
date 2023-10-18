
import json

from PyQt5.QtCore import pyqtSignal, QObject
from linkkit import linkkit


class AliyunLinkModel(QObject):
    __instance = None
    topimessgeFun = pyqtSignal(str)
    selectID = 5



    def __init__(self):
        if AliyunLinkModel.__instance is None:
            AliyunLinkModel.__instance = self
        else:
            raise Exception("Singleton class instantiated more than once")

        self.isTrueconnect = False
        self.hikUrl = 'admin:ZHNSEB@192.168.31.231'
        # self.hikUrl='admin:Hik123456@192.168.31.212'

        # {
        #     "ProductKey": "iq6659GBxxY",
        #     "DeviceName": "mobile",
        #     "DeviceSecret": "c4d8ff52c7bb0cbd474ed3ee9b6b0b06"
        # }
        # {
        #     "ProductKey": "iq6659GBxxY",
        #     "DeviceName": "pythontiktok",
        #     "DeviceSecret": "234810429507b6a8bdc24e7fe752b09b"
        # }
        print('初始化阿里云物联网------》init BaseLinkModel')
        self.lk = linkkit.LinkKit(
            host_name="cn-shanghai",
            product_key="iq6659GBxxY",
            device_name="pythontiktok",
            device_secret="234810429507b6a8bdc24e7fe752b09b")

        lk = self.lk
        lk.on_device_dynamic_register = self.on_device_dynamic_register
        lk.on_connect = self.on_connect
        lk.on_disconnect = self.on_disconnect

        lk.on_topic_message = self.on_topic_message
        lk.on_subscribe_topic = self.on_subscribe_topic
        lk.on_unsubscribe_topic = self.on_unsubscribe_topic
        lk.on_publish_topic = self.on_publish_topic

        lk.config_device_info("Eth|03ACDEFF0032|Eth|03ACDEFF0031")
        lk.config_mqtt(port=1883, protocol="MQTTv311", transport="TCP", secure="TLS")
        lk.connect_async()
        lk.start_worker_loop()
        self.rerishTiktokView()


    def on_device_dynamic_register(self, rc, value, userdata):
        if rc == 0:
            print("dynamic register device success, value:" + value)
        else:
            print("dynamic register device fail, message:" + value)


    def on_connect(self, session_flag, rc, userdata):
        print('连接成功')
        print("on_connect:%d,rc:%d" % (session_flag, rc))
        self.isTrueconnect = True
        pass


    def on_disconnect(self, rc, userdata):
        print("on_disconnect:rc:%d,userdata:" % rc)


    def on_topic_message(self, topic, payload, qos, userdata):
        print("on_topic_message:" + topic + " payload:" + str(payload) + " qos:" + str(qos))
        temp = str(payload)
        print(temp)
        temp = temp[2:len(temp) - 1]
        result = json.loads(temp)
        self.selectID = result['total']
        self.rerishTiktokView()

        # 主识别视频切换是否为本地还是海康监控


    showHikCameFrame = False
    # 是否显示时时视频
    showDeepSortFrame = False
    # 是否显示图像识别视频
    showLockVedeo = False


    def rerishTiktokView(self):
        idx = self.selectID
        arr = [0, 3, 5, 13]
        hasIt = False
        for num in arr:
            if num == idx:
                hasIt = True
        if not hasIt:
            return

        self.showLockVedeo = False
        self.showHikCameFrame = False
        self.showDeepSortFrame = False

        match idx:
            case 0:
                self.showHikCameFrame = True
                pass
            case 3:
                self.showDeepSortFrame = True
                pass
            case 5:
                self.showHikCameFrame = True
                self.showDeepSortFrame = True
                pass
            case 13:
                self.showHikCameFrame = True
                self.showDeepSortFrame = True
                self.showLockVedeo = True

            case _:

                pass


    def on_subscribe_topic(self, mid, granted_qos, userdata):
        print("on_subscribe_topic mid:%d, granted_qos:%s" %
              (mid, str(','.join('%s' % it for it in granted_qos))))
        pass


    def on_unsubscribe_topic(self, mid, userdata):
        print("on_unsubscribe_topic mid:%d" % mid)
        pass


    def on_publish_topic(self, mid, userdata):
        print("on_publish_topic mid:%d" % mid)


    skipnum = 0


    def pingLink(self, val):
        if val<=self.skipnum:
            return
        self.skipnum = val
        if self.isTrueconnect:
            print('发送', val)
            lk = self.lk
            # lk.publish_topic(lk.to_full_topic("user/msg"), "{\"total\":" + str(val) + "}")
            lk.publish_topic('/sys/iq6659GBxxY/pythontiktok/thing/event/property/post', str({ "params": {"total": val}}))


        else:
            print('阿里云还没准备好')


    lastNum = 0


    def sendArrToChuankou(self, arr):
        if len(arr) > 0:
            for vo in arr:
                if self.lastNum < vo['id']:
                    self.lastNum = vo['id']
                    print(self.lastNum)
                    self.pingLink(self.lastNum)


    def initData(self):
        print('初始化链接，在第一次引用单例时', self.name)


    @staticmethod
    def get_instance():
        if not AliyunLinkModel.__instance:
            AliyunLinkModel()
        return AliyunLinkModel.__instance

