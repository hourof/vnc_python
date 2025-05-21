import socket
import struct

import mss
import cv2
import numpy as np
import threading
import time

#画面周期
IDLE =0.05

bufsize = 1024
host = ("0.0.0.0", 80)  # Correct IP for binding
#创建一个套接字对象
soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#将套接字对象绑定到地址HOST上
soc.bind(host)

#告诉套接字开始监听来自客户端的连接请求
soc.listen(1)

#压缩包 1-100 数值越小,压缩比越高，图片质量损失越严重
IMQUALTTY = 40

#创建一个锁对象，该对象在多线程编程中用于同步线程
lock = threading.Lock()

#压缩后np图像
img =None

#编码后的图像
imbyt = None
monitor = {"top": 0, "left": 0, "width": 400, "height": 400}
#定义图像处理函数
def handle(conn =1):
    global  img, imbyt
    reduce_img = None
    if imbyt is None:
        with mss.mss() as sct:
            screenshot = sct.grab(monitor)
            #将mss的截图转换成numpy数组
            scrimg = np.array(screenshot)
            _, reduce_img = cv2.imencode(".jpg", scrimg, [cv2.IMWRITE_JPEG_QUALITY, IMQUALTTY])
            #将一个编码后的数据解码为opencv图像
            img = cv2.imdecode(reduce_img, cv2.IMREAD_COLOR)
            cv2.imshow("imbyt", img)
            #将数据打包成二进制
            lenb =struct.pack(">BI", 1, len(reduce_img))
            flag,lentth = struct.unpack(">BI",lenb)
            cv2.imshow("ia",flag)
            #发生打包的二进制数据
            #conn.sendall(lenb)
            #发送压缩后的数据
            #conn.sendall(reduce_img)
            #cv2.imshow("img", scrimg)
            if cv2.waitKey(20) &0xff == ord("q"):
                return  False
    return  True
while True:

    if not handle():
        break
    time.sleep(IDLE)