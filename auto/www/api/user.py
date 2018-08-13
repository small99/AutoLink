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
from werkzeug.security import generate_password_hash, check_password_hash

from utils.file import list_dir, exists_path, rename_file, make_nod, remove_dir, write_file, read_file, mk_dirs


class User(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('method', type=str)
        self.parser.add_argument('username', type=str)
        self.parser.add_argument('password', type=str)
        self.parser.add_argument('new_password', type=str, default="")
        self.parser.add_argument('email', type=str)
        self.parser.add_argument('fullname', type=str)
        self.app = current_app._get_current_object()

    def get(self):
        user_list = {"total": 0, "rows": []}
        user_path = self.app.config["AUTO_HOME"] + "/users"
        if exists_path(user_path):
            users = list_dir(user_path)

            user_list["total"] = len(users)
            for user in users:
                if user == "AutoLink":
                    category = "管理员"
                else:
                    category = "普通用户"
                config = json.load(codecs.open(user_path + "/" + user + '/config.json', 'r', 'utf-8'))
                user_list["rows"].append({ "name": user, "fullname": config["fullname"], "email": config["email"], "category": category })

        return user_list

    def post(self):
        args = self.parser.parse_args()

        method = args["method"].lower()
        if method == "create":
            result = self.__create(args)
        elif method == "edit":
            result = self.__edit(args)
        elif method == "delete":
            result = self.__delete(args)
        elif method == "save":
            result = self.__save(args)
        else:
            print(request.files["files"])

        return result, 201

    def __create(self, args):
        result = {"status": "success", "msg": "创建用户成功"}
        user_path = self.app.config["AUTO_HOME"] + "/users/%s" % (args["username"])
        if not exists_path(user_path):
            mk_dirs(user_path)

            make_nod(user_path + "/config.json")

            user = {"fullname": args["fullname"],
                    "email": args["email"],
                    "passwordHash": generate_password_hash(args["password"]),
                    "data": []}
            json.dump(user, codecs.open(user_path + '/config.json', 'w', 'utf-8'))
        else:
            result["status"] = "fail"
            result["msg"] = "用户名称重复，创建失败"

        return result

    def __edit(self, args):

        result = {"status": "success", "msg": "用户信息修改成功"}
        user_path = self.app.config["AUTO_HOME"] + "/users/" + args["username"]
        if exists_path(user_path):
            config = json.load(codecs.open(user_path + '/config.json', 'r', 'utf-8'))
            if check_password_hash(config["passwordHash"], args["password"]):
                config["passwordHash"] = generate_password_hash(args["new_password"])
                config["fullname"] = args["fullname"]
                config["email"] = args["email"]
                json.dump(config, codecs.open(user_path + '/config.json', 'w', 'utf-8'))
            else:
                result["status"] = "fail"
                result["msg"] = "原始密码错误"
        else:
            result["status"] = "fail"
            result["msg"] = "用户不存在"

        return result

    def __delete(self, args):
        result = {"status": "success", "msg": "用户删除成功"}
        user_path = self.app.config["AUTO_HOME"] + "/users/" + args["username"]

        if exists_path(user_path):
            config = json.load(codecs.open(user_path + '/config.json', 'r', 'utf-8'))
            if len(config["data"]) > 0:
                result["status"] = "fail"
                result["msg"] = "请先删除该用户拥有的项目"
            else:
                remove_dir(user_path)

        else:
            result["status"] = "fail"
            result["msg"] = "用户不存在，删除失败"

        return result

    def __save(self, args):
        result = {"status": "success", "msg": "保存成功"}

        user_path = self.app.config["AUTO_HOME"] + "/workspace/%s%s" % (session["username"], args["path"])

        if not write_file(user_path, args["data"]):
            result["status"] = "fail"
            result["msg"] = "保存失败"

        return result
