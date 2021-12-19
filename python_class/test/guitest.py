import tkinter as tk
from tkinter import *
import tkinter.ttk
import os,sys
from tkinter.filedialog import askdirectory
# 创建tkinter应用程序主窗口
window = tk.Tk()
path = StringVar()
var = StringVar()

#print(window.keys())

# 设置窗口标题
window.title('文件管理器')
# 定义窗口初始大小
#window['width'] = 1000
#window['height'] = 800
window.geometry('1000x800')
window.resizable(0, 0)  # 设置窗口大小不可变

def selectPath():
    path_ = askdirectory()
    path.set(path_)

def printInfo():
    dir_list = os.listdir(entry.get())
    os.chdir(entry.get())
    n = 0
    for dir_list_ in dir_list:
        n += 1
        file_path = os.path.realpath(dir_list_)
        print(file_path)
        lb.insert(n, '文件名:'+dir_list_+',文件路径'+file_path+',  大小:'+str(int((os.path.getsize(file_path) // 1024)))+'KB, 创建时间:')



frame1 = tk.Frame(window)  # 生成第一组按钮的容器
frame1.grid(row=0, column=0, sticky='w')  # sticky='w'指定了组件在单元格中靠左对齐
tk.Label(frame1, text='文件夹:').pack(side='left')  # 添加本组标题
entry=Entry(frame1, textvariable = path, width = 80)
entry.pack(side='left')
tk.Button(frame1, text='选择文件夹', height=1, command=selectPath).pack(side='left',padx=10)  # 添加按钮
tk.Button(frame1, text='扫描文件', height=1, command=printInfo).pack(side='left')  # 添加按钮


frame2 = tk.Frame(window)  # 生成第二组按钮的容器
frame2.grid(row=1, column=0, sticky='w')  # sticky='w'指定了组件在单元格中靠左对齐
tk.Label(frame2, text='文件分组:').pack(side='left')  # 添加本组标题
tk.ttk.Combobox(frame2, textvariable=var,value=('所有文件', '可编辑文件', '含有学号信息的文件')).pack(side='left')  #
tk.Button(frame2, text='文件分组筛选', height=1, command=selectPath).pack(side='left',padx=10)  # 添加按钮


lb=Listbox(window,width=140,height=35)

lb.grid()
# 启动应用程序，启动消息循环
window.mainloop()






