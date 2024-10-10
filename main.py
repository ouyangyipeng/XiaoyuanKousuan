import pyautogui
from PIL import Image, ImageEnhance, ImageOps
import pytesseract
import re
import time
import os

# 设置 Tesseract 可执行文件的路径
pytesseract.pytesseract.tesseract_cmd = os.getenv('TESSERACT_CMD', r'D:\Programm\tesseract\tesseract.exe')

# 定义图像预处理函数

def preprocess_image(image_path):
    img = Image.open(image_path)
    
    # 将图片转换为灰度图像
    img = img.convert('L')
    
    # 自动调整图片对比度
    img = ImageOps.autocontrast(img)
    
    # 二值化图片
    img = img.point(lambda p: p > 128 and 255)
    
    # 保存处理后的图像供检查
    processed_image_path = "screenshot.png"
    img.save(processed_image_path)
    
    return processed_image_path


# 定义捕捉屏幕区域函数

def capture_screen_region(x_start, y_start, width, height, save_path="screenshot.png"):
    region = (x_start, y_start, width, height)
    screenshot = pyautogui.screenshot(region=region)
    screenshot.save(save_path)
    save_path = preprocess_image(save_path)
    return save_path

# 使用 OCR 识别数学题

def recognize_math_question(image_path):
    custom_config = r'--psm 6 -c tessedit_char_whitelist=0123456789?'
    result = pytesseract.image_to_string(Image.open(image_path), config=custom_config).strip()
    
    return result

def compare_math_question(question):
    # 处理有问号的情况，如 "14 ? 11"
    match = re.match(r"(\d{1,2})\s*\?\s*(\d{1,2})", question)
    
    # 如果没有问号，尝试匹配两个数字的情况，如 "1411" 或 "14 11"
    # if not match:
    #     match = re.match(r"(\d{1,2})\s*(\d{1,2})", question)
    
    # 如果匹配到两个数字，继续处理
    if match:
        num1 = int(match.group(1))  # 获取第一个数字
        num2 = int(match.group(2))  # 获取第二个数字

        # 根据数字大小返回比较结果
        if num1 > num2:
            return '>'
        elif num1 < num2:
            return '<'
        else:
            return '='
    
    # 如果未能匹配任何有效的数学题，返回 None
    return None

def draw_result(result, x, y):
    if result == '>':
        # 绘制大于号 ">"
        pyautogui.moveTo(x, y)
        pyautogui.mouseDown(button='left')

    # 右下角移动 (50, 50)
        pyautogui.moveRel(50, 50, duration=0.01)

    # 接着左下角移动 (-50, 50)
        pyautogui.moveRel(-50, 50, duration=0.01)

    # 松开鼠标左键
        pyautogui.mouseUp(button='left')
    
    elif result == '<':
        # 绘制小于号 "<"
        pyautogui.moveTo(x, y)  # 移动到起始位置
        pyautogui.mouseDown(button='left')

    # 右下角移动 (50, 50)
        pyautogui.moveRel(-50, 50, duration=0.01)

    # 接着左下角移动 (-50, 50)
        pyautogui.moveRel(50, 50, duration=0.01)

    # 松开鼠标左键
        pyautogui.mouseUp(button='left')
    
    elif result == '=':
        # 绘制等于号 "="
        pyautogui.moveTo(x, y)  # 移动到起始位置
        pyautogui.dragRel(50, 0, duration=0.2)    # 绘制第一条水平线
        pyautogui.moveTo(x, y + 20)  # 移动到下方
        pyautogui.dragRel(50, 0, duration=0.2)    # 绘制第二条水平线
        
# 主程序流程
def main():
    x_start = 2810
    y_start = 550
    width = 700
    height = 500

    screenshot_path = "screenshot.png"

    capture_screen_region(x_start, y_start, width, height, screenshot_path)

    math_question = recognize_math_question(screenshot_path)
    print(f"识别到的数学题：{math_question}")

    result = compare_math_question(math_question)
    
    if result:
        print(f"判断结果：{result}")
        draw_x = 3000
        draw_y = 1260
        draw_result(result, draw_x, draw_y)
    else:
        print("无法解析数学题")

if __name__ == "__main__":
    start_time = time.time()  # 记录程序开始运行的时间
    try:
        while True:
            main()  # 执行主函数
            time.sleep(0.5)  # 每次循环后等待 0.5 秒
            
            elapsed_time = time.time() - start_time
            if elapsed_time > 100:  # 如果超过 25 秒，则停止程序
                print("程序已自动运行 25 秒，停止运行")
                break  # 跳出循环，终止程序

    except KeyboardInterrupt:
        print("程序已手动终止")
    except Exception as e:
        print(f"发生错误：{e}")
