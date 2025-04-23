import cv2
import numpy as np

# 定义坐标点（这里坐标为浮点数，通常可以直接转换为整数）
points = np.array([[220.0, 3.0],
                   [247.0, 3.0],
                   [247.0, 21.0],
                   [220.0, 21.0]], dtype=np.int32)

# 将坐标点转换成符合 cv2.polylines 要求的形状：NumPy 数组，形状为 (N, 1, 2)
points = points.reshape((-1, 1, 2))

# 读取图片。如果没有现成的图片，也可以创建一张空白图像进行测试
img = cv2.imread('../img/2.png')

# 这里创建一张空白的黑色背景图像，尺寸可以根据实际需要调整
#img = np.zeros((100, 300, 3), dtype=np.uint8)

# 绘制多边形。参数说明：
# - [points]：传入点的列表（必须是一个列表，包含一个数组）
# - isClosed=True：表示闭合多边形（即最后一个点与第一个点相连）
# - color=(0, 255, 0)：设置绘制颜色为绿色（BGR格式）
# - thickness=2：线条粗细
cv2.polylines(img, [points], isClosed=True, color=(0, 255, 0), thickness=2)

# 显示结果
cv2.imshow("Image with Box", img)
cv2.waitKey(0)
cv2.destroyAllWindows()
