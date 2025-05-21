import cv2
import numpy as np
import time

def nothing(x):
    # Trackbar 的回调函数（这里不做任何操作）
    pass

def adjust_brightness_contrast(image, brightness=0, contrast=1.0):
    """
    调整图像的亮度和对比度
    :param image: 输入图像
    :param brightness: 亮度偏移，正值增加亮度，负值降低亮度
    :param contrast: 对比度系数，1.0表示无改变
    :return: 调整后的图像
    """
    # 利用 cv2.convertScaleAbs 对图像做线性变换: new_image = image * alpha + beta
    # 其中 alpha 为对比度系数，beta 为亮度偏移
    return cv2.convertScaleAbs(image, alpha=contrast, beta=brightness)

def adjust_saturation(image, saturation_scale=1.0):
    """
    调整图像的饱和度
    :param image: BGR图像
    :param saturation_scale: 饱和度放大系数，1.0表示无改变
    :return: 调整后的图像
    """
    # 将 BGR 图像转换到 HSV 色彩空间
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV).astype(np.float32)
    # 调整饱和度（S 通道），并克服值域问题
    hsv[..., 1] *= saturation_scale
    hsv[..., 1] = np.clip(hsv[..., 1], 0, 255)
    hsv = hsv.astype(np.uint8)
    # 转回 BGR 色彩空间
    return cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)

# 打开摄像头
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("无法打开摄像头")
    exit()

# 为方便演示，这里直接使用摄像头读取的分辨率（也可设置为其他分辨率）
# cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
# cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)

# 创建显示 Trackbar 的窗口
cv2.namedWindow("Trackbar")

# 在窗口中创建三个滑动条：亮度、对比度、饱和度
# 默认值设置为50，范围 0～100，50 被设定为“无变化”的中心值
cv2.createTrackbar("Brightness", "Trackbar", 50, 100, nothing)
cv2.createTrackbar("Contrast", "Trackbar", 50, 100, nothing)
cv2.createTrackbar("Saturation", "Trackbar", 50, 100, nothing)

frame_count = 0
start_time = time.time()

while True:
    ret, frame = cap.read()
    if not ret:
        print("无法读取视频帧")
        break

    frame_count += 1
    elapsed_time = time.time() - start_time
    fps = frame_count / elapsed_time

    # 此例中，我们从图像左上角截取 800x600 的区域
    cropped_frame = frame[0:600, 0:800]

    # 获取 Trackbar 的值，数值范围均为 0～100
    brightness_slider = cv2.getTrackbarPos("Brightness", "Trackbar")
    contrast_slider   = cv2.getTrackbarPos("Contrast", "Trackbar")
    saturation_slider = cv2.getTrackbarPos("Saturation", "Trackbar")

    # 将滑动条的数值映射到实际的图像处理参数
    # 默认中性值为50，无变化时：
    # - 亮度：映射为 [-50, +50]（即 50 对应 0 变化）
    # - 对比度：映射为 [0.5, 1.5]（即 50 对应 1.0，无变化）
    # - 饱和度：映射为 [0.5, 1.5]（即 50 对应 1.0，无变化）
    brightness_offset = brightness_slider - 50
    contrast_scale    = contrast_slider / 50.0
    saturation_scale  = saturation_slider / 50.0

    # 先调整亮度与对比度，再调整饱和度
    processed = adjust_brightness_contrast(cropped_frame,
                                           brightness=brightness_offset,
                                           contrast=contrast_scale)
    processed = adjust_saturation(processed, saturation_scale=saturation_scale)

    # 在图像上显示 FPS 和参数数值，便于观察调整效果
    cv2.putText(processed, "FPS: {:.2f}".format(fps), (10, 40),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    cv2.putText(processed, "Brightness: {}".format(brightness_offset), (10, 80),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
    cv2.putText(processed, "Contrast: {:.2f}".format(contrast_scale), (10, 110),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
    cv2.putText(processed, "Saturation: {:.2f}".format(saturation_scale), (10, 140),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

    # 显示处理后的结果
    cv2.imshow("Processed", processed)

    # 按 'q' 键退出循环
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()