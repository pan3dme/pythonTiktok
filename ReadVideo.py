


import os
from  dele.base_draw_sample_role import  BaseDrawSampleRole
from dele.save_line_mask_video import SaveLineMaskVideo

os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"




# sampleRole=BaseDrawSampleRole('sheep002')
# sampleRole=BaseDrawSampleRole('mul_yolo')
# sampleRole=BaseDrawSampleRole('s_dele')
sampleRole=BaseDrawSampleRole('20231020t1536')


match 1:
   case 0:
       print('保存指定ID的最合适图像')
       sampleRole.savePicToFolder()
   case 1:
       print('截图保存用于训练，按D截图，按V是否显示原来识别到的线框')
       sampleRole.drawImgFoVdeo(True, 2)
   case 2:
       print('显示指定角色信息')
       sampleRole.runLineToOne(scale=1)
   case 3:
       # 定制输出用玩抖音视频素材
       SaveLineMaskVideo('sheep002').drawImgFoVdeoTiTok(True, 0.5)







