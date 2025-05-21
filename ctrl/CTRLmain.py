import socket
import pickle
import cv2
from yolov5 import  yolov5_fp32
import numpy as np
IP = "192.168.5.2"
PORT = 800
# 创建客户端 Socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((IP, PORT))  # 连接到服务器

print("已连接到服务器")
model = "../model/best.onnx"
confThreshold = 0.3
nmsThreshold = 0.5
yolov7_detector = yolov5_fp32.YOLOv7(model, confThreshold, nmsThreshold)
while True:
    # 接收数据长度
    data_length = int.from_bytes(client_socket.recv(4), 'big')

    # 接收图像数据
    data = b""
    while len(data) < data_length:
        packet = client_socket.recv(data_length - len(data))
        if not packet:
            break
        data += packet

    # 反序列化图像数据
    img_bgr = pickle.loads(data)
    boxes, scores, class_ids = yolov7_detector(img_bgr)
    # 显示接收到的图像
    cv2.imshow("Received Image", img_bgr)

    if cv2.waitKey(1) == 27:  # 按 ESC 键退出
        break

client_socket.close()
cv2.destroyAllWindows()
