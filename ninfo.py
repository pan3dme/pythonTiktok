import torch
import sys
import torchvision
import ultralytics

from ultralytics import YOLO

print('----------')
print('python 版本sys.version-->',sys.version)
print('----------')
print('torch_version-->',torch.torch_version)
print('----------')
print('torch.cuda.is_available-->',torch.cuda.is_available())
print('----------')
print('torch.__version__-->',torch.__version__)
print('----------')
print('torch.version.cuda-->',torch.version.cuda) # 如果有GPU版本
print('----------')
print('ttorchvision.__version__-->',torchvision.__version__)

ultralytics.checks()