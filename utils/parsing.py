# -*- coding: utf-8 -*-

__author__ = "苦叶子"

"""

公众号: 开源优测

Email: lymking@foxmail.com

"""

import os
import codecs
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
            doc_params = []
            for arg in kw.iter("arg"):
                params += "\t[" + arg.text + "]"
                doc_params.append(arg.text)
            params += "\n"
            if len(doc_params) == 0:
                doc_params = "无"

            # 使用说明
            doc = kw.find("doc").text
            if doc is not None:
                doc_help = doc .replace("\n", "<br>").replace("\r\t", "<br>")
            else:
                doc_help = doc

            children.append({
                "id": keyword,
                "text": keyword,
                "iconCls": "icon-keyword",
                "attributes": {
                    "keyword": keyword,
                    "category": "keyword",
                    "params": params,
                    "doc": "<p>关键字: %s<br><br/>所属库: %s<br><br>参数: <br>%s<br><br>文档:<br>%s</p>" % (keyword, k, " | ".join(doc_params), doc_help)
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


def generate_high_light(doc_dir):
    ff = codecs.open(os.getcwd() + "/auto/www/static/js/highlight.js", "w", "utf-8")
    keyword_list = []
    for k in USER_KEYS["all"]:
        path = doc_dir + "/%s.xml" % k
        tree = ET.parse(path)
        root = tree.getroot()
        name = root.attrib["name"]

        for kw in root.iter("kw"):
            # 关键字
            keyword_list.append("'" + kw.attrib["name"] + "'")
    kewords = "var high_light=" + "[" + ",".join(keyword_list) + "];"
    ff.write(kewords)
    ff.close()


def generate_auto_complete(doc_dir):
    ff = codecs.open(os.getcwd() + "/auto/www/static/js/autocomplete.js", "w", "utf-8")
    keyword_list = []
    for k in USER_KEYS["all"]:
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

    kewords = "var auto_complete=" + "[" + ",".join(keyword_list) + "];"
    ff.write(kewords)
    ff.close()


if __name__ == "__main__":
    path = os.getcwd() + "/keyword"
    generate_high_light(path)
    generate_auto_complete(path)
