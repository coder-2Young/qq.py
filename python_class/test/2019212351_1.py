import random

# 第1题，使用一条语句，统计并输出100以内的所有素数。
print('第1题输出：' + str([i for i in range(2, 101) if 0 not in [i % j for j in range(2, i)]]))
# 判断0是否在小于i的整数的j除i的余数列表里，如果在则说明有能整除i的数，即i不是素数

# 第2题，使用一条语句，统计并输出40（含）以内的所有合数。
print('第2题输出：' + str([i for i in range(2, 41) if 0 in [i % j for j in range(2, i)]]))

# 第3题，使用一条语句，统计并输出100（含）以内所有能被4整除但不能被5整除的数字。
print('第3题输出：' + str([i for i in range(4, 101) if (i % 4 == 0) & (i % 5 != 0)]))

# 第4题，使用一条语句，统计并输出100（含）以内所有能被4整除但不能被5整除的数字的个数。
print('第4题输出：' + str(len([i for i in range(4, 100 + 1) if (i % 4 == 0) & (i % 5 != 0)])))

# 第5题，使用一条语句，统计并输出100（含）以内所有能被4整除但不能被5整除的数字的和。
print('第5题输出：' + str(sum([i for i in range(4, 100 + 1) if (i % 4 == 0) & (i % 5 != 0)])))

# 第6题，使用一条语句，统计并以字典形式输出结果，其键分别为从1到10的10个整数，其值为100（含）以内可以整除键的正整数的个数。
print('第6题输出：' + str({i: 100 // i for i in range(1, 11)}))  # 100内可以整除i的正整数的个数就是100//i

# 第7题，使用变量num存储本人学号。
# 使用一条语句，将num中的各位数字分别输出（以空格为分隔符）。
num = '2019212351'
print('第7题输出：' + ' '.join(num) + '\n')

# 第8题，使用一条语句，生成包含3个子列表的列表list10，其中每个子列表包含10个1-100间的随机整数。
# 分3行输出list10中的各子列表。
# 使用一条语句，输出其中所有元素之和最大的子列表。
# 使用一条语句，输出其中含有最大元素的子列表。
# 使用一条语句，输出其中含有最小元素的子列表。
print('第8题输出：')
list10 = [[random.randint(0, 100) for i in range(10)] for i in range(3)]
for list in list10:
    print(list)
print('所有元素之和最大的子列表：' + str([list for list in list10 if sum(list) == max(sum(list) for list in list10)]))
print('含有最大元素的子列表：' + str([list for list in list10 for i in list if i == max(i for list in list10 for i in list)]))
print(
    '含有最小元素的子列表：' + str([list for list in list10 for i in list if i == min(i for list in list10 for i in list)]) + '\n')

# 第9题，已知有一个包含一些学生成绩的字典scores。
# 使用一条语句，输出其中成绩的最高分、最低分、平均分。
# 使用一条语句，输出获得最高分和最低分的所有同学。
scores = {"Zhang San": 99, "Li Si": 78, "Wang Wu": 60, "Zhou Liu": 96, "Zhao Qi": 65, "Sun Ba": 90,
          "Zheng Jiu": 78, "Wu Shi": 99, "Dong Shiyi": 60}
print("第9题输出为：")
print("最高分为：" + str([value for value in scores.values() if value == max(scores.values())][0]), end=', ')
print("最低分为：" + str([value for value in scores.values() if value == min(scores.values())][0]), end=', ')
print("平均分为：" + str(sum([value for value in scores.values()]) / len(scores)))
print("获得最高分的同学有：" + str([key for key in scores.keys() if scores[key] == max(scores.values())]), end=', ')
print("获得最低分的同学有：" + str([key for key in scores.keys() if scores[key] == min(scores.values())]) + '\n')


# 第10题，定义具有一个参数n的函数Narcissistic()，用于生成所有n位的水仙花数。（所谓n位水仙花数是指1个n位的十进制数，其各位数字的n次方之和等于该数本身。）
# 在函数体内使用一条语句，生成所有n位的水仙花数。
# 通过return语句返回所有n位的水仙花数。
# 调用该函数，生成所有3位的水仙花数。

def Narcissistic(n):
    output = [target for target in range(10 ** (n - 1), 10 ** n) if
              sum([int(str(target)[dig]) ** n for dig in range(0, n)]) == target]
    return output


print('第10题输出：\n' + str(Narcissistic(3)) + '\n')


# 第11题，定义具有三个个参数num、start和end的函数RandomGeneration()，使用一条语句，生成num个介于start和end之间的不重复随机数。
# 将实参值存储在序列中，通过序列解包调用该函数，生成10个介于10和30之间的不重复随机数。
# 将实参值存储在字典中，通过序列解包调用该函数，生成10个介于40和60之间的不重复随机数。
def RandomGeneration(num, start, end):
    return [random.randint(start, end) for i in range(num)]


print("第11题输出：")
arg_list = [10, 10, 30]
print(RandomGeneration(*arg_list))
arg_dict = {'num': 10, 'start': 40, 'end': 60}
print(RandomGeneration(**arg_dict))

# 第12题，分析给定诗词序列poem，定义函数find_x(poem, x)，可在poem中查找所有含有字符x的诗句，并将该诗句的诗名、作者和相应诗句输出。
# 定义函数find_dup(poem)，可在poem中查找所有含有叠字的诗句，并将该诗句的诗名、作者和相应诗句输出。
# 调用所定义的两个函数，输出所有含有春的诗句信息，以及所有含有叠字的诗句信息。
poem = [['元日', '宋', '王安石', '爆竹声中一岁除', '春风送暖入屠苏', '千门万户曈曈日', '总把新桃换旧符'],
        ['小池', '宋', '杨万里', '泉眼无声惜细流', '树阴照水爱晴柔', '小荷才露尖尖角', '早有蜻蜓立上头'],
        ['春晓', '唐', '孟浩然', '春眠不觉晓', '处处闻啼鸟', '夜来风雨声', '花落知多少'],
        ['绝句', '唐', '杜甫', '两个黄鹂鸣翠柳', '一行白鹭上青天', '窗含西岭千秋雪', '门泊东吴万里船']]


def find_x(poem, x):
    for data in poem:
        for sentence in data[3:6]:
            if x in sentence:
                print(data[0] + ' ' + data[2] + ' ' + sentence)


def find_dup(poem):
    for data in poem:
        for sentence in data[3:6]:
            for i in range(0, len(sentence) - 1):
                if sentence[i] == sentence[i + 1]:
                    print(data[0] + ' ' + data[2] + ' ' + sentence)


print('\n第12题输出为：')
find_x(poem, '春')
find_dup(poem)
