#控制端的代码   ctrl
import tkinter
import tkinter.messagebox
import struct
import socket
import numpy as np
from PIL import Image, ImageTk
import threading
import re
import cv2
import time
import sys
import platform
from yolov5.yolov5_fp32 import  YOLOv7
#ip地址
ip_address = "192.168.5.2:80"
#创建主窗口
root = tkinter.Tk()
# 加载模型路径
model_path = "../model/best.onnx"

# 设置置信度和 IOU 阈值
confThreshold = 0.3
nmsThreshold = 0.5

# 初始化 YOLOv7 检测器
yolov7_detector = YOLOv7(model_path, confThreshold, nmsThreshold)
# 画面周期
IDLE = 0.05

# 放缩大小
scale = 1

# 原传输画面尺寸
fixw, fixh = 0, 0

# 放缩标志
wscale = False

# 屏幕显示画布
showcan = None

# socket缓冲区大小
bufsize = 10240

# 线程
th = None

# socket
soc = None

# socks5

socks5 = None



# 平台
PLAT = b''
#检测是什么操作系统
if sys.platform == "win32":
    PLAT = b'win'
elif sys.platform == "darwin":
    PLAT = b'osx'
elif platform.system() == "Linux":
    PLAT = b'x11'

# 初始化socket


def SetSocket():
    global soc, host_en

    """
    该函数将 IPv4 地址和端口打包成 Socks5 协议格式的二进制数据
    5, 1, 0, 1: Socks5 协议的版本、命令、保留字段和地址类型
    ip[0], ip[1], ip[2], ip[3]: IP 地址的四个字节
    port: 端口号
    """
    def byipv4(ip, port):
        return struct.pack(">BBBBBBBBH", 5, 1, 0, 1, ip[0], ip[1], ip[2], ip[3], port)
    """
    该函数将域名和端口打包成 Socks5 协议格式的二进制数据
    5, 1, 0, 3: Socks5 协议的版本、命令、保留字段和地址类型
    blen: 域名的长度
    host.encode(): 域名的字节表示
    """
    def byhost(host, port):
        d = struct.pack(">BBBB", 5, 1, 0, 3)
        blen = len(host)
        d += struct.pack(">B", blen)
        d += host.encode()
        d += struct.pack(">H", port)
        return d
    """
    从 host_en 获取主机地址，并检查其格式。如果格式不正确，则显示错误信息并返回
    """
    host = host_en.get()
    if host is None:
        tkinter.messagebox.showinfo('提示', 'Host设置错误！')
        return
    hs = host.split(":")
    if len(hs) != 2:
        tkinter.messagebox.showinfo('提示', 'Host设置错误！')
        return
    #检查并解析 Socks5 代理地址。如果格式不正确，则显示错误信息并返回
    if socks5 is not None:
        ss = socks5.split(":")
        if len(ss) != 2:
            tkinter.messagebox.showinfo('提示', '代理设置错误！')
            return
        #创建一个 TCP 套接字，并连接到 Socks5 代理服务器。然后发送 Socks5 握手请求并接收响应。如果代理响应错误，则显示错误信息并返回
        soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        soc.connect((ss[0], int(ss[1])))
        soc.sendall(struct.pack(">BB", 5, 0))
        recv = soc.recv(2)
        if recv[1] != 0:
            tkinter.messagebox.showinfo('提示', '代理回应错误！')
            return
        #根据主机地址的类型（IP 或域名），使用相应的辅助函数 byhost 或 byipv4 打包连接请求，并发送给 Socks5 代理服务器
        if re.match(r'^\d+?\.\d+?\.\d+?\.\d+?:\d+$', host) is None:
            # host 域名访问
            hand = byhost(hs[0], int(hs[1]))
            soc.sendall(hand)
        else:
            # host ip访问
            ip = [int(i) for i in hs[0].split(".")]
            port = int(hs[1])
            hand = byipv4(ip, port)
            soc.sendall(hand)
        # 代理回应
        #接收代理服务器的回应，并检查是否成功连接。如果代理回应错误，则显示错误信息并返回。
        rcv = b''
        while len(rcv) != 10:
            rcv += soc.recv(10-len(rcv))
        if rcv[1] != 0:
            tkinter.messagebox.showinfo('提示', '代理回应错误！')
            return
    else:
        #如果没有设置代理，直接创建一个 TCP 套接字并连接到主机。
        soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        soc.connect((hs[0], int(hs[1])))

