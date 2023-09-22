import time

import cv2
import numpy as np
from ffpyplayer.player import MediaPlayer

video_path = "rtmp://192.168.31.36:1935/live/test"

def PlayVideo(video_path):
    video=cv2.VideoCapture(video_path)
    player = MediaPlayer(video_path)
    while True:
        tm= time.time()
        grabbed, frame = video.read()
        tt=video.get(cv2.CAP_PROP_POS_FRAMES)
        mm=video.get()
        print(tt,mm)
        audio_frame, val = player.get_frame()
        if not grabbed:
            print("End of video")
            break

        cv2.imshow("Video", frame)
        print(time.time()-tm)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break
        if val != 'eof' and audio_frame is not None:
            # audio
            img, t = audio_frame
            # print(img, t)
    video.release()
    cv2.destroyAllWindows()

PlayVideo(video_path)
