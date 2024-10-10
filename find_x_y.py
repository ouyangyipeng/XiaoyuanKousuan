import pyautogui
import time

print("开始获取鼠标坐标，按 Ctrl+C 停止")

try:
    while True:
        x, y = pyautogui.position()  # 获取当前鼠标的坐标
        position_str = f"当前鼠标坐标: ({x}, {y})"
        print(position_str, end="\r")  # 用\r回到行首，避免屏幕上重复输出
        time.sleep(0.1)  # 每隔100毫秒刷新一次
except KeyboardInterrupt:
    print("\n坐标获取结束")