#这个函数 SetScale(x) 的作用是设置缩放比例并标记缩放状态
def SetScale(x):
    global scale, wscale
    scale = float(x) / 100
    wscale = True

#这个函数 ShowProxy() 的作用是显示一个用于设置 Socks5 代理的对话框窗口。让我们逐行解析一下这段代码
def ShowProxy():
    # 显示代理设置
    global root
    #定义一个嵌套函数 set_s5_addr，用于获取用户输入的 Socks5 代理地址并保存。如果输入为空，则将 socks5 设置为 None。最后销毁窗口
    def set_s5_addr():
        global socks5
        socks5 = s5_en.get()
        if socks5 == "":
            socks5 = None
        pr.destroy()
    print("我被调用了")
    #创建一个新的顶级窗口 pr，作为设置 Socks5 代理的对话框。顶级窗口是一个独立的窗口，相对于主窗口 root
    pr = tkinter.Toplevel(root)
    #创建一个 StringVar 对象 s5v，用于存储和管理 Tkinter 小部件的字符串值
    s5v = tkinter.StringVar()
    #创建一个标签 s5_lab，显示文本 "Socks5 Host:"
    s5_lab = tkinter.Label(pr, text="Socks5 Host:")
    #创建一个文本输入框 s5_en，用于用户输入 Socks5 代理地址。输入框的文本内容由 StringVar 对象 s5v 管理
    s5_en = tkinter.Entry(pr, show=None, font=('Arial', 14), textvariable=s5v)
    #创建一个按钮 s5_btn，显示文本 "OK"。点击按钮时，将调用 set_s5_addr 函数
    s5_btn = tkinter.Button(pr, text="OK", command=set_s5_addr)
    #使用网格布局管理器 (grid)，将标签、输入框和按钮放置在顶级窗口 pr 中，并设置它们的布局参数和内外填充
    s5_lab.grid(row=0, column=0, padx=10, pady=10, ipadx=0, ipady=0)
    s5_en.grid(row=0, column=1, padx=10, pady=10, ipadx=40, ipady=0)
    s5_btn.grid(row=1, column=0, padx=10, pady=10, ipadx=30, ipady=0)
    #设置 StringVar 对象 s5v 的初始值为 "127.0.0.1:88"，这将显示在输入框 s5_en 中
    s5v.set(ip_address)

#函数 ShowScreen() 主要用于显示或关闭一个屏幕窗口，并控制相关的线程
def ShowScreen():
    global showcan, root, soc, th, wscale
    # if showcan is None:：检查 showcan 是否为 None，即当前没有显示窗口
    if showcan is None:
        #wscale = True：设置全局变量 wscale 为 True，表示需要重新设置缩放比例
        wscale = True
        #showcan = tkinter.Toplevel(root)：创建一个新的顶级窗口 showcan，作为主窗口 root 的子窗口
        showcan = tkinter.Toplevel(root)
        #th = threading.Thread(target=run)：创建一个新的线程 th，该线程将运行目标函数 run
        th = threading.Thread(target=run)
        #启动新创建的线程 th，开始执行 run 函数
        th.start()
    #else:：如果 showcan 不为 None，即当前已经有显示窗口
    else:
        #soc.close()：关闭套接字 soc，终止网络连接
        soc.close()
        #showcan.destroy()：销毁 showcan 窗口，关闭显示窗口
        showcan.destroy()

