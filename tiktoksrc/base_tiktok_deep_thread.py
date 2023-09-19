import time

import dele.base_Linkit_model
from dele.base_write_worker import BaseWriteProcessThread


class BaseTokeDeepThread(BaseWriteProcessThread):

    def setAliyunType(self, num):

        pass



    def run(self):
        showDeepSortFrame=dele.base_Linkit_model.instance.showDeepSortFrame

        frame_id = 1
        while self.threadFlag:
            if self.pause_process or len(self.waitFrameUrlArr) < 1:
                time.sleep(2)
                continue
            if showDeepSortFrame:
                self.runTemp(frame_id)
                frame_id += 1






    