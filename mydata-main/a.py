import cv2
import os

# 确保 img 文件夹存在
folder_path = "img"
os.makedirs(folder_path, exist_ok=True)  # 如果文件夹不存在，就创建它

# 读取或创建图像
image = cv2.imread("images/train/0.jpg")  # 你也可以用 np.zeros() 创建一张图

# 指定保存路径
save_path = os.path.join(folder_path, "saved_image.jpg")
print(save_path)
# 保存图像
cv2.imwrite(save_path, image)

print(f"图像已保存至: {save_path}")