#创建一个 StringVar 对象 val，用于存储和管理 Tkinter 小部件的字符串值
val = tkinter.StringVar()
#host_lab：创建一个标签 host_lab，显示文本 "Host:"
host_lab = tkinter.Label(root, text="Host:")
#host_en：创建一个输入框 host_en，用于用户输入主机地址，输入框的内容由 StringVar 对象 val 管理，字体为 Arial，大小 14
host_en = tkinter.Entry(root, show=None, font=('Arial', 14), textvariable=val)
sca_lab = tkinter.Label(root, text="Scale:")
#sca：创建一个滑动条 sca，范围从 10 到 100，方向为水平，长度为 100，显示当前值，分辨率为 0.1，刻度间隔为 50，改变值时调用 SetScale 函数
sca = tkinter.Scale(root, from_=10, to=100, orient=tkinter.HORIZONTAL, length=100,
                    showvalue=100, resolution=0.1, tickinterval=50, command=SetScale)
proxy_btn = tkinter.Button(root, text="Proxy", command=ShowProxy)
show_btn = tkinter.Button(root, text="Show", command=ShowScreen)

host_lab.grid(row=0, column=0, padx=10, pady=10, ipadx=0, ipady=0)
host_en.grid(row=0, column=1, padx=0, pady=0, ipadx=40, ipady=0)
sca_lab.grid(row=1, column=0, padx=10, pady=10, ipadx=0, ipady=0)
sca.grid(row=1, column=1, padx=0, pady=0, ipadx=100, ipady=0)
proxy_btn.grid(row=2, column=0, padx=0, pady=10, ipadx=30, ipady=0)
show_btn.grid(row=2, column=1, padx=0, pady=10, ipadx=30, ipady=0)
sca.set(100)
val.set(ip_address)

last_send = time.time()
def run():
    global wscale, fixh, fixw, soc, showcan
    SetSocket()
    # 发送平台信息
    soc.sendall(PLAT)
    lenb = soc.recv(5)
    imtype, le = struct.unpack(">BI", lenb)
    imb = b''
    while le > bufsize:
        t = soc.recv(bufsize)
        imb += t
        le -= len(t)
    while le > 0:
        t = soc.recv(le)
        imb += t
        le -= len(t)
    data = np.frombuffer(imb, dtype=np.uint8)
    img = cv2.imdecode(data, cv2.IMREAD_COLOR)
    h, w, _ = img.shape
    fixh, fixw = h, w
    imsh = cv2.cvtColor(img, cv2.COLOR_RGBA2RGB)
    imi = Image.fromarray(imsh)
    imgTK = ImageTk.PhotoImage(image=imi)
    cv = tkinter.Canvas(showcan, width=w, height=h, bg="white")
    cv.focus_set()
    cv.pack()
    cv.create_image(0, 0, anchor=tkinter.NW, image=imgTK)
    h = int(h * scale)
    w = int(w * scale)
    while True:
        if wscale:
            h = int(fixh * scale)
            w = int(fixw * scale)
            cv.config(width=w, height=h)
            wscale = False
        try:
            lenb = soc.recv(5)
            imtype, le = struct.unpack(">BI", lenb)
            imb = b''
            while le > bufsize:
                t = soc.recv(bufsize)
                imb += t
                le -= len(t)
            while le > 0:
                t = soc.recv(le)
                imb += t
                le -= len(t)
            data = np.frombuffer(imb, dtype=np.uint8)
            ims = cv2.imdecode(data, cv2.IMREAD_COLOR)
            if imtype == 1:
                # 全传
                img = ims
            else:
                # 差异传
                img = img ^ ims
            imt = cv2.resize(img, (w, h))
            imsh = cv2.cvtColor(imt, cv2.COLOR_RGBA2RGB)
            cv2.imshow("img",imsh)
            if cv2.waitKey(10) &0xff == ord('q'):
                break
            # 使用 YOLOv7 进行推理
            #boxes, scores, class_ids = yolov7_detector.detect(img)

            # 绘制检测框
            #dstimg = yolov7_detector.draw_detections(img, boxes, scores, class_ids)
            imi = Image.fromarray(imsh)
            imgTK.paste(imi)
        except:
            showcan = None
            ShowScreen()
            return


root.mainloop()
