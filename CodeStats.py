# -*- coding: utf-8 -*-

__author__ = "苦叶子"

"""

公众号: 开源优测

Email: lymking@foxmail.com

"""

# coding=utf-8
import os
import time
basedir = os.getcwd()
filelists = []

# 指定想要统计的文件类型
whitelist = ['py', 'js']

filelists = []


# 遍历文件, 递归遍历文件夹中的所有
def get_file(base_dir):
    for parent, dirnames, filenames in os.walk(basedir):
        # for dirname in dirnames:
        # getFile(os.path.join(parent,dirname)) #递归

        for filename in filenames:
            if filename in ("AutoStats.py", "commonLibrary.py"):
                continue

            ext = filename.split('.')[-1]
            if ext == "js" and filename != "auto.js":
                continue

            # 只统计指定的文件类型，略过一些log和cache文件
            if ext in whitelist:
                filelists.append(os.path.join(parent, filename))


# 统计一个文件的行数
def count_line(fname):
    count = 0
    for file_line in open(fname).readlines():
        # 过滤掉空行
        if file_line != '' and file_line != '\n':
            count += 1
    print('%s ---- %s' % (fname, count))
    return count


if __name__ == '__main__' :
    startTime = time.clock()
    get_file(basedir)
    totalline = 0
    for filelist in filelists:
        totalline = totalline + count_line(filelist)

    print('total lines: %s' % totalline)
    print('Done! Cost Time: %0.2f second' % (time.clock() - startTime))