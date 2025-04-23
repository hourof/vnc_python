#截屏本机的代码   bectrl   启动服务器
import struct
import socket
from PIL import ImageGrab
import cv2
import numpy as np
import threading
import time
import pyautogui as ag
import mouse
from _keyboard import getKeycodeMapping

# 画面周期
IDLE = 0.05

# 鼠标滚轮灵敏度
SCROLL_NUM = 5

bufsize = 1024

host = ('0.0.0.0', 80)
"""
socket.socket(): 创建一个新的套接字对象。

socket.AF_INET: 指定套接字使用 IPv4 协议。

socket.SOCK_STREAM: 指定套接字使用 TCP 协议。
"""
soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#的作用是将套接字绑定到一个特定的地址和端口上，使得这个套接字可以监听来自该地址和端口的连接请求。
# 在你的代码中，这行代码将套接字 soc 绑定到地址 ('0.0.0.0', 80) 上
soc.bind(host)
#soc.listen(1) 是在告诉套接字开始监听来自客户端的连接请求。这行代码的具体作用是
soc.listen(1)
# 压缩比 1-100 数值越小，压缩比越高，图片质量损失越严重
IMQUALITY = 80
#是创建一个新的锁对象，该对象在多线程编程中用于同步线程
lock = threading.Lock()


# 压缩后np图像
img = None
# 编码后的图像
imbyt = None
#定义图像处理函数
def handle(conn):
    global img, imbyt
    #是在多线程编程中用于获取锁的函数。它确保在某一时刻，只有一个线程可以进入被锁保护的临界区
    lock.acquire()
    #if imbyt is None: 是一个条件判断语句，用于检查变量 imbyt 是否为 None
    if imbyt is None:
        screen_area = (0, 0, 800, 600)
        #ImageGrab.grab()用来截取屏幕，他来自pIL库然后转换成numpy数组

        imorg = np.asarray(ImageGrab.grab(screen_area))
        """
        cv2.imencode：这是 OpenCV 库中的一个函数，用于将图像编码为特定格式的文件
        .jpg：指定要将图像编码为 JPEG 格式
        imorg：这是要编码的图像数据，通常是一个 NumPy 数组
        [cv2.IMWRITE_JPEG_QUALITY, IMQUALITY]：这是一个可选参数，用于指定编码质量。
        IMQUALITY 变量定义了 JPEG 压缩质量（从 0 到 100，值越大质量越高）
        返回值:
            _：这是函数的第一个返回值，表示操作是否成功（通常我们忽略这个值，所以用 _ 表示）
            imbyt：这是函数的第二个返回值，是一个包含编码后图像的字节数组
        """
        _, imbyt = cv2.imencode(".jpg", imorg, [cv2.IMWRITE_JPEG_QUALITY, IMQUALITY])
        #将图像数据转换成为一个无符号8位数的整形,转换成numpy数组
        imnp = np.asarray(imbyt, np.uint8)
        #将一个编码后的图像字节数组解码为一个 OpenCV 图像
        #cv2.IMREAD_COLOR:这是一个标志，指定解码图像为彩色图像。OpenCV 默认会将图像解码为 BGR 格式的彩色图像（蓝-绿-红）
        img = cv2.imdecode(imnp, cv2.IMREAD_COLOR)
    #是用于释放先前获取的锁
    lock.release()
    """
    将数据打包成二进制格式
    ">BI":
        >：表示数据采用大端（big-endian）字节顺序。
        B：表示一个无符号的8位整数（unsigned char）
        I：表示一个无符号的32位整数（unsigned int
        1:这是要打包的第一个值，它是一个无符号的8位整数，值为 1
        len(imbyt):获取数据长度,这个值将被打包为无符号的32位整数
    """
    lenb = struct.pack(">BI", 1, len(imbyt))
    #用于通过套接字连接发送数据的一行代码。具体来说，它将 lenb 中的所有字节数据发送到连接的另一端
    #lenb是打包成二进制的数据
    conn.sendall(lenb)
    #imbyt是原始数据
    conn.sendall(imbyt)
    while True:
        # fix for linux
        #以秒为单位延时0.05秒
        time.sleep(IDLE)
        #截取屏幕
        gb = ImageGrab.grab(screen_area)
        #转换成np数组
        imgnpn = np.asarray(gb)
        #将图像编码
        _, timbyt = cv2.imencode(
            ".jpg", imgnpn, [cv2.IMWRITE_JPEG_QUALITY, IMQUALITY])
        imnp = np.asarray(timbyt, np.uint8)
        #编码后的数据解码成opencv数据
        imgnew = cv2.imdecode(imnp, cv2.IMREAD_COLOR)
        # 计算图像差值
        #异或操作符 ^ 用于比较两个二进制数的每个位。如果两个对应的位不同，则结果为 1，否则为 0 例如：1010 ^ 1100 = 0110
        imgs = imgnew ^ img
        #any是numpy的一个方法,如果数组中至少有一个 True 元素，.any() 返回 True，否则返回 False
        if (imgs != 0).any():
            # 画质改变
            #pass 语句是一个占位符，用于在语法上需要语句但实际上不需要执行任何操作的地方
            pass
        else:
            #当循环遇到 continue 语句时，会跳过当前的迭代，直接开始下一次迭代
            continue
        imbyt = timbyt
        img = imgnew
        # 无损压缩
        _, imb = cv2.imencode(".png", imgs)
        l1 = len(imbyt)  # 原图像大小
        l2 = len(imb)  # 差异图像大小
        if l1 > l2:
            # 传差异化图像
            lenb = struct.pack(">BI", 0, l2)
            conn.sendall(lenb)
            conn.sendall(imb)
        else:
            # 传原编码图像
            lenb = struct.pack(">BI", 1, l1)
            conn.sendall(lenb)
            conn.sendall(imbyt)


while True:
    conn, addr = soc.accept()
    threading.Thread(target=handle, args=(conn,)).start()
