import time
from socket import  *
import numpy
import cv2
import mss
#主机地址为0.0.0.0，表示绑定本机的所有网络接口ip地址
import numpy as np
import struct
IP = "0.0.0.0"
PORT = 80
#定义一次从socket缓冲区最多读入1024个字节数据
BUFLEN = 1024

#实例化一个socket对象
listenSocket = socket(AF_INET, SOCK_STREAM)

#Socket绑定地址和端口号
listenSocket.bind((IP, PORT))

#使socket处于监听状态,等待客户端的连接请求,参数5代表最多可以连接客户端的数量
listenSocket.listen(5)
print(f"服务器端启动成功,在{PORT}端口等待客户端连接...")
dataSocket , addr = listenSocket.accept()
print("接受一个客户端连接",addr)
monitor = {"top":0, "left":0, "width":800, "height":700}
while True:
    #尝试读取对方发生的消息
    #recved  = dataSocket.recv(BUFLEN)
    time.sleep(0.05)
    with mss.mss() as sct:
        sreeen_area = sct.grab(monitor)
        img_array = np.array(sreeen_area)
        img_cv = cv2.cvtColor(img_array, cv2.COLOR_RGBA2RGB)
    _, encode_cv = cv2.imencode(".jpg", img_cv, [cv2.IMWRITE_JPEG_QUALITY, 80])
    decode_cv = cv2.imdecode(encode_cv, cv2.IMREAD_COLOR)
    branry_pack = struct.pack(">BI", 1, len(encode_cv))
    print("二进制打包数据",branry_pack)
    try:
        dataSocket.settimeout(5)
        dataSocket.sendall(branry_pack)
        dataSocket.sendall(encode_cv)
    except Exception as e:
        print("发送数据时出现错误",e)
        #关闭socket通信
        dataSocket.close()
        #等待新的客户端连接
        dataSocket, addr = listenSocket.accept()
        print("接受了一个客户端连接",dataSocket,addr)
    #cv2.imshow("decode_cv", decode_cv)

    # if cv2.waitKey(20) & 0xff == ord('q'):
    #     cv2.destroyWindow()
    #     break
    # if not recved:
    #     print("客户端关闭了连接")
    #     break
    #读取客户端的数据,需要解码为bytes类型
    #info  =recved.decode()
    #print(f"接收对方信息:{info}")

