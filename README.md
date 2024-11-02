# 注意事项：

使用前请点个免费的star

版本较粗糙，可能出问题，欢迎大佬来优化

作者对使用造成的任何后果不负责任

只能识别两位数及以下的比大小

# 使用方法：

## 下载python
```
https://www.python.org/downloads/windows/
```

上述链接下载python，打开安装包，安装过程中记得勾选add to path选项

若没有addtopath则手动添加至系统变量

win+r输入powershell，输入
```shell
python --version
```
检查是否成功安装

## 相关下载
保持在cmd输入
```shell
pip install pyautogui pillow pytesseract
```

## 下载tesseract

```
https://github.com/tesseract-ocr/tesseract/releases
```

在上述网址下载tesseract，相同方法检查是否成功安装


## 下载脚本
拉取整个仓库，存放于一个文件夹

## 修改脚本

main.py中的地址改成本地地址
```python
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'\
```

## 寻找坐标并修改坐标

将手机投屏至电脑，保证不要移动投屏窗口的位置和大小，保证鼠标可以正常操作手机（就像触屏一样）

powershell中进入仓库文件夹，运行find_x_y.py
```shell
cd 输入你的文件夹
python find_x_y.py
```

根据指示移动至 题目识别区域 和 画大小号区域

修改main.py的主函数
```python
def main():
    x_start = 400  # 根据实际情况调整
    y_start = 350  # 根据实际情况调整
    width = 500    # 根据实际情况调整
    height = 100   # 根据实际情况调整

    screenshot_path = "screenshot.png"

    capture_screen_region(x_start, y_start, width, height, screenshot_path)

    math_question = recognize_math_question(screenshot_path)
    print(f"识别到的数学题：{math_question}")

    result = compare_math_question(math_question)

    if result:
        print(f"判断结果：{result}")
        draw_x = 450  # 根据实际情况调整
        draw_y = 800  # 根据实际情况调整
        draw_result(result, draw_x, draw_y)
    else:
        print("无法解析数学题")

```


## 运行
```shell
python main.py
```

## 贡献
<a href="https://github.com/ouyangyipeng/XiaoyuanKousuan/graphs/contributors">
    <img src="https://contrib.rocks/image?repo=ouyangyipeng/XiaoyuanKousuan" />
</a>

