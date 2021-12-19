from tkinter import *
from tkinter.ttk import Combobox
from os import stat
from os.path import isfile, realpath, splitext, getsize
from tkinter.filedialog import askdirectory
from time import localtime, strftime
from os import listdir
import re


def sizeConvert(size):  # 文件大小转换函数，将以字节为单位的文件大小转化成K, M, G
    K, M, G = 1024, 1024 ** 2, 1024 ** 3
    if size > G:
        return str(size / G)[:5] + 'GB'  # 截取大小长度为5
    elif size > M:
        return str(size / M)[:5] + 'MB'
    elif size > K:
        return str(size / K)[:5] + 'KB'
    else:
        return str(size)[:5] + 'B'


def sel_dir():
    path_ = askdirectory()  # 打开图形窗口，选择目录
    path.set(path_)  # 记录选定目录


def scan_file():
    n = 0
    for file in listdir(e1.get()):
        if isfile(file):
            n += 1
            realdir = realpath(file)
            lb1.insert(n, '名称：{:10},路径{:20},大小:{:10},创建时间:{:10},类型:{:5}'.
                       format(str(file),
                              realdir,
                              sizeConvert(getsize(realdir)),
                              strftime("%Y-%m-%d", localtime(stat(realdir).st_mtime)),
                              splitext(realdir)[-1][1:]))


def scan_edt_file():
    n = 0
    for file in listdir(e1.get()):
        if isfile(file) and splitext(file)[-1][1:] in ['txt', 'doc', 'docx', 'xls', 'xlsx']:
            n += 1
            realdir = realpath(file)
            lb1.insert(n, '名称：{:10},路径{:20},大小:{:10},创建时间:{:10},类型:{:5}'.
                       format(str(file),
                              realdir,
                              sizeConvert(getsize(realdir)),
                              strftime("%Y-%m-%d", localtime(stat(realdir).st_mtime)),
                              splitext(realdir)[-1][1:]))


def scan_code_file():
    n = 0
    for file in listdir(e1.get()):
        code = re.findall('(\d{10})', file)
        if isfile(file) and code:
            n += 1
            realdir = realpath(file)
            lb1.insert(n, '名称：{:10},路径{:20},大小:{:10},创建时间:{:10},类型:{:5}'.
                       format(str(file),
                              realdir),
                       sizeConvert(getsize(realdir)),
                       strftime("%Y-%m-%d", localtime(stat(realdir).st_mtime)),
                       splitext(realdir)[-1][1:])


def file_print():
    flag = c1.get()
    if flag == '所有文件':
        lb1.delete(0, END)
        scan_file()
    elif flag == '可编辑文件':
        lb1.delete(0, END)
        scan_edt_file()
    elif flag == '含学号的文件':
        lb1.delete(0, END)
        scan_code_file()


# 创建tkinter应用程序主窗口


window = Tk()
path = StringVar()
var = StringVar()

# 设置窗口标题
window.title('文件管理器')
# 定义窗口初始大小
window['width'] = 1000
window['height'] = 800
window.resizable(0, 0)  # 设置窗口大小不可变
b1 = Button(window, text='选择文件夹', command=sel_dir)
b1.grid(row=0, column=1, padx=10, pady=5, sticky='w')
e1 = Entry(window, textvariable=path, width=140)
e1.grid(row=0, column=0, padx=10, pady=5, sticky='w')
b2 = Button(window, text='扫描文件', command=scan_file)
b2.grid(row=0, column=2, padx=10, pady=5, sticky='w')
lb1 = Listbox(window, width=150, height=40)
lb1.grid(row=2, padx=5, pady=5, sticky='w')
c1 = Combobox(window, textvariable=var, value=('所有文件', '可编辑文件', '含学号的文件'))
c1.grid(row=1, column=0, padx=5, pady=5, sticky='w')
b3 = Button(window, text='文件分组筛选', command=file_print)
b3.grid(row=1, column=1, padx=5, pady=5, sticky='w')
# 启动应用程序，启动消息循环
window.mainloop()
