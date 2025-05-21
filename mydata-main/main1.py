import cv2
import numpy as np
# 初始化摄像头
cap = cv2.VideoCapture(0)

# 定义按钮区域
button_x1, button_y1, button_x2, button_y2 = 50, 50, 200, 100

def on_mouse(event, x, y, flags, param):
    """鼠标回调函数"""
    if event == cv2.EVENT_LBUTTONDOWN:  # 鼠标左键点击
        if button_x1 < x < button_x2 and button_y1 < y < button_y2:
            ret, frame = cap.read()
            if ret:
                cv2.imwrite("img.jpg", frame)
                print("图像已保存为 img.jpg")

cv2.namedWindow("Camera")
cv2.resizeWindow("Camera",120 , 120)
cv2.setMouseCallback("Camera", on_mouse)
img = np.zeros((120,120, 3), dtype= np.uint8)
img[:] = (255,0 ,0)
while True:
    ret, frame = cap.read()
    if not ret:
        break

    # 画按钮
    cv2.rectangle(img, (button_x1, button_y1), (button_x2, button_y2), (0, 255, 0), -1)
    cv2.putText(img, "Save Img", (button_x1 + 20, button_y1 + 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)

    cv2.imshow("img", frame)
    cv2.imshow("Camera", img)

    if cv2.waitKey(1) & 0xFF == 27:  # ESC 退出
        break

cap.release()
cv2.destroyAllWindows()
