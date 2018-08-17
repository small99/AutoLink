# -*- coding: utf-8 -*-

__author__ = "苦叶子"

"""

公众号: 开源优测

Email: lymking@foxmail.com

"""

import os
import xml.etree.ElementTree as ET


USER_KEYS = {
    "web": ["BuiltIn", "Collections", "DateTime", "String", "Screenshot", "SeleniumLibrary"],
    "app": ["BuiltIn", "Collections", "DateTime", "String", "Screenshot", "AppiumLibrary"],
    "http": ["BuiltIn", "Collections", "DateTime", "String", "RequestsLibrary"],
    "all": ["BuiltIn", "Collections", "DateTime",
            "OperatingSystem", "Process", "String", "Screenshot", "Telnet",
            "AppiumLibrary", "RequestsLibrary", "SeleniumLibrary", "SSHLibrary", "DatabaseLibrary"
            ]
}


def parser_robot_keyword_list():
    keyword_list = []
    cwd = os.getcwd() + "/keyword"
    for k in USER_KEYS['all']:
        path = cwd + "/%s.xml" % k
        tree = ET.parse(path)
        root = tree.getroot()
        name = root.attrib["name"]

        children = []
        for kw in root.iter("kw"):
            # 关键字
            keyword = kw.attrib["name"]

            # 关键字参数
            params = ""
            for arg in kw.iter("arg"):
                params += "\t" + arg.text
            params += "\n"

            # 使用说明
            doc = kw.find("doc").text

            children.append({
                "id": keyword,
                "text": keyword,
                "iconCls": "icon-keyword",
                "attributes": {
                    "keyword": keyword,
                    "category": "keyword",
                    "params": params,
                    "doc": doc
                }
            })

        keyword_list.append({
            "id": name,
            "text": name,
            "state": "closed",
            "iconCls": "icon-keyword-list",
            "attributes": {"category": name},
            "children": children
        })

    return keyword_list


def parser(doc_dir):

    for k in USER_KEYS["all"]:
        keyword_list = []
        path = doc_dir + "/%s.xml" % k
        tree = ET.parse(path)
        root = tree.getroot()
        name = root.attrib["name"]

        for kw in root.iter("kw"):
            # 关键字
            keyword_list.append("'" + kw.attrib["name"] + "'")

        print("rf_" + name + "=[" + ",".join(keyword_list))


def parser_with_args(doc_dir):

    for k in USER_KEYS["all"]:
        keyword_list = []
        path = doc_dir + "/%s.xml" % k
        tree = ET.parse(path)
        root = tree.getroot()
        name = root.attrib["name"]

        for kw in root.iter("kw"):
            # 关键字
            word = "'" + kw.attrib["name"]

            # 关键字参数
            for arg in kw.iter("arg"):
                word += "\t[" + arg.text + "]"

            word += "'"

            keyword_list.append(word)

        print("rf_" + name + "_args = [" + ",".join(keyword_list) + "];")


if __name__ == "__main__":
    doc_dir = "/Users/lyy/Documents/AutoLine/doc"
    parser_with_args(doc_dir)
