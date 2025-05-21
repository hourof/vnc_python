import cv2
import  mss
import  os
import numpy as np
template = os.listdir("img")
#找图函数
def templatea(img, template):
    a =os.listdir("img")
    #print(a,len(a))
    img_list = []
    #扫描列表里的图像
    for i,item in enumerate(a, start=1):
        img1 = os.path.join("img", item)
        #print(f"{i}",img1)
        img2 = cv2.imread(img1)
        #获取模板尺寸
        _,w, h = img2.shape[::-1]
        result = cv2.matchTemplate(img,img2,cv2.TM_CCOEFF_NORMED)
        threshold = 0.8
        loc = np.where(result >= threshold)
        #print(loc)
        #当有模板匹配到了图片loc[0]里面就有数据了,就可以处理逻辑了
        if len(loc[0]) >0:
            new_filename = img1.lstrip("img\\")
            img_list.append(new_filename)
            #print("图像名字",new_filename)
            # 在主图上绘制匹配框
            for pt in zip(*loc[::-1]):
                cv2.rectangle(img, pt, (pt[0] + w, pt[1] + h), (255, 0, 0), 2)
    return  img_list

#处理任务逻辑
class Automatic_task:
    #__init__()是类的构造函数，每当你创建类的实例时，它就会被自动调用。它的作用是初始化对象的属性
    def __init__(self):
        #super() 用于 调用父类的方法，特别是在继承时很有用。例如
        super().__init__()

    # 1.判断一下目前是哪张地图
    # 2.判断地图等级
    # 3.判断在地图里的那一个房间
    # 4.执行打怪任务
    # 5.执行拾取物品任务
    # 6.进入下一张地图
    pass
