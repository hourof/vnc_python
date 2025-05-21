import socket
import struct
import threading
import tkinter
import cv2
import numpy as np
from PIL import  Image, ImageTk
#"192.168.5.2:80" 这是宏基那台电脑的地址
ip_address = "127.0.0.1:80"
# "127.0.0.1:88" 这是本机ip地址
root = tkinter.Tk()

#放缩标志
wscale = False
#放缩大小
scale = 1

# 屏幕显示画布   Node代表没有打开cv窗体,True代表打开
showcan =None

# 线程
th = None

# socket接口
soc = None

#socks5接口
socks5 = None

# 原传输画面尺寸
fixw, fixh = 0, 0

#数据缓存区
bufsize = 10240
#滚动条事件函数
def SetScale():
    print("滚动条在滚动")
    #pass

#SetSocket函数 启动socket通信
def SetSocket():
    global  soc, host_en
    #host存放id地址信息  ip_address = "192.168.5.2:80"
    host = host_en.get()
    print(host)
    if host is None:
        #会在控制台输出错误信息
        tkinter.messagebox.showinfo('提示', "Host设置错误")
        return
    #以：分割host
    hs = host.split(":")
    print(hs,type(hs))
    if len(hs) != 2:
        tkinter.messagebox.showinfo("提示", "Host设置错误")
        return
    #检测socks5是否不等于None
    if socks5 is not None:
        ss = socks5.split(":")
        print("代理设置错误")
    else:
        print("启动了socket通信")
        #如果没有设置代理,直接创建一个Tcp套接字并连接到主机
        #创建Tcp socket对象
        soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        #连接到服务器
        soc.connect((hs[0], int(hs[1])))
        print(soc)

#proxy代理按钮事件
def ShowProxy():
    print("代理窗口被打开了")
host_label = tkinter.Label(root, text="Host:")
host_label.grid(row=0, column=0, padx=10, pady=10, ipadx=0, ipady=0)


#显示画面按钮事件
def ShowScreen():
    global showcan, root, soc, th, wscale
    if showcan is None or not showcan.winfo_exists():
        wscale = True
        #创建一个新的窗口,用于显示画面
        showcan = tkinter.Toplevel(root)
        showcan.title("远程画布")
        #创建一个新的线程,该函数将执行run函数
        th = threading.Thread(target= run)
        th.start()
    pass

#显示画面线程,用于程序不会卡死
def run():
    print("开启了run函数")
    global wscale, fixh, fixw, soc, showcan,tk_image
    #启动socket通信
    SetSocket()
    # 构造要发送的数据（作为示例发送一个字符串）
    print(soc)
    message = "Hello, Server!"
    soc.sendall(message.encode())

    #接收服务器返回的数据,最大接收1024
    lenb = soc.recv(5)
    print("打包后的数据",lenb)
    #解包
    imtype, le = struct.unpack(">BI", lenb)
    print("解包后的数据",imtype,"le数据:", le)
    imb = b""
    while le > bufsize:
        t = soc.recv(le)
        #print("图像数据",t)
        imb += t
        le -= len(t)
    while le > 0:
        t = soc.recv(le)
        imb += t
        le -= len(t)
    data = np.frombuffer(imb, dtype=np.uint8)
    print( "data数据",data)
    decode_cv = cv2.imdecode(data, cv2.IMREAD_COLOR)
    h,w, _ = decode_cv.shape
    fixh, fixw = h, w
    img = cv2.cvtColor(decode_cv, cv2.COLOR_BGR2RGB)
    #cv2.imshow("img", img)
    #cv2.waitKey(0)
    pil_image = Image.fromarray(img)
    tk_image = ImageTk.PhotoImage(image= pil_image)
    #创建一个 Canvas 画布，并将其放置在 showcan 窗口中 bg="white" 设置背景为 白色
    cv = tkinter.Canvas(showcan, width= w, height=h , bg= "white")
    #将焦点设置到 cv 组件，这样它可以接收键盘事件
    cv.focus_set()
    #将 cv 组件添加到 showcan 窗口，并自动调整位置和大小
    cv.pack()
    #在 Canvas 画布上绘制图像：(0, 0): 让图像的左上角对齐到画布的 (0, 0) 位置。anchor=tkinter.NW: 让图像的 左上角 对齐 Canvas 画布的左上角。image=tk_image: tk_image 变量（ImageTk.PhotoImage 格式）存储了你要显示的图像。
    cv.create_image(0, 0, anchor = tkinter.NW, image = tk_image)
    h = int(h * scale)
    w = int(w * scale)
    while True:
        if wscale:
            h = int(fixh * scale)
            w = int(fixw * scale)
            #动态调整 Canvas 画布的大小。
            cv.config(width= w, height=h)
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
            data  = np.frombuffer(imb, dtype= np.uint8)
            ims = cv2.imdecode(data, cv2.IMREAD_COLOR)
            if imtype == 1:
                #全传
                img = ims
            else:
                #差异传
                img = img ^ ims
            imt = cv2.resize(img, (w,h))
            imsh = cv2.cvtColor(imt, cv2.COLOR_BGR2RGB)
            imi = Image.fromarray(imsh)
            tk_image.paste(imi)
        except:
            showcan = None
            ShowScreen()
            return
#创建一个字符串,用于存储和管理Tkinter小部件的字符串值
val =tkinter.StringVar()
#创建一个输入框
host_en = tkinter.Entry(root, show=None, font=('Arial',14), textvariable= val)
host_en.grid(row=0, column=1, padx=0, pady=0, ipadx=50, ipady=0)
val.set(ip_address)

#滚动条标题
sca_lab = tkinter.Label(root, text="Scale:")
sca_lab.grid(row=1, column=0, padx=10, pady=10,ipadx=0, ipady= 0)
#创建一个滚动条
sca = tkinter.Scale(root, from_= 10, to= 100, orient= tkinter.HORIZONTAL, length= 100,
                    showvalue=100, resolution=0.1, tickinterval=50, command= SetScale)
#滚动条默认值
sca.set(100)
sca.grid(row=1, column=1, padx=0, pady=0, ipadx=100, ipady= 0)

#代理窗口按钮
proxy_btn = tkinter.Button(root, text="Proxy", command= ShowProxy)
proxy_btn.grid(row=2, column=0, padx=0, pady= 10, ipadx= 30, ipady= 0)

#显示画面按钮
show_btn = tkinter.Button(root, text="Show", command= ShowScreen)
show_btn.grid(row=2, column=1, padx=0, pady=10, ipadx=30, ipady=0)
root.mainloop()