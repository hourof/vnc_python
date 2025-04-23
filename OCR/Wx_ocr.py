#微信ocr项目
import os
import json
import time
from wechat_ocr.ocr_manager import OcrManager, OCR_MAX_TASK_ID

wechat_ocr_dir = "C:\\Users\\user\\AppData\\Roaming\\Tencent\\WeChat\\XPlugin\\Plugins\\WeChatOCR\\7079\\extracted\\WeChatOCR.exe"
wechat_dir = "C:\\Program Files\\Tencent\WeChat\\[3.9.12.51]"

#获取当前文件(main.py)所在的目录
current_dir = os.path.dirname(os.path.abspath(__file__))
print(current_dir)
img_path = os.path.join(current_dir, "..", "img", "1.jpg")
print("你好",img_path)
def ocr_result_callback(img_path: str, results: dict):
    result_file = os.path.basename(img_path) + ".json"
    print(f"识别成功，img_path: {img_path}, result_file: {result_file}")
    with open(result_file, 'w', encoding='utf-8') as f:
        f.write(json.dumps(results, ensure_ascii=False, indent=2))


def main():
    ocr_manager = OcrManager(wechat_dir)
    # 设置WeChatOcr目录
    ocr_manager.SetExePath(wechat_ocr_dir)
    # 设置微信所在路径
    ocr_manager.SetUsrLibDir(wechat_dir)
    # 设置ocr识别结果的回调函数
    ocr_manager.SetOcrResultCallback(ocr_result_callback)
    # 启动ocr服务
    ocr_manager.StartWeChatOCR()
    # 开始识别图片
    ocr_manager.DoOCRTask("../img/1.jpg")
    time.sleep(1)
    while ocr_manager.m_task_id.qsize() != OCR_MAX_TASK_ID:
        pass
    # 识别输出结果

    a =  ocr_manager.KillWeChatOCR()
    print(a)


if __name__ == "__main__":
    main()
