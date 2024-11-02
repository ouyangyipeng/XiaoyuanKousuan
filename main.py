import cv2
import numpy as np
import pyautogui
pyautogui.FAILSAFE = False
import pytesseract
import keyboard
import sys
import time
import re

# 设置 Tesseract-OCR 的路径
pytesseract.pytesseract.tesseract_cmd = r'C:\Tesseract-OCR\tesseract.exe'

# 跟踪状态的变量
not_found_count = 0
last_not_found_time = 0
last_numbers = None

def capture_area():
    region = (500, 350, 600, 150)  # 截取区域的坐标和大小
    screenshot = pyautogui.screenshot(region=region)
    return np.array(screenshot)

def recognize_numbers(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray = cv2.medianBlur(gray, 3)  # 中值滤波
    _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)  # Otsu二值化
    text = pytesseract.image_to_string(thresh, config='--psm 6')
    return [int(num) for num in re.findall(r'\d+', text)]  # 提取并转换所有数字

def handle_insufficient_numbers():
    global not_found_count, last_not_found_time
    current_time = time.time()
    if current_time - last_not_found_time <= 1:
        not_found_count += 1
    else:
        not_found_count = 1
    last_not_found_time = current_time

    if not_found_count >= 25:
        print("未找到足够的数字，准备重新开始...")

def draw_comparison(numbers):
    global not_found_count, last_numbers

    if len(numbers) < 2:
        handle_insufficient_numbers()
        return

    execute_drawing_logic(numbers)
    not_found_count = 0
    last_numbers = numbers

def execute_drawing_logic(numbers):
    first, second = numbers[:2]
    print(f"识别的数字: {first}, {second}")

    if first > second:
        print(f"{first} > {second}")
        draw_greater_than()
    elif first < second:
        print(f"{first} < {second}")
        draw_less_than()

def draw_greater_than():
    pyautogui.press(".")  # 使用热键绘制大于号
    print("绘制大于号")

def draw_less_than():
    pyautogui.press(",")  # 使用热键绘制小于号
    print("绘制小于号")

def main():
    keyboard.add_hotkey('=', lambda: sys.exit("进程已结束"))

    try:
        while True:
            image = capture_area()
            numbers = recognize_numbers(image)
            draw_comparison(numbers)
            time.sleep(0.5)  # 可根据需要调整延迟
    except SystemExit as e:
        print(e)

if __name__ == "__main__":
    main()  # 启动主程序
