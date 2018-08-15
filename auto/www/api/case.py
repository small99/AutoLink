# -*- coding: utf-8 -*-

__author__ = "苦叶子"

"""

公众号: 开源优测

Email: lymking@foxmail.com

"""

from flask import current_app, session, request, send_file
from flask_restful import Resource, reqparse
import werkzeug

from utils.file import exists_path, rename_file, make_nod, remove_file, write_file, read_file, get_splitext


class Case(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('method', type=str)
        self.parser.add_argument('name', type=str)
        self.parser.add_argument('new_name', type=str)
        self.parser.add_argument('project_name', type=str)
        self.parser.add_argument('suite_name', type=str)
        self.parser.add_argument('category', type=str)
        self.parser.add_argument('new_category', type=str)
        self.parser.add_argument('path', type=str)
        self.parser.add_argument('data', type=str)
        self.app = current_app._get_current_object()

    def get(self):
        args = self.parser.parse_args()
        result = {"status": "success", "msg": "读取文件成功"}

        ext = get_splitext(args["path"])
        result["ext"] = ext[1]

        path = self.app.config["AUTO_HOME"] + "/workspace/%s%s" % (session["username"], args["path"])
        data = read_file(path)
        if not data["status"]:
            result["status"] = "fail"
            result["msg"] = "读取文件失败"

        result["data"] = data["data"]

        return result, 201

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
        result = {"status": "success", "msg": "创建文件成功"}
        user_path = self.app.config["AUTO_HOME"] + "/workspace/%s/%s/%s/%s%s" % (session["username"],
                                                                                 args["project_name"],
                                                                                 args["suite_name"],
                                                                                 args["name"],
                                                                                 args["category"])
        if not exists_path(user_path):
            make_nod(user_path)
        else:
            result["status"] = "fail"
            result["msg"] = "文件名称重复，创建失败"

        return result

    def __edit(self, args):
        result = {"status": "success", "msg": "文件重命名成功"}
        old_name = self.app.config["AUTO_HOME"] + "/workspace/%s/%s/%s/%s%s" % (session["username"],
                                                                                args["project_name"],
                                                                                args["suite_name"],
                                                                                args["name"],
                                                                                args["category"])

        new_name = self.app.config["AUTO_HOME"] + "/workspace/%s/%s/%s/%s%s" % (session["username"],
                                                                                args["project_name"],
                                                                                args["suite_name"],
                                                                                args["new_name"],
                                                                                args["new_category"])

        if not rename_file(old_name, new_name):
            result["status"] = "fail"
            result["msg"] = "文件重命名失败，名称重复"

        return result

    def __delete(self, args):
        result = {"status": "success", "msg": "目录删除成功"}
        user_path = self.app.config["AUTO_HOME"] + "/workspace/%s/%s/%s/%s%s" % (session["username"],
                                                                                 args["project_name"],
                                                                                 args["suite_name"],
                                                                                 args["name"],
                                                                                 args["category"])
        if exists_path(user_path):
            remove_file(user_path)

        else:
            result["status"] = "fail"
            result["msg"] = "删除失败，不存在的文件"

        return result

    def __save(self, args):
        result = {"status": "success", "msg": "保存成功"}

        user_path = self.app.config["AUTO_HOME"] + "/workspace/%s%s" % (session["username"], args["path"])

        if not write_file(user_path, args["data"]):
            result["status"] = "fail"
            result["msg"] = "保存失败"

        return result


class ManageFile(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('data', type=str)
        self.parser.add_argument('file', type=werkzeug.datastructures.FileStorage, location='files', action='append')
        self.app = current_app._get_current_object()

    def post(self):
        args = request.form.to_dict()
        print(args)
        method = args["method"].lower()
        if method == "upload":
            file = request.files.to_dict()['files']
            return self.__upload(file, args['path']), 201
        elif method == "download":
            return self.__download(args)

    def __upload(self, file, path):
        result = {"status": "success", "msg": "上传成功"}

        user_path = self.app.config["AUTO_HOME"] + "/workspace/%s" % session['username'] + path + file.filename
        if not exists_path(user_path):
            file.save(user_path)
        else:
            result["status"] = "fail"
            result["msg"] = "上传失败"

        return result

    def __download(self, args):
        user_path = self.app.config["AUTO_HOME"] + "/workspace/%s" % session['username'] + args["path"]

        return send_file(user_path, mimetype='application/octet-stream', as_attachment=True)
