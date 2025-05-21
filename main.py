import cv2
import numpy as np
import time
import  os
import  threading
from findpic import templatea
from yolov5.yolov5_fp32 import YOLOv7
from paddleocr import PaddleOCR
#ocr = PaddleOCR(use_angle_cls=True, use_gpu=False, lang="ch")
# def ocr_image(img):
#     list = []
#     result = ocr.ocr(img, cls=True)
#     if result == [None]:
#         print("打印")
#         return 0
#     if result:
#         for line in result:
#             for item in line:
#                 if len(item) >= 2:
#                     text, confidence = item[1]
#                     print(f"文字: {text}, 置信度: {confidence}")
#
#     return list

#cap = cv2.VideoCapture(0)
cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)  # Windows 用户可以试试 DirectShow
cap.set(cv2.CAP_PROP_FPS, 30)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)
if not cap.isOpened():
    print("无法打开摄像头")
    exit()
#初始化帧计数器和起始时间
frame_count = 0
# start_time的值是时间戳
start_time = time.time()

# 加载模型路径
model_path = "model/best.onnx"
# 设置置信度和 IOU 阈值
confThreshold = 0.7
nmsThreshold = 0.5
# 初始化 YOLOv7 检测器
yolov7_detector = YOLOv7(model_path, confThreshold, nmsThreshold)
template = os.listdir("img")
#看一下是否判断当前地图的地图名
ocr_flag =0
# 定义映射关系
map_names = {
    "qiandian.png": "当前地图名称为:幻境前殿",
    "cangchi.png": "当前地图名称为:仓持竹林",
    "weiyang.png": "当前地图名称为:未央之脊",
    "canyue.png": "当前地图名称为:残月宫阙",
}
while True:
    #读取一帧
    ret, frame = cap.read ()
    if not ret:
        print("无法读取视频帧")
        break
    #增加帧计数
    frame_count +=  1

    #计算经过的时间
    elapsed_time = time.time() - start_time
    fps = frame_count / elapsed_time
    # 从左上角截取800*600的区域
    cropped_frame = frame[0:600, 0:800]
    # 使用 YOLOv7 进行推理
    boxes, scores, class_ids = yolov7_detector.detect(cropped_frame)
    # 绘制检测框
    dstimg,target_list = yolov7_detector.draw_detections(cropped_frame, boxes, scores, class_ids)
    #生成roi区域 该区域用ocr来判断我们进的是哪张地图
    roi_map = dstimg[0: 120,600:790]
    #存放着所有模板匹配到的图像
    temp_list= templatea(roi_map,template)
    print(f"模板匹配列表{temp_list}")
    #查找模板图像中的人物
    if "xiaoperson.png" in temp_list:
        print("执行过图逻辑")
        #1.判断一下目前是哪张地图
        #2.判断地图等级
        #3.判断在地图里的那一个房间
        #4.执行打怪任务
        #5.执行拾取物品任务
        #6.进入下一张地图
        if "xia.png" in temp_list:
            print("进入下一张地图")
    if "uotu.png" in temp_list:
        print("放入思南再次挑战")

    cv2.imshow("ror",roi_map)
    cv2.rectangle(dstimg, (662,0),(783,25),(0,0,255), 1)
    #存放着模型名字和坐标
    print(target_list)
    # 为了让观察效果更直观，将当前 FPS 和相机参数信息绘制到图像上
    cv2.putText(cropped_frame, "FPS: {:.2f}".format(fps), (10, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    #显示图像
    cv2.imshow("yolo", dstimg)
    #按q建退出循环
    if cv2.waitKey(500) & 0xff == ord('q'):
        break
#释放视像头资源
cap.release()
#释放opencv
cv2.destroyAllWindows()

