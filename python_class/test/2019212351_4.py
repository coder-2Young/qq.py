from tkinter import *
from tkinter.ttk import Combobox
from os import stat
from os.path import splitext, getsize, abspath, isdir, join
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


def file_by_path(file_dir):
    file_all = []  # 定义用于存放文件信息的空列表
    if not isdir(file_dir):
        print("Not a dir!")
        return
    for dir in listdir(file_dir):
        realdir = join(file_dir, dir)  # Python以主函数所在的dirctory作为基准进行文件读取，如果不用join将会找不到下层的文件
        if isdir(realdir):
            file_in_dir = file_by_path(realdir)  # 递归调用
            for file in file_in_dir:
                file_all.append(file)  # 如果不用file_in_dir而直接调用的话，内部递归会将file_all这个局部变量清零，无法保存目录内的文件信息
        else:
            if splitext(realdir)[-1] != '':  # 在查找过程中查找到了不是目录也没有后缀的文件，应该是pycharm自动保存的一些数据，进行过滤
                file_inform = []  # 以2维列表的形式保存信息，每个file_inform保存一个文件的所有信息
                file_inform.append(dir)
                file_inform.append(abspath(file_dir))  # 记录文件的绝对地址，通过file_dir只记录到上层目录
                file_inform.append(sizeConvert(getsize(realdir)))  # 记录文件的大小，通过sizeConvert将其转化成更可读的形式
                file_inform.append(strftime("%Y-%m-%d", localtime(stat(realdir).st_mtime)))  # 记录创建时间，以格式化输出
                file_inform.append(strftime("%Y-%m-%d", localtime(stat(realdir).st_ctime)))  # 记录修改时间，以格式化输出
                file_inform.append(splitext(realdir)[-1][1:])  # 记录文件类型
                file_all.append(file_inform)  # 将完整的文件信息填入所有文件信息的列表
    return file_all


def sel_dir():
    path_ = askdirectory()  # 打开图形窗口，选择目录
    path.set(path_)  # 记录选定目录


def scan_file():
    lb1.delete(0, END)  # 清空listbox，不然重复点击按钮会叠加显示
    file_dir = e1.get()  # 获取选定路径
    file_all = file_by_path(file_dir)  # 调用遍历文件函数
    for file in file_all:  # 在listbox里插入文件信息
        lb1.insert(0, file[0] + '路径：' + file[1] + ',大小：' + file[2] + '，创建时间：' + file[3] + ',类型:' + file[5])


def filter_file():
    lb1.delete(0, END)  # 清空listbox，不然重复点击按钮会叠加显示
    file_dir = e1.get()  # 获取选定路径
    file_all = file_by_path(file_dir)
    file_kind = c1.get()  # 获取筛选文件的类型
    if file_kind == '所有文件':
        for file in file_all:
            lb1.insert(0, file[0] + '路径：' + file[1] + ',大小：' + file[2] + '，创建时间：' + file[3] + ',类型:' + file[5])
    elif file_kind == '可编辑文件':
        for file in file_all:
            if file[5] in ['txt', 'doc', 'docx', 'xls', 'xlsx']:  # 判断文件类型是否为可修改类型
                lb1.insert(0, file[0] + '路径：' + file[1] + ',大小：' + file[2] + '，创建时间：' + file[3] + ',类型:' + file[5])
    else:
        for file in file_all:
            if re.findall('(\d{10})', file[0]):  # 正则表达式判断是否有长度为10的整数，即学号在文件名里
                lb1.insert(0, file[0] + '路径：' + file[1] + ',大小：' + file[2] + '，创建时间：' + file[3] + ',类型:' + file[5])


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
b1 = Button(window, text='选择文件夹', command=sel_dir)  # 设置按钮1，显示"选择文件夹"，点击后执行sel_dir选择路径
b1.grid(row=0, column=1, padx=10, pady=5, sticky='w')  # 将按钮布置到网格的0行1列，横向间距10，纵向间距5，向左对齐
e1 = Entry(window, textvariable=path, width=140)  # 设置输入框，显示路径，宽度140
e1.grid(row=0, column=0, padx=10, pady=5, sticky='w')  # 将输入框布置到网格的0行0列，横向间距10，纵向间距5，向左对齐
b2 = Button(window, text='扫描文件', command=scan_file)
b2.grid(row=0, column=2, padx=10, pady=5, sticky='w')
lb1 = Listbox(window, width=150, height=40)  # 设置Listbox，宽150，高40
lb1.grid(row=2, padx=5, pady=5, sticky='w')
c1 = Combobox(window, textvariable=var, value=('所有文件', '可编辑文件', '含学号的文件'))  # 设置Combobox，选择'所有文件', '可编辑文件', '含学号的文件'
c1.grid(row=1, column=0, padx=5, pady=5, sticky='w')
b3 = Button(window, text='文件分组筛选', command=filter_file)
b3.grid(row=1, column=1, padx=5, pady=5, sticky='w')
# 启动应用程序，启动消息循环
window.mainloop()
