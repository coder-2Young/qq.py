
from os.path import isdir, isfile, abspath, getsize, splitext, join, exists
from os import listdir, stat, rename, makedirs
from time import localtime, strftime
import hashlib
import re
import shutil


def sizeConvert(size):  # 文件大小转换函数，将以字节为单位的文件大小转化成K, M, G
    K, M, G = 1024, 1024 ** 2, 1024 ** 3
    if size > G:
        return str(size / G)[:5] + 'GB'
    elif size > M:
        return str(size / M)[:5] + 'MB'
    elif size > K:
        return str(size / K)[:5] + 'KB'
    else:
        return str(size)[:5] + 'B'


def file_rename(file_dir):
    if not isdir(file_dir):  # 如果输入的不是一个目录，则报错退出函数
        print("Not a dir!")
        return
    for dir in listdir(file_dir):
        realdir = join(file_dir, dir)  # Python以主函数所在的dirctory作为基准进行文件读取，如果不加file_dir将会找不到下层的文件
        if isdir(realdir):
            file_rename(realdir)  # 如果目标还是一个目录，递归调用函数
        else:
            if re.findall('(\d{10})', dir):  # 正则表达找到长度为10的整数即学号
                code = re.findall('(\d{10})', dir)[0]
                dir = ' '.join(dir.split())  # 去除多余空格
                dir = dir.replace(code, '')
                newname = join(file_dir, code + ' ' + dir)  # 改名要改完整的目录路径名
                rename(realdir, newname)


def get_md5(file_path):
    md5 = None  # 另一种增强鲁棒性的做法，前一种是判断如果不是目录则返回None，这一种是先定义返回值为None如果目标是文件则修改返回值为目标值
    if isfile(file_path):
        f = open(file_path, 'rb')
        md5_obj = hashlib.md5()  # 调用hashlib得到文件的md5值
        md5_obj.update(f.read())
        hash_code = md5_obj.hexdigest()
        f.close()
        md5 = hash_code.lower()
    return md5 #使用md5存在一个问题，即将名称中带有'副本'的文件留下，将原文件移到待删除中，后续可以加入对名称的条件判断增强实用性


def movefile(srcfile, dstfile):
    if not isfile(srcfile):
        print("src not exist!")
    else:
        shutil.move(srcfile, dstfile)  # 移动文件


def mvrep(file_all, new_dir):
    replist = []  # 存储文件的md5值，如果在该列表中找到了同样的md5值则说明文件重复
    if not exists(new_dir):
        makedirs(new_dir)
    for file in file_all:
        if file[-1] in replist:  # 判断文件的md5值是否在列表中
            movefile(join(file[1], file[0]), new_dir)
        else:
            replist.append(file[-1])  # 如果不在，说明该文件从未出现过，将其md5值记录在列表里


# 文件列表下标含义： 0名称 1路径 2大小 3创建时间 4修改时间 5文件类型 6md5值
def file_by_path(file_dir):
    file_all = []  # 定义用于存放文件信息的空列表
    if not isdir(file_dir):
        print("Not a dir!")
        return
    for dir in listdir(file_dir):
        realdir = join(file_dir, dir)  # Python以主函数所在的dirctory作为基准进行文件读取，如果不加file_dir将会找不到下层的文件
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
                file_inform.append(get_md5(realdir))  # 记录文件md5值
                file_all.append(file_inform)  # 将完整的文件信息填入所有文件信息的列表
    return file_all


# 将文件名列表写入excel
def write_excel(file_all):
    wb = Workbook()  # 创建一个表格文件
    sheet = wb.active  # 激活表格
    sheet.title = '文件信息'  # 修改表格标题
    # 向第1个sheet页写数据
    sheet1 = wb.create_sheet('全部文件', 1)
    sheet1.column_dimensions['A'].width = 35  # 修改表格列宽
    sheet1.column_dimensions['B'].width = 74
    sheet1.column_dimensions['C'].width = 14
    sheet1.column_dimensions['D'].width = 15
    sheet1.column_dimensions['E'].width = 8
    sheet1['A1'] = '文件名'  # 向第一行填入信息
    sheet1['B1'] = '路径'
    sheet1['C1'] = '大小'
    sheet1['E1'] = '类型'
    for file in file_all:
        file_ = file[0:4]  # 对列表进行切片，得到列表0 1 2 3 5的信息
        type = file[5]
        file_.append(type)
        sheet1.append(file_)  # 在sheet1上直接插入一行

    # 向第2个sheet页写数据
    sheet2 = wb.create_sheet('可编辑文件', 2)
    sheet2.column_dimensions['A'].width = 35
    sheet2.column_dimensions['B'].width = 74
    sheet2.column_dimensions['C'].width = 14
    sheet2.column_dimensions['D'].width = 15
    sheet2.column_dimensions['E'].width = 15
    sheet2.column_dimensions['F'].width = 8
    sheet2['A1'] = '文件名'
    sheet2['B1'] = '路径'
    sheet2['C1'] = '大小'
    sheet2['D1'] = '创建时间'
    sheet2['E1'] = '修改时间'
    sheet2['F1'] = '类型'
    for file in file_all:
        if file[5] in ['txt', 'doc', 'docx', 'xls', 'xlsx']:  # 判断文件类型是否为可修改类型
            sheet2.append(file[0:6])  # 将文件信息 0 1 2 3 4 5填入

    sheet3 = wb.create_sheet('含有学号的文件', 3)
    sheet3.column_dimensions['A'].width = 35
    sheet3.column_dimensions['B'].width = 74
    sheet3.column_dimensions['C'].width = 14
    sheet3.column_dimensions['D'].width = 15
    sheet3.column_dimensions['E'].width = 8
    sheet3['A1'] = '文件名'
    sheet3['B1'] = '路径'
    sheet3['C1'] = '大小'
    sheet3['D1'] = '创建时间'
    sheet3['E1'] = '类型'
    for file in file_all:
        code = re.findall('(\d{10})', file[0])  # 正则表达式判断是否有学号在文件名称里
        if code:
            file_ = file[0:4]  # 切片+组合
            type = file[5]
            file_.append(type)
            sheet3.append(file_)

    sheet4 = wb.create_sheet('待删除文件', 4)
    sheet4.column_dimensions['A'].width = 35
    sheet4.column_dimensions['B'].width = 74
    sheet4.column_dimensions['C'].width = 14
    sheet4.column_dimensions['D'].width = 15
    sheet4.column_dimensions['E'].width = 8
    sheet4['A1'] = '文件名'
    sheet4['B1'] = '路径'
    sheet4['C1'] = '大小'
    sheet4['D1'] = '创建时间'
    sheet4['E1'] = '类型'
    for file in file_all:
        if re.findall('待删除文件', file[1]):  # 正则表达式查找文件是否在'待删除文件'这个文件夹里
            file_ = file[0:4]
            type = file[5]
            file_.append(type)
            sheet4.append(file_)
    # 工作簿保存到磁盘
    xlsx_name = '文件信息.xlsx'
    wb.save(xlsx_name)


def main():
    # 文档目录设置
    file_dir = r'上机3测试用（运行前）'  # r是为了使/不产生转义

    file_rename(file_dir)  # 先对所有文件进行一次重命名操作

    # 函数调用，返回文件名列表
    file_all = file_by_path(file_dir)
    mvrep(file_all, join(file_dir,'待删除文件'))  # 将重复的文件移到'待删除文件'里
    file_all = file_by_path(file_dir)  # 再次查询修改过的文件目录
    write_excel(file_all)  # 将文件信息写入excel


main()
