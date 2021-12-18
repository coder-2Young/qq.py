import re  # 导入正则表达式模块


# 定义文件类File
class File:
    count = 0  # 定义类变量——File类文件的个数

    def __init__(self, file_name, file_path, file_size, file_createTime, file_type):
        self.file_name = file_name  # 定义实例变量
        self.file_path = file_path
        self.file_size = file_size
        self.file_createTime = file_createTime
        self.file_type = file_type
        '''修改类变量，这种方法用于统计File类实例的个数的优点是：节约内存、提高运行速度，缺点是：如果重复定义同一个实例，count会高于实际上的类实例个数
        例如：
        a=File(1,2,3,4,5)
        a.output_count()
        1
        b=File(1,2,3,4,5)
        a.output_count()
        2
        a=File(1,2,3,3,5)
        a.output_count()
        3
        实际上工作空间中只有a,b两个File类实例'''
        File.count += 1

    def __str__(self):
        # 使用.format函数进行格式化输出，可以设定输出的位置和预留的长度
        s = '文件名：{0:>22}, 文件路径：{1:>8}, 文件大小：{2:>4}, 创建时间：{3:>8}, 文件类型：{4:>4}'.format(self.file_name, self.file_path,
                                                                                     self.file_size,
                                                                                     self.file_createTime,
                                                                                     self.file_type)
        return s

    def output_count(self):
        return self.count


# 定义可编辑文件类File_Ed
class File_Ed(File):
    count = 0

    def __init__(self, file_name, file_path, file_size, file_createTime, file_type, modify_time):
        super(File_Ed, self).__init__(file_name, file_path, file_size, file_createTime, file_type)  # 继承父类的实例变量
        self.modify_time = modify_time  # 定义新的实例变量

    def __str__(self):  # 修改字符串方法
        s = '文件名：{0:>22}, 文件路径：{1:>8}, 文件大小：{2:>4}, 创建时间：{3:>8}, 文件修改时间：{5:>8}，文件类型：{4:>4},'.format(self.file_name,
                                                                                                    self.file_path,
                                                                                                    self.file_size,
                                                                                                    self.file_createTime,
                                                                                                    self.file_type,
                                                                                                    self.modify_time)
        return s


# 定义含学号信息文件类File_Co
class File_Co(File):
    count = 0

    def __init__(self, file_name, file_path, file_size, file_createTime, file_type, file_code):
        super(File_Co, self).__init__(file_name, file_path, file_size, file_createTime, file_type)
        self.file_code = file_code

    def __str__(self):  # 修改字符串方法
        s = '学号：{5:>11}, 文件名：{0:>22}, 文件路径：{1:>8}, 文件大小：{2:>4}, 创建时间：{3:>8}, 文件类型：{4:>4} '.format(self.file_name,
                                                                                                  self.file_path,
                                                                                                  self.file_size,
                                                                                                  self.file_createTime,
                                                                                                  self.file_type,
                                                                                                  self.file_code)
        return s


# 对列表file_list中的文件信息进行分析
def file_by_list(file_list):
    file = []  # 将File等类文件存入列表
    file_ed = []
    file_co = []
    for file_ in file_list:  # 提取file_list中的每一行，即每个文件的信息
        file.append(File(file_[0], file_[1], file_[2], file_[3], file_[5]))  # 将文件信息的下标为01235的信息用于定义File类文件，并存入列表
        code_ = re.findall('(\d{10})', file_[0])  # 使用正则表达式提取长度为10的学号信息
        if file_[5] in ['xlsx', 'doc', 'txt', 'docx']:  # 判断文件类型是否为可修改类型
            # 定义File_Ed类时，第4个参数为文件类型，第5个参数为修改时间；实际在file_list中文件类型为第5个，修改时间为第4个
            file_ed.append(File_Ed(file_[0], file_[1], file_[2], file_[3], file_[5], file_[4]))
        if code_:  # 判断正则表达式提取结果是否为空，若非空则说明是含学号的文件
            code = code_[0]
            file_co.append(File_Co(file_[0], file_[1], file_[2], file_[3], file_[5], code))  # 将File_Co类定义并存入列表

    return file, file_ed, file_co  # 返回存储三种文件对象的列表


def main():
    # file_list中的每个子列表均包含一个文件的基本信息（文件名，文件路径，文件大小，文件创建日期，文件修改日期，文件类型）
    file_list = [['2012211216的请假条.jpg', 'F:\\test', '1', '20211207', '20211207', 'jpg'],
                 ['2012211998 实验报告.xlsx', 'F:\\test', '8', '20211207', '20211208', 'xlsx'],
                 ['2012217996 文件记录.doc', 'F:\\test', '4', '20211207', '20211207', 'doc'],
                 ['Python3 正则表达式.jpg', 'F:\\test', '81', '20211207', '20211207', 'jpg'],
                 ['Python3 面向对象.jpg', 'F:\\test', '103', '20211207', '20211207', 'jpg'],
                 ['实验报告 2013211216.xlsx', 'F:\\test', '8', '20211207', '20211209', 'xlsx'],
                 ['报告 2014217216 张三.xlsx', 'F:\\test', '5', '20211207', '20211207', 'xlsx'],
                 ['报告2014217226王五.docx', 'F:\\test', '8', '20211207', '20211207', 'docx'],
                 ['文件记录2012211216.txt', 'F:\\test', '4', '20211207', '20211208', 'txt']]

    # 函数调用，返回文件列表
    file, file_ed, file_co = file_by_list(file_list)
    # 输出所有3类实例的信息
    # 这里使用len函数而不是output_count方法是为了防止重复定义造成文件数比实际高
    print('共有{0}个文件，其中有{1}个可编辑文件，其中有{2}个含学号的文件：'.format(len(file), len(file_ed), len(file_co)))
    # 输出所有文件信息
    print('*' * 15 + '所有文件的信息：')
    for i in file:
        print(i)
    print('*' * 15 + '所有可编辑文件的信息：')
    for i in file_ed:
        print(i)
    print('*' * 15 + '所有含学号文件的信息：')
    for i in file_co:
        print(i)


if __name__ == '__main__':
    main()
