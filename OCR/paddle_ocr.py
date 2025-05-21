from paddleocr import PaddleOCR
import mss
import argparse
import numpy as np
import cv2

ocr = PaddleOCR(use_angle_cls=True, use_gpu=False, lang="ch")

monitor = {"top": 300, "left": 300, "width": 300, "height": 300}

with mss.mss() as sct:
    while True:
        screenshot = sct.grab(monitor)
        srcimg = np.array(screenshot)
        srcimg = cv2.cvtColor(srcimg, cv2.COLOR_BGRA2RGB)  # 注意这里改为BGRA2RGB

        result = ocr.ocr(srcimg, cls=True)
        print("1",result)
        if result ==[None]:
            print("打印")
            continue
        if result:
            for line in result:
                for item in line:
                    if len(item) >= 2:
                        text, confidence = item[1]
                        print(f"文字: {text}, 置信度: {confidence}")
        cv2.imshow("img", srcimg)
        # 按'q'退出
        if cv2.waitKey(500) & 0xFF == ord('q'):
            break
# if __name__ == '__main__':
#     parser = argparse.ArgumentParser()
#     parser.add_argument("--imgpath", type= str, default="../img/2.png", help= "img path")
#     args = parser.parse_args()
#     print(args)
#     print(args.imgpath)
#     result = ocr.ocr(args.imgpath)
#
#     print(result)
#     print(f"len{len(result)}")
#
#     cv2.destroyAllWindows()
