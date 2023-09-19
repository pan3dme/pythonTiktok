from labelme import utils
import json
import copy
import os
import io
import PIL
import codecs
import base64

class BaseSaveLabelMe():

    def __init__(self,name):
        self.name = name
        self.initdata()
    def initdata(self):
        print('BaseSaveLabelMe')

    def encodeImageForJson(self,image):
        img_pil = PIL.Image.fromarray(image, mode='RGB')
        f = io.BytesIO()
        img_pil.save(f, format='PNG')
        data = f.getvalue()
        encData = codecs.encode(data, 'base64').decode()
        encData = encData.replace('\n', '')
        return encData
    def saveLabelJosn(self,url:str,img,box):

        _outObj={}
        _outObj["version"] = "5.3.1"
        _outObj["flags"] = {}
        _outObj["imagePath"]="sheep0013.jpg"
        _outObj["imageHeight"] = 1080
        _outObj["imageWidth"] = 1920

        dir_path = os.path.dirname(url)  # 获取路径名，删掉文件名

        _imageData=utils.img_arr_to_b64(img).decode('utf-8')




        if _outObj:

            a = base64.b64encode(img)
            b = self.encodeImageForJson(img)

            _outObj["imagePath"]=os.path.basename(url)
            _outObj["shapes"]=[]
            _outObj["imageData"]=b

            for obj in box:

                _vo={}
                _vo["group_id"] = None
                _vo["label"] = 'sheep'
                _vo["description"] = ""
                _vo["shape_type"] = "rectangle"
                _vo["flags"] = {}

                x0 = round(obj["bbox"][0])
                y0 = round(obj["bbox"][1])
                x1 = round(obj["bbox"][2])
                y1 = round(obj["bbox"][3])

                if obj["rect"] is not None:
                    x0+=  obj["rect"][0]
                    y0+=  obj["rect"][1]
                    x1+=  obj["rect"][0]
                    y1+=  obj["rect"][1]


                id = int(obj["id"])
                class_name = obj["class"]

                confi = float(obj["confidence"])

                print(class_name)
                print(confi)

                _vo['points']=[[x0, y0], [x1, y1]]

                # if class_name =='sheep' or class_name =='horse' or class_name =='dog':
                _outObj['shapes'].append(_vo)




            _txtUrl = url.replace('.jpg', '.json')
            if os.path.exists(_txtUrl):
                print("文件存在")
            else:
                print("写入文件",_txtUrl)
                with open(_txtUrl, 'w') as f:
                    f.write(json.dumps(_outObj))










