import tkinter as tk




# 创建tkinter应用程序主窗口
window = tk.Tk()

# print(window.keys())

# 设置窗口标题
window.title('文件管理器')
# 定义窗口初始大小
window['width'] = 1000
window['height'] = 800
window.resizable(0, 0)  # 设置窗口大小不可变


# 启动应用程序，启动消息循环
window.mainloop()