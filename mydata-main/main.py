import cv2

# 读取图像
image = cv2.imread("images/train/0.jpg")
height, width, _ = image.shape

# YOLO 坐标 (class, x_center, y_center, box_width, box_height)
yolo_data = [1, 0.081250, 0.142487, 0.100000, 0.147668]

# 解析数据
_, x_center, y_center, box_width, box_height = yolo_data

# 归一化坐标转换为像素坐标
x_center, y_center = int(x_center * width), int(y_center * height)
box_width, box_height = int(box_width * width), int(box_height * height)

# 计算左上角和右下角坐标
x1, y1 = x_center - box_width // 2, y_center - box_height // 2
x2, y2 = x_center + box_width // 2, y_center + box_height // 2

# 画框
cv2.rectangle(image, (x1, y1), (x2, y2), (0, 255, 0), 2)

# 显示图像
cv2.imshow("YOLO Detection", image)
cv2.waitKey(0)
cv2.destroyAllWindows()