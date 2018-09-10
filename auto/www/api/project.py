# -*- coding: utf-8 -*-

__author__ = "苦叶子"

"""

公众号: 开源优测

Email: lymking@foxmail.com

"""

from flask import current_app, session
from flask_restful import Resource, reqparse
import json
import os
import codecs

from robot.api import TestSuiteBuilder
from robot.api import TestData, ResourceFile, TestCaseFile

from utils.file import list_dir, mk_dirs, exists_path, rename_file, remove_dir, get_splitext
from utils.resource import ICONS


class Project(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('method', type=str)
        self.parser.add_argument('name', type=str)
        self.parser.add_argument('new_name', type=str)
        self.parser.add_argument('description', type=str)
        self.parser.add_argument('enable', type=str, default="否")
        self.parser.add_argument('cron', type=str, default="* * * * * *")
        self.parser.add_argument('boolean', type=str, default="启用")
        self.app = current_app._get_current_object()

    def get(self):
        args = self.parser.parse_args()

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
        result = {"status": "success", "msg": "创建项目成功"}

        user_path = self.app.config["AUTO_HOME"] + "/workspace/%s/%s" % (session["username"], args["name"])
        if not exists_path(user_path):
            mk_dirs(user_path)

            create_project(
                self.app,
                session["username"],
                {
                    "name": args["name"],
                    "description": args["description"],
                    "boolean": args["boolean"],
                    "enable": args["enable"],
                    "cron": args["cron"]
                }
            )
        else:
            result["status"] = "fail"
            result["msg"] = "项目名称重复，创建失败"

        return result

    def __edit(self, args):
        result = {"status": "success", "msg": "项目重命名成功"}
        old_name = self.app.config["AUTO_HOME"] + "/workspace/%s/%s" % (session["username"], args["name"])
        new_name = self.app.config["AUTO_HOME"] + "/workspace/%s/%s" % (session["username"], args["new_name"])

        if rename_file(old_name, new_name):
            edit_project(
                self.app,
                session["username"],
                args["name"],
                {
                    "name": args["new_name"],
                    "description": args["description"],
                    "boolean": args["boolean"],
                    "enable": args["enable"],
                    "cron": args["cron"]
                })
        else:
            result["status"] = "fail"
            result["msg"] = "项目重命名失败，名称重复"

        return result

    def __delete(self, args):
        result = {"status": "success", "msg": "项目删除成功"}
        user_path = self.app.config["AUTO_HOME"] + "/workspace/%s/%s" % (session["username"], args["name"])
        if exists_path(user_path):
            remove_dir(user_path)

            remove_project(self.app, session['username'], args['name'])
        else:
            result["status"] = "fail"
            result["msg"] = "删除失败，不存在的项目"

        return result


class ProjectList(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('name', type=str)
        self.parser.add_argument('category', type=str, default="root")
        self.parser.add_argument('project', type=str)
        self.parser.add_argument('suite', type=str)
        self.parser.add_argument('splitext', type=str)
        self.app = current_app._get_current_object()

    def get(self):
        args = self.parser.parse_args()

        if args["category"] == "root":
            return get_projects(self.app, session["username"])
        elif args["category"] == "project":
            return get_suite_by_project(self.app, session["username"], args)
        elif args["category"] == "suite":
            return get_case_by_suite(self.app, session["username"], args)
        elif args["category"] == "case":
            return get_step_by_case(self.app, session["username"], args)

        """
        projects = get_project_list(self.app, session['username'])
        children = []
        for p in projects:
            detail = get_project_detail(self.app, session['username'], p["name"])
            children.append({
                "text": p["name"],
                "iconCls": "icon-project",
                "state": "closed",
                "attributes": {
                    "name": p["name"],
                    "description": p["description"],
                    "category": "project",
                    "boolean": p["boolean"]
                },
                "children": detail
            })
        
        return [{
            "text": session['username'],
            "iconCls": "icon-workspace",
            "attributes": {
                "category": "root"
            },
            "children": children}]
        """


def create_project(app, username, project):
    user_path = app.config["AUTO_HOME"] + "/users/" + username
    if os.path.exists(user_path):
        config = json.load(codecs.open(user_path + '/config.json', 'r', 'utf-8'))
        config["data"].append(project)
        json.dump(config, codecs.open(user_path + '/config.json', 'w', 'utf-8'))


def edit_project(app, username, old_name, new_project):
    user_path = app.config["AUTO_HOME"] + "/users/" + username
    if os.path.exists(user_path):
        config = json.load(codecs.open(user_path + '/config.json', 'r', 'utf-8'))
        index = 0
        for p in config["data"]:
            if p["name"] == old_name:
                config["data"][index]["name"] = new_project["name"]
                config["data"][index]["description"] = new_project["description"]
                config["data"][index]["boolean"] = new_project["boolean"]
                break
            index += 1

    json.dump(config, codecs.open(user_path + '/config.json', 'w', 'utf-8'))


def remove_project(app, username, name):
    user_path = app.config["AUTO_HOME"] + "/users/" + username
    if os.path.exists(user_path):
        config = json.load(codecs.open(user_path + '/config.json', 'r', 'utf-8'))
        index = 0
        for p in config["data"]:
            if p["name"] == name:
                del config["data"][index]
                break
            index += 1

    json.dump(config, codecs.open(user_path + '/config.json', 'w', 'utf-8'))


def get_project_list(app, username):
    work_path = app.config["AUTO_HOME"] + "/workspace/" + username
    if os.path.exists(work_path):
        projects = list_dir(work_path)
        if len(projects) > 1:
            projects.sort()

            return projects

    return []


def get_project_detail(app, username, p_name):
    path = app.config["AUTO_HOME"] + "/workspace/" + username + "/" + p_name

    projects = []
    # raw_suites = list_dir(path)
    # suites = sorted(raw_suites, key=lambda x: os.stat(path + "/" + x).st_ctime)
    suites = list_dir(path)
    if len(suites) > 1:
        suites.sort()
    for d in suites:
        children = []
        # cases = sorted(list_dir(path + "/" + d), key=lambda x: os.stat(path + "/" + d + "/" + x).st_ctime)
        cases = list_dir(path + "/" + d)
        if len(cases) > 1:
            cases.sort()
        for t in cases:
            text = get_splitext(t)
            if text[1] == ".robot":
                icons = "icon-robot"
            elif text[1] == ".txt":
                icons = "icon-resource"
            else:
                icons = "icon-file-default"

            children.append({
                "text": t, "iconCls": icons,
                "attributes": {
                    "name": text[0], "category": "case", "splitext": text[1]
                }
            })
        if len(children) == 0:
            icons = "icon-suite"
        else:
            icons = "icon-suite-open"
        projects.append({
            "text": d, "iconCls": icons,
            "attributes": {
                "name": d, "category": "suite"
            },
            "children": children
        })

    return projects


def get_projects(app, username):
    projects = get_project_list(app, username)
    children = []
    for p in projects:
        children.append({
            "text": p, "iconCls": "icon-project", "state": "closed",
            "attributes": {
                "name": p,  # "description": p["description"],
                "category": "project",  # "boolean": p["boolean"]
            },
            "children": []
        })

    return [{
        "text": session['username'], "iconCls": "icon-workspace",
        "attributes": {
            "category": "root"
        },
        "children": children}]


def get_suite_by_project(app, username, args):
    path = app.config["AUTO_HOME"] + "/workspace/" + username + "/" + args["name"]

    suites = list_dir(path)
    children = []
    if len(suites) > 1:
        suites.sort()
    for d in suites:
        cases = list_dir(path + "/" + d)
        icons = "icon-suite"
        if len(cases) > 1:
            icons = "icon-suite-open"

        children.append({
            "text": d, "iconCls": icons, "state": "closed",
            "attributes": {
                "name": d, "category": "suite"
            },
            "children": []
        })

    return children


def get_case_by_suite(app, username, args):
    path = app.config["AUTO_HOME"] + "/workspace/" + username + "/%s/%s" % (args["project"], args["name"] )

    cases = list_dir(path)
    if len(cases) > 1:
        cases.sort()
    children = []
    for t in cases:
        text = get_splitext(t)
        if text[1] in ICONS:
            icons = ICONS[text[1]]
        else:
            icons = "icon-file-default"

        if text[1] in (".robot"):
            children.append({
                "text": t, "iconCls": icons, "state": "closed",
                "attributes": {
                    "name": text[0], "category": "case", "splitext": text[1]
                },
                "children": []
            })
        else:
            children.append({
                "text": t, "iconCls": icons, "state": "open",
                "attributes": {
                    "name": text[0], "category": "case", "splitext": text[1]
                }
            })

    return children


def get_step_by_case(app, username, args):
    print(args)
    path = app.config["AUTO_HOME"] + "/workspace/" + username + "/%s/%s/%s%s" % (args["project"], args["suite"], args["name"], args["splitext"])

    data = []
    if args["splitext"] == ".robot":
        data = get_case_data(path)

    return data


def get_case_data(path):
    suite = TestSuiteBuilder().build(path)
    children = []
    if suite:
        # add library
        for i in suite.resource.imports:
            children.append({
                "text": i.name, "iconCls": "icon-library", "state": "open",
                "attributes": {
                    "name": i.name, "category": "library"
                }
            })

        for v in suite.resource.variables:
            children.append({
                "text": v.name, "iconCls": "icon-variable", "state": "open",
                "attributes": {
                    "name": v.name, "category": "variable"
                }
            })

        for t in suite.tests:
            keys = []
            for k in t.keywords:
                keys.append({
                    "text": k.name, "iconCls": "icon-keyword", "state": "open",
                    "attributes": {
                        "name": k.name, "category": "keyword"
                    }
                })

            children.append({
                "text": t.name, "iconCls": "icon-step", "state": "closed",
                "attributes": {
                    "name": t.name, "category": "step"
                },
                "children": keys
            })

        for v in suite.resource.keywords:
            children.append({
                "text": v.name, "iconCls": "icon-user-keyword", "state": "open",
                "attributes": {
                    "name": v.name, "category": "user_keyword"
                }
            })

    return children
