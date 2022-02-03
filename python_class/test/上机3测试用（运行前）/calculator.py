'''
基本思路是：
1.先把一个字符串形式的算式转化为数字和运算符组成的列表存储——例如1+（2+3）*4转化为['1','+','(','2','+','3',')','*','4']
2.从最内层括号开始，先计算括号内的内容，递归调用将所有括号内的内容都计算出来，使得列表变为['1','+','5','*','4']
3.计算乘/除，把乘除号两边的数字结果求出来
4.计算加/减
'''

import re
from math import *


# 先把字符串转化成列表
def eq_format(eq):
    format_list = re.findall('[\d\.]+|\(|\+|\-|\*|\/|\)|sin|cos|sqrt|exp', eq)  # 正则表达式模式为'找到数字、小数点的整体 或者 四则运算符'
    return format_list


# 对于存在+-，++等运算符联立的情况进行处理
def change(eq, count):
    if eq[count] == '-':
        if eq[count - 1] == '-':
            eq[count - 1] = '+'
            del eq[count]
        elif eq[count - 1] == '+':
            eq[count - 1] = '-'
            del eq[count]
    return eq


def remove_high_function(eq):
    count = 0
    for i in eq:
        if i == 'sin':
            if eq[count + 1] != '-':
                eq[count] = sin(float(eq[count + 1]))
                del (eq[count+1])
            elif eq[count + 1] == '-':
                eq[count+2] = -sin(float(eq[count+2]))
                eq[count] = '-'
                del (eq[count + 1])
            eq = change(eq, count - 1)
            return remove_high_function(eq)
        elif i == 'cos':
            if eq[count + 1] != '-':
                eq[count] = cos(float(eq[count + 1]))
                del (eq[count + 1])
            elif eq[count + 1] == '-':
                eq[count + 2] = cos(float(eq[count + 2]))
                del (eq[count])
                del (eq[count])
            eq = change(eq, count - 1)
            return remove_high_function(eq)
        elif i == 'sqrt':
            if eq[count + 1] != '-':
                eq[count] = sqrt(float(eq[count + 1]))
                del (eq[count + 1])
            else:
                pass  # 放在主函数里报错
        elif i == 'exp':
            if eq[count + 1] != '-':
                eq[count] = exp(float(eq[count + 1]))
                del (eq[count + 1])
            elif eq[count + 1] == '-':
                eq[count + 2] = exp(float(-eq[count + 2]))
                del (eq[count])
                del (eq[count])
            eq = change(eq, count - 1)
            return remove_high_function(eq)
        count = count + 1
    return eq


# 做乘除
def remove_multiplication_division(eq):
    count = 0
    for i in eq:
        if i == '*':
            if eq[count + 1] != '-':
                eq[count - 1] = float(eq[count - 1]) * float(eq[count + 1])
                del (eq[count])
                del (eq[count])
            elif eq[count + 1] == '-':
                eq[count] = float(eq[count - 1]) * float(eq[count + 2])
                eq[count - 1] = '-'
                del (eq[count + 1])
                del (eq[count + 1])
            eq = change(eq, count - 1)
            return remove_multiplication_division(eq)
        elif i == '/':
            if eq[count + 1] != '-':
                eq[count - 1] = float(eq[count - 1]) / float(eq[count + 1])
                del (eq[count])
                del (eq[count])
            elif eq[count + 1] == '-':
                eq[count] = float(eq[count - 1]) / float(eq[count + 2])
                eq[count - 1] = '-'
                del (eq[count + 1])
                del (eq[count + 1])
            eq = change(eq, count - 1)
            return remove_multiplication_division(eq)
        count = count + 1
    return eq


# 做加减
def remove_plus_minus(eq):
    count = 0
    if eq[0] != '-':
        sum = float(eq[0])
    else:
        sum = 0.0
    for i in eq:
        if i == '-':
            sum = sum - float(eq[count + 1])
        elif i == '+':
            sum = sum + float(eq[count + 1])
        count = count + 1
    if sum >= 0:
        eq = [str(sum)]
    else:
        eq = ['-', str(-sum)]
    return eq


# 最后计算
def calculate(s_eq):
    if 'sin' or 'cos' or 'sqrt' or 'exp' in s_eq:
        s_eq = remove_high_function(s_eq)
    if '*' or '/' in s_eq:
        s_eq = remove_multiplication_division(s_eq)
    if '+' or '-' in s_eq:
        s_eq = remove_plus_minus(s_eq)
    return s_eq


# 去括号
def simplify(format_list):
    bracket = 0  # 用于存放左括号在格式化列表中的索引
    count = 0
    for i in format_list:
        if i == '(':
            bracket = count
        elif i == ')':
            temp = format_list[bracket + 1: count]
            # print(temp)
            new_temp = calculate(temp)
            format_list = format_list[:bracket] + new_temp + format_list[count + 1:]
            format_list = change(format_list, bracket)  # 解决去括号后会出现的--  +- 问题
            return simplify(format_list)  # 递归去括号
        count = count + 1
    return format_list  # 当递归到最后一层的时候，不再有括号，因此返回列表


def caculator(eq):
    format_list = eq_format(eq)
    s_eq = simplify(format_list)
    ans = calculate(s_eq)
    if len(ans) == 2:
        ans = -float(ans[1])
    else:
        ans = float(ans[0])
    return ans
