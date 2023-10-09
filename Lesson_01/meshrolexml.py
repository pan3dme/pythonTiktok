import math


class MeshRoleXml():
    __instance = None

    def __init__(self):
        if MeshRoleXml.__instance is None:
            MeshRoleXml.__instance = self
        else:
            raise Exception("Singleton class instantiated more than once")

            # 记录所有数据
            self.roleDic = {}
            # 记录判断确定是羊的id
            self.rightItem = []

    def clearData(self):
        # 记录所有数据
        self.roleDic = {}
        # 记录判断确定是羊的id
        self.rightItem = []
        print('MeshRoleXml,clearData')

    def pushXmlData(self,value):

        for obj in value:
            id = int(obj["id"])
            # x0 = round(obj["bbox"][0])
            # y0 = round(obj["bbox"][1])
            # x1 = round(obj["bbox"][2])
            # y1 = round(obj["bbox"][3])
            # if obj["rect"] is not None:
            #     x0 += obj["rect"][0]
            #     y0 += obj["rect"][1]
            #     x1 += obj["rect"][0]
            #     y1 += obj["rect"][1]
            # class_name = obj["class"]
            # confi = float(obj["confidence"])
            # image_id = float(obj["image_id"])

            if not (id in self.roleDic):
                self.roleDic[id]=[]
            self.roleDic[id].append(obj)


        for id in self.roleDic:
            if not (id in self.rightItem):
                tempArr=self.roleDic[id]
                if(len(tempArr)>5):
                    if self.isTureRitheRoldByArr(tempArr,id):
                        self.rightItem.append(id)
            else:
                pass

        # print('---------------------------')
        # print(self.rightItem)

    #判断指定路劲在一个轨迹上
    def isTureRitheRoldByArr(self, arr,id):
        lasPos=None
        totalDis=0
        for obj in arr:
            x0 = round(obj["bbox"][0])
            y0 = round(obj["bbox"][1])
            x1 = round(obj["bbox"][2])
            y1 = round(obj["bbox"][3])
            if lasPos is not None:
                (nx,ny)=((x1-x0)/2.0,(y1-y0)/2.0)
                (ox,oy)=lasPos
                d = math.sqrt(math.pow((nx - ox), 2) + math.pow((ny - oy), 2))
                totalDis+=d
            lasPos=((x1-x0)/2.0,(y1-y0)/2.0)

            id = int(obj["id"])



        if  totalDis>20:
            print( '编号为 ',id,"两点间的距离为:{:.2f}".format(totalDis))
            print('---------------------------',len(arr),'核对数量',len(self.rightItem))
        return  totalDis>20

    @staticmethod
    def get_instance():
        if not MeshRoleXml.__instance:
            MeshRoleXml()
        return MeshRoleXml.__instance

