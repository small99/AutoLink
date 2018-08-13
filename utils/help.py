# -*- coding: utf-8 -*-

__author__ = "苦叶子"

"""

公众号: 开源优测

Email: lymking@foxmail.com

"""

import codecs
import requests


def check_version():
    f = codecs.open('version.txt', 'r')
    version = f.readline()
    s = requests.Session()
    r_version = s.get("https://gitee.com/lym51/AutoLink/raw/master/version.txt").text
    if version != r_version:
        print("*" * 25)
        print("本地版本：v%s" % version)
        print("github版本: v%s" % r_version)
        print("AutoLinK开源平台代码已有更新，请到下面的地址更新代码:")
        print("下载最新代码，直接覆盖本地即可")
        print("https://github.com/small99/AutoLink")
        print("*" * 25)
        exit(0)
    f.close()
