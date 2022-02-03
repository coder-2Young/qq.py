import tkinter as tk
from tkinter import *
import tkinter.ttk
import os,sys
import openpyxl
from openpyxl.workbook import Workbook
from os.path import isdir, isfile, abspath, getsize, splitext, join, exists
import os,re
import time

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

def file_by_path(file_dd):
    file_all = []  # 定义用于存放文件信息的空列表
    for dir in os.listdir(file_dd):
        dir_ = join(file_dd, dir)
        print(dir_)
        if isdir(dir_):
            file_in_dir = file_by_path(dir_)
            for file in file_in_dir:
                file_all.append(file)
        else:
            file_lb = []
            file_lb.append(dir)
            file_lb.append(abspath(file_dd))
            file_lb.append(str(int(os.path.getsize(dir_) / 1024)) + 'KB')  # 记录文件的大小，通过sizeConvert将其转化成更可读的形式
            file_lb.append(time.strftime("%Y-%m-%d", time.localtime(os.path.getctime(dir_))))  # 记录创建时间，以格式化输出
            file_lb.append(time.strftime("%Y-%m-%d", time.localtime(os.path.getmtime(dir_))))  # 记录修改时间，以格式化输出
            file_lb.append(os.path.splitext(dir_)[-1][1:])  # 记录文件类型
            # file_inform.append(get_md5(dir_))  # 记录文件md5值
            file_all.append(file_lb)  # 将完整的文件信息填入所有文件信息的列表
    return file_all

def selectPath():
    path_ = askdirectory()
    path.set(path_)

def shaixuan():
    lb.delete(0,END)
    file_dir = os.listdir(entry.get())
    os.chdir(entry.get())
    file_dd = entry.get()
    file_all = file_by_path(file_dd)
    file_kind = com.get()
    if file_kind == '所有文件':
        for item in file_all:
            lb.insert(0, item[0] + '路径：' + item[1] + ',大小：' + item[2] + '，创建时间：' + item[3] + ',类型:' + item[5])
    elif file_kind == '可编辑文件':
        for item in file_all:
            if item[5] in ['txt', 'doc', 'docx', 'xls', 'xlsx']: # 判断文件类型是否为可修改类型
                lb.insert(0, item[0] + '路径：' + item[1] + ',大小：' + item[2] + '，创建时间：' + item[3] + ',类型:' + item[5])
    else:
        for item in file_all:
            code = re.findall('(\d{10})', item[0])  # 正则表达式判断是否有学号在文件名称里
            if code:
                lb.insert(0, item[0] + '路径：' + item[1] + ',大小：' + item[2] + '，创建时间：' + item[3] + ',类型:' + item[5])






def printInfo():
    lb.delete(0,END)
    file_dir = os.listdir(entry.get())
    os.chdir(entry.get())
    file_dd = entry.get()
    file_all = file_by_path(file_dd)
    #print(e
    #
    #print(file_dd)
    for item in file_all:
        lb.insert(0,item[0] + '路径：'+item[1] +',大小：' + item[2] +'，创建时间：'+ item[3]+',类型:'+ item[5])


on_hit = False
#e = tk.Entry(window, show=None,textvariable = path,font=('Arial', 14)).grid(row = 0, column = 1)  # 显示成明文形式
#e.pack()



frame1 = tk.Frame(window)  # 生成第一组按钮的容器
frame1.grid(row=0, column=0, sticky='w')  # sticky='w'指定了组件在单元格中靠左对齐
tk.Label(frame1, text='文件夹:').pack(side='left')  # 添加本组标题
entry=Entry(frame1, textvariable = path, width = 110)
entry.pack(side='left')
tk.Button(frame1, text='选择文件夹', height=1, command=selectPath).pack(side='left',padx=10)  # 添加按钮
tk.Button(frame1, text='扫描文件', height=1, command=printInfo).pack(side='left',padx=10)  # 添加按钮


frame2 = tk.Frame(window)  # 生成第二组按钮的容器
frame2.grid(row=1, column=0, sticky='w')  # sticky='w'指定了组件在单元格中靠左对齐
tk.Label(frame2, text='文件分组:').pack(side='left')  # 添加本组标题
com=tk.ttk.Combobox(frame2, textvariable=var,value=('所有文件', '可编辑文件', '含有学号信息的文件'))  #
com.pack(side='left')
tk.Button(frame2, text='文件分组筛选', height=1, command=shaixuan).pack(side='left',padx=10)  # 添加按钮


lb=Listbox(window,width=140,height=35)

lb.grid()
# 启动应用程序，启动消息循环
window.mainloop()






