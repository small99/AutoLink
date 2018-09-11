# -*- coding: utf-8 -*-

__author__ = "苦叶子"

"""

公众号: 开源优测

Email: lymking@foxmail.com

"""

from flask import current_app, session, url_for
from flask_restful import Resource, reqparse
import json
import os
import codecs
import threading
import multiprocessing
from dateutil import tz

from robot.api import ExecutionResult

from utils.file import exists_path, read_file, remove_dir
from utils.run import robot_run, is_run, remove_robot, stop_robot, robot_job
from ..app import scheduler


class Task(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('method', type=str)
        self.parser.add_argument('category', type=str)
        self.parser.add_argument('project', type=str)
        self.parser.add_argument('suite', type=str)
        self.parser.add_argument('case', type=str)
        self.parser.add_argument('task_no', type=str)
        self.app = current_app._get_current_object()

    def post(self):
        args = self.parser.parse_args()
        category = args["category"].lower()
        if args["method"] == "run":
            project = self.app.config["AUTO_HOME"] + "/workspace/%s/%s" % (session['username'], args["project"])
            output = self.app.config["AUTO_HOME"] + "/jobs/%s/%s" % (session['username'], args["project"])
            if category == "project":
                if not is_run(self.app, args["project"]):
                    p = multiprocessing.Process(target=robot_run, args=(session["username"], args["project"], project, output))
                    p.start()
                    self.app.config["AUTO_ROBOT"].append({"name": args["project"], "process": p})
                else:
                    return {"status": "fail", "msg": "请等待上一个任务完成"}
            elif category == "suite":
                case_path = project + "/%s" % args["suite"]
                if not is_run(self.app, args["project"]):
                    p = multiprocessing.Process(target=robot_run, args=(session["username"], args["project"], case_path, output))
                    p.start()
                    self.app.config["AUTO_ROBOT"].append({"name": args["project"], "process": p})
                else:
                    return {"status": "fail", "msg": "请等待上一个任务完成"}
            elif category == "case":
                case_path = project + "/%s/%s" % (args["suite"], args["case"])
                if not is_run(self.app, args["project"]):
                    p = multiprocessing.Process(target=robot_run,
                                                args=(session["username"], args["project"], case_path, output))
                    p.start()
                    self.app.config["AUTO_ROBOT"].append(
                        {"name": "%s" % args["project"], "process": p})
                else:
                    return {"status": "fail", "msg": "请等待上一个任务完成"}

            return {"status": "success", "msg": "已启动运行"}
        elif args["method"] == "stop":
            stop_robot(self.app, args["project"])

            return {"status": "success", "msg": "已停止运行"}
        elif args["method"] == "delete":
            delete_task_record(self.app, args["project"], args["task_no"])

            return {"status": "success", "msg": "已经删除记录"}


class TaskList(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('method', type=str)
        self.parser.add_argument('name', type=str)
        self.parser.add_argument('cron', type=str)
        self.app = current_app._get_current_object()

    def get(self):
        args = self.parser.parse_args()
        project = args["name"]

        return get_task_list(self.app, session['username'], project)

    def post(self):
        args = self.parser.parse_args()
        if args["method"] == "query":
            return get_all_task(self.app)
        elif args["method"] == "start":
            result = {"status": "success", "msg": "调度启动成功"}
            job_id = "%s_%s" % (session["username"], args["name"])
            lock = threading.Lock()
            lock.acquire()
            job = scheduler.get_job(job_id)
            if job:
                scheduler.remove_job(job_id)
            cron = args["cron"].replace("\n", "").strip().split(" ")
            if args["cron"] != "* * * * * *" and len(cron) == 6:
                scheduler.add_job(id=job_id,
                                  name=args["name"],
                                  func=robot_job,
                                  args=(self.app, args["name"], session["username"]),
                                  trigger="cron",
                                  second=cron[0],
                                  minute=cron[1],
                                  hour=cron[2],
                                  day=cron[3],
                                  month=cron[4],
                                  day_of_week=cron[5])
            else:
                result["msg"] = "cron表达式为默认* * * * * *, <br><br>无法启动调度，请修改cron表达式"
            lock.release()
            return result

        elif args["method"] == "stop":
            lock = threading.Lock()
            lock.acquire()
            job = scheduler.get_job(job_id)
            if job:
                scheduler.remove_job(id="%s_%s" % (session["username"], args["name"]))
            lock.release()
            return {"status": "success", "msg": "停止调度成功"}
        elif args["method"] == "edit":

            result = edit_cron(self.app, args["name"], args["cron"])
            if result:
                job_id = "%s_%s" % (session["username"], args["name"])
                lock = threading.Lock()
                lock.acquire()
                job = scheduler.get_job(job_id)
                if job:
                    scheduler.remove_job(job_id)

                cron = args["cron"].replace("\n", "").strip().split(" ")
                if args["cron"] != "* * * * * *" and len(cron) == 6:
                    scheduler.add_job(id=job_id,
                                      name=args["name"],
                                      func=robot_job,
                                      args=(self.app, args["name"], session["username"]),
                                      trigger="cron",
                                      second=cron[0],
                                      minute=cron[1],
                                      hour=cron[2],
                                      day=cron[3],
                                      month=cron[4],
                                      day_of_week=cron[5])
                lock.release()

            return {"status": "success", "msg": "更新调度成功"}


def get_task_list(app, username, project):
    job_path = app.config["AUTO_HOME"] + "/jobs/%s/%s" % (username, project)
    next_build = 0
    task = []
    if exists_path(job_path):
        next_build = get_next_build_number(job_path)
        if next_build != 0:
            # 遍历所有任务结果
            # 判断最近一个任务状态
            icons = {
                "running": url_for('static', filename='img/running.gif'),
                "success": url_for('static', filename='img/success.png'),
                "fail": url_for('static', filename='img/fail.png'),
                "exception": url_for('static', filename='img/exception.png')}

            #if exists_path(job_path + "/%s" % (next_build - 1)):
            running = False
            lock = threading.Lock()
            lock.acquire()
            remove_robot(app)
            for p in app.config["AUTO_ROBOT"]:
                if p["name"] == project:
                    running = True
                    break
            lock.release()
            if running:
                task.append(
                   {
                       "status": icons["running"],
                       "name": "%s_#%s" % (project, next_build-1),
                       "success": "",
                       "fail": ""
                   }
                )
            last = 1
            if running:
                last = 2
            for i in range(next_build-last, -1, -1):
                if exists_path(job_path + "/%s" % i):
                    try:
                        suite = ExecutionResult(job_path + "/%s/output.xml" % i).suite
                        stat = suite.statistics.critical
                        if stat.failed != 0:
                            status = icons["fail"]
                        else:
                            status = icons['success']
                        task.append({
                            "task_no": i,
                            "status": status,
                            "name": "<a href='/view_report/%s/%s' target='_blank'>%s_#%s</a>" % (project, i, project, i),
                            "success": stat.passed,
                            "fail": stat.failed,
                            "starttime": suite.starttime,
                            "endtime": suite.endtime,
                            "elapsedtime": suite.elapsedtime,
                            "note": ""
                        })
                    except:
                        status = icons["exception"]
                        if i == next_build-last:
                            status = icons["running"]
                        task.append({
                            "task_no": i,
                            "status": status,
                            "name": "%s_#%s" % (project, i),
                            "success": "-",
                            "fail": "-",
                            "starttime": "-",
                            "endtime": "-",
                            "elapsedtime": "-",
                            "note": "异常"
                        })

    return {"total": next_build-1, "rows": task}


def get_last_task(app, username, project):
    icons = {
        "running": url_for('static', filename='img/running.gif'),
        "success": url_for('static', filename='img/success.png'),
        "fail": url_for('static', filename='img/fail.png'),
        "exception": url_for('static', filename='img/exception.png')}
    job_path = app.config["AUTO_HOME"] + "/jobs/%s/%s" % (username, project)
    status = icons["running"]
    if exists_path(job_path):
        next_build = get_next_build_number(job_path)
        last_job = next_build-1
        if exists_path(job_path + "/%s" % last_job):
            try:
                suite = ExecutionResult(job_path + "/%s/output.xml" % last_job).suite
                stat = suite.statistics.critical
                if stat.failed != 0:
                    status = icons["fail"]
                else:
                    status = icons['success']
            except:
                status = icons["running"]
        else:
            status = icons["exception"]
    else:
        status = icons['success']

    return status


def get_all_task(app):
    user_path = app.config["AUTO_HOME"] + "/users/" + session["username"]
    if exists_path(user_path):
        config = json.load(codecs.open(user_path + '/config.json', 'r', 'utf-8'))
        projects = config['data']
        task_list = {"total": len(projects), "rows": []}
        for p in projects:
            # job_path = app.config["AUTO_HOME"] + "/jobs/%s/%s" % (session["username"], p["name"])
            # running = False
            # lock = threading.Lock()
            # lock.acquire()
            # remove_robot(app)
            # next_build = get_next_build_number(job_path)
            # if next_build != 0:
            #     for pp in app.config["AUTO_ROBOT"]:
            #         if pp["name"] == p["name"]:
            #             running = True
            #             status = icons["running"]
            #             break
            #     if running is False:
            #         if exists_path(job_path + "/%s" % (next_build-1)):
            #             try:
            #                 suite = ExecutionResult(job_path + "/%s/output.xml" % (next_build-1)).suite
            #                 stat = suite.statistics.critical
            #                 if stat.failed != 0:
            #                     status = icons["fail"]
            #                 else:
            #                     status = icons['success']
            #             except:
            #                 status = icons["running"]
            # else:
            #     status = icons['success']

            # lock.release()
            task = {
                #"status": status,
                "name": p["name"],
                #"last_success": get_last_pass(job_path + "/lastPassed"),
                #"last_fail": get_last_fail(job_path + "/lastFail"),
                "enable": p["enable"],
                "next_time": get_next_time(app, p["name"]),
                "cron": p["cron"],
                "status": get_last_task(app, session["username"], p["name"])
            }

            task_list["rows"].append(task)

    return task_list


def get_last_pass(job_path):
    passed = "无"
    passed_path = job_path + "lastPassed"
    if exists_path(passed_path):
        f = codecs.open(passed_path, "r", "utf-8")

        passed = f.read()

        f.close()

    return passed


def get_last_fail(job_path):
    fail = "无"
    fail_path = job_path + "lastFail"
    if exists_path(fail_path):
        f = codecs.open(fail_path, "r", "utf-8")

        fail = f.read()

        f.close()

    return fail


def get_next_build_number(job_path):
    next_build_number = 1
    next_path = job_path + "/nextBuildNumber"
    if exists_path(next_path):
        f = codecs.open(next_path, "r", "utf-8")

        next_build_number = int(f.read())

        f.close()

    return next_build_number


def get_next_time(app, name):
    job = scheduler.get_job("%s_%s" % (session["username"], name))
    if job:
        to_zone = tz.gettz("CST")
        return job.next_run_time.astimezone(to_zone).strftime("%Y-%m-%d %H:%M:%S")
    else:
        return "-"


def edit_cron(app, name, cron):
    user_path = app.config["AUTO_HOME"] + "/users/" + session["username"]
    if os.path.exists(user_path):
        config = json.load(codecs.open(user_path + '/config.json', 'r', 'utf-8'))
        index = 0
        for p in config["data"]:
            if p["name"] == name:
                config["data"][index]["cron"] = cron
                break
            index += 1

        json.dump(config, codecs.open(user_path + '/config.json', 'w', 'utf-8'))

        return True

    return False


def delete_task_record(app, name, task_no):
    task_path = app.config["AUTO_HOME"] + "/jobs/" + session["username"] + "/%s/%s" % (name, task_no)
    if os.path.exists(task_path):
        remove_dir(task_path)
