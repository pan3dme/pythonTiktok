import torch
print(torch.__version__)
import sys
from ultralytics import YOLO
import cv2



print('sys.version',sys.version)
print('torch_version-->',torch.torch_version)
# conda info  canda 版本


print(torch.cuda.is_available())
print(torch.__version__)
print(torch.version.cuda) # 如果有GPU版本


model = YOLO("D:\\ultralytics-main\\runs\\detect\\can\\weights\\best.pt")  # 加载预训练模型（建议用于训练）
# path = model.export(format="onnx")  # export the model to ONNX format
# model = YOLO("yolov8n.pt")  # 加载预训练模型（建议用于训练）
# picurl="bus.jpg"
# picurl="data\\panassets\\coco100\\images\\val2017\\picture_002.jpg"
picurl="bus.jpg"
# picurl="bus.jpg"
image=cv2.imread(picurl,cv2.IMREAD_COLOR)
results = model(picurl)

det = results[0].boxes  # TODO: make boxes inherit from tensors

print(det)
for d in reversed(det):
    cls, conf = d.cls.squeeze(), d.conf.squeeze()
    c = int(cls)  # integer class
    name = f'id:{int(d.id.item())} {model.names[c]}' if d.id is not None else  model.names[c]
    box=d.xyxy.squeeze()
    box = box.tolist()
    p1, p2 = (int(box[0]), int(box[1])), (int(box[2]), int(box[3]))
    cv2.rectangle(image,p1, p2, (0, 255, 0),5)




while True:
	cv2.imshow("image",image)
	if cv2.waitKey(100) == ord("q"):
	    break

# cuda安装pytorch
# https://pytorch.org/get-started/locally/
# pip3 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
# pip install opencv-python
# pip install opencv-contrib-python
# cuda安装
# https://developer.nvidia.cn/cuda-toolkit-archive

# pip uninstall torch
# 此外，如果还安装了torchvision组件，则需要再运行以下命令：
#
# pip uninstall torchvision
# 卸载完成后，可以使用以下命令检查PyTorch是否还存在：
#
# import torch

# 1.这里创建一个名为torch1.12的虚拟环境，python使用3.8的版本
# conda create -n torch1.12.1 python=3.8.8
# conda create -n torch1.12 python=3.8
# conda create -n gpupython3.11 Python 3.11.4
# 1
# 2.激活虚拟环境（注：后续的操作都是在该虚拟环境下进行）
# conda activate torch1.12
# conda activate gpupytorch
# conda activate gpu

# conda install pytorch==1.13.1 torchvision==0.14.1 torchaudio==0.13.1 pytorch-cuda=11.6 -c pytorch -c https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/main
# $ pip
# install
# nvidia - pyindex
# $ pip
# install
# nvidia - cudnn - cu116


# pip install torch==2.0.0+cu118 torchvision==0.15.1+cu118 torchaudio==2.0.1 --index-url https://download.pytorch.org/whl/cu118