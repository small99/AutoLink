# -*- coding: utf-8 -*-

__author__ = "苦叶子"

"""

公众号: 开源优测

Email: lymking@foxmail.com

"""

from flask import current_app, session
from flask_restful import Resource, reqparse

from utils.file import mk_dirs, exists_path, rename_file, remove_dir


class Suite(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('method', type=str)
        self.parser.add_argument('name', type=str)
        self.parser.add_argument('new_name', type=str)
        self.parser.add_argument('project_name', type=str)
        self.app = current_app._get_current_object()

    def post(self):
        args = self.parser.parse_args()

        method = args["method"].lower()
        if method == "create":
            result = self.__create(args)
        elif method == "edit":
            result = self.__edit(args)
        elif method == "delete":
            result = self.__delete(args)

        return result, 201

    def __create(self, args):
        result = {"status": "success", "msg": "创建目录成功"}
        user_path = self.app.config["AUTO_HOME"] + "/workspace/%s/%s/%s" % (session["username"], args["project_name"], args["name"])
        if not exists_path(user_path):
            mk_dirs(user_path)
        else:
            result["status"] = "fail"
            result["msg"] = "目录名称重复，创建失败"

        return result

    def __edit(self, args):
        result = {"status": "success", "msg": "目录重命名成功"}
        old_name = self.app.config["AUTO_HOME"] + "/workspace/%s/%s/%s" % (session["username"], args["project_name"], args["name"])
        new_name = self.app.config["AUTO_HOME"] + "/workspace/%s/%s/%s" % (session["username"], args["project_name"], args["new_name"])

        if not rename_file(old_name, new_name):
            result["status"] = "fail"
            result["msg"] = "目录重命名失败，名称重复"

        return result

    def __delete(self, args):
        result = {"status": "success", "msg": "目录删除成功"}
        user_path = self.app.config["AUTO_HOME"] + "/workspace/%s/%s/%s" % (session["username"], args["project_name"], args["name"])
        if exists_path(user_path):
            remove_dir(user_path)

        else:
            result["status"] = "fail"
            result["msg"] = "删除失败，不存在的目录"

        return result
