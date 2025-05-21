import numpy as np
import cv2

# 创建一个 50x50 的黑色图像 (默认为全零)
image = np.zeros((50, 50, 3), dtype=np.uint8)

# 选择颜色填充图像 (例如蓝色)
image[:] = (255, 0, 0)  # BGR 格式，(255, 0, 0) 代表蓝色

# 显示图像
cv2.imshow("Generated Image", image)
cv2.waitKey(0)
cv2.destroyAllWindows()
