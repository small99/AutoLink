# -*- coding: utf-8 -*-

__author__ = "苦叶子"

"""

公众号: 开源优测

Email: lymking@foxmail.com

"""
import json
import codecs
from flask import current_app, session, request, send_file
from flask_restful import Resource, reqparse
from utils.file import exists_path


class Settings(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('method', type=str)
        self.parser.add_argument('ssl', type=bool, default=False)
        self.parser.add_argument('server', type=str)
        self.parser.add_argument('port', type=str)
        self.parser.add_argument('username', type=str)
        self.parser.add_argument('password', type=str)
        self.parser.add_argument('project', type=str)
        self.parser.add_argument('success_list', type=str)
        self.parser.add_argument('fail_list', type=str)
        self.app = current_app._get_current_object()

    def get(self):
        args = self.parser.parse_args()
        method = args["method"]

        conf_path = self.app.config["AUTO_HOME"] + "/auto.json"
        if method == "smtp":
            config = json.load(codecs.open(conf_path, 'r', 'utf-8'))
            result = {
                "ssl": config["smtp"]["ssl"],
                "server": config["smtp"]["server"],
                "port": config["smtp"]["port"],
                "username": config["smtp"]["username"],
                "password": config["smtp"]["password"]
            }
        elif method == "email":
            conf_path = self.app.config["AUTO_HOME"] + "/users/%s/config.json" % session["username"]
            config = json.load(codecs.open(conf_path, 'r', 'utf-8'))
            for p in config["data"]:
                if p["name"] == args["project"]:
                    result = {
                        "success_list": p["success_list"],
                        "fail_list": p["fail_list"]
                    }
                    break

        return result

    def post(self):
        args = self.parser.parse_args()
        method = args["method"]

        if method == "smtp":
            result = self.__smtp(args)
        elif method == "email":
            result = self.__email(args)

        return result, 201

    # 配置smtp
    def __smtp(self, args):
        result = {"status": "success", "msg": "配置smtp服务成功"}
        conf_path = self.app.config["AUTO_HOME"] + "/auto.json"
        if not exists_path(conf_path):
            make_nod(conf_path)
        try:
            config = json.load(codecs.open(conf_path, 'r', 'utf-8'))
            config["smtp"]["ssl"] = args["ssl"]
            config["smtp"]["server"] = args["server"]
            config["smtp"]["port"] = args["port"]
            config["smtp"]["username"] = args["username"]
            config["smtp"]["password"] = args["password"]
            json.dump(config, codecs.open(conf_path, 'w', 'utf-8'))

            self.app.config["MAIL_SERVER"] = args["server"]
            self.app.config["MAIL_PORT"] = args["port"]
            self.app.config["MAIL_USERNAME"] = args["username"]
            self.app.config["MAIL_PASSWORD"] = args["password"]
            self.app.config["MAIL_USE_SSL"] = args["ssl"]
        except Expetion as e:
            result["status"] = "fail"
            result["msg"] = str(e)

        return result

    # 设置email通知列表
    def __email(self, args):
        result = {"status": "success", "msg": "配置smtp服务成功"}

        conf_path = self.app.config["AUTO_HOME"] + "/users/%s/config.json" % (session["username"])
        try:
            config = json.load(codecs.open(conf_path, 'r', 'utf-8'))
            index = 0
            for p in config["data"]:
                if p["name"] == args["project"]:
                    config["data"][index]["success_list"] = args["success_list"]
                    config["data"][index]["fail_list"] = args["fail_list"]
                    break
                else:
                    index = index + 1
                    continue

            json.dump(config, codecs.open(conf_path, 'w', 'utf-8'))
        except Expetion as e:
            result["status"] = "fail"
            result["msg"] = str(e)

        return result
