# -*- coding: utf-8 -*-

__author__ = "苦叶子"

"""

公众号: 开源优测

Email: lymking@foxmail.com

"""
from flask import current_app, session
import threading
import multiprocessing
import time
from robot.api import TestSuiteBuilder, ResultWriter, ExecutionResult

from utils.file import exists_path, make_nod, write_file, read_file, mk_dirs


def robot_job(app, name, username):
    with app.app_context():
        project = app.config["AUTO_HOME"] + "/workspace/%s/%s" % (username, name)
        output = app.config["AUTO_HOME"] + "/jobs/%s/%s" % (username, name)
        if not is_run(app, project):
            p = multiprocessing.Process(target=robot_run, args=(project, output))
            p.start()
            app.config["AUTO_ROBOT"].append({"name": project, "process": p})
            print("-+" * 15)
            print(app.config["AUTO_ROBOT"])
            print("-+" * 15)


def robot_run(name, output):
    if not exists_path(output):
        mk_dirs(output)

    suite = TestSuiteBuilder().build(name)

    (out, index) = reset_next_build_numb(output)

    result = suite.run(output_directory=out,
                       output=out + "/output.xml",
                       debugfile=out + "/debug.txt",
                       log_level="TRACE")

    # reset_last_status(result, output, index)

    # Report and xUnit files can be generated based on the result object.
    # ResultWriter(result).write_results(report=out + '/report.html', log=out + '/log.html')
    detail_result = ExecutionResult(out + "/output.xml")

    # detail_result.save(out + "/output_new.xml")
    reset_last_status(detail_result, output, index)

    # Report and xUnit files can be generated based on the result object.
    ResultWriter(detail_result).write_results(report=out + '/report.html', log=out + '/log.html')


def reset_next_build_numb(output):
    next_build_number = output + "/nextBuildNumber"
    index = 1
    data = "%d" % (index + 1)
    if not exists_path(next_build_number):
        make_nod(next_build_number)
    else:
        index = int(read_file(next_build_number)["data"])
        data = "%d" % (index + 1)
    write_file(next_build_number, data)

    out = output + "/%d" % index
    if not exists_path(output):
        mk_dirs(output)

    return (out, index)


def reset_last_status(result, output, index):
    stats = result.statistics
    fail = stats.total.critical.failed

    last_fail = output + "/lastFail"
    last_passed = output + "/lastPassed"
    data = "%d" % index

    if fail != 0:
        if not exists_path(last_fail):
            make_nod(last_fail)

        write_file(last_fail, data)
    else:
        if not exists_path(last_passed):
            make_nod(last_passed)
        write_file(last_passed, data)


def remove_robot(app):
    lock = threading.Lock()
    lock.acquire()
    for p in app.config["AUTO_ROBOT"]:
        if not p["process"].is_alive():
            app.config["AUTO_ROBOT"].remove(p)
            break
    lock.release()


def stop_robot(app, name):
    lock = threading.Lock()
    lock.acquire()
    for p in app.config["AUTO_ROBOT"]:
        if name == p["name"]:
            if p["process"].is_alive():
                p["process"].terminate()
                time.sleep(0.2)
                app.config["AUTO_ROBOT"].remove(p)
                break

    lock.release()

    return True


def is_run(app, name):
    remove_robot(app)
    for p in app.config["AUTO_ROBOT"]:
        if name == p["name"]:
            return True

    return False


class RobotRun(threading.Thread):
    def __init__(self, name, output, lock, executor="auto"):
        threading.Thread.__init__(self)
        self.lock = lock
        self.project = name
        self.output = output
        self.executor = executor
        self.suite = None
        self.result = None

    def run(self):
        #lock = threading.Lock()

        # self.lock.acquire()
        if not exists_path(self.output):
            mk_dirs(self.output)

        self.suite = TestSuiteBuilder().build(self.project)

        (output, index) = self.reset_next_build_numb()

        self.setName(output)

        self.result = self.suite.run(output_directory=output,
                                     output=output + "/output.xml",
                                     debugfile=output + "/debug.txt",
                                     log_level="TRACE")

        # self.reset_last_status(index)

        # Report and xUnit files can be generated based on the result object.
        # ResultWriter(self.result).write_results(report=output + '/report.html', log=output + '/log.html')

        # self.lock.release()

        # Generating log files requires processing the earlier generated output XML.
        # ResultWriter(self.output + '/output.xml').write_results()

        self.result = ExecutionResult(out + "/output.xml")

        self.reset_last_status(self.result, output, index)

        # Report and xUnit files can be generated based on the result object.
        ResultWriter(self.result).write_results(report=out + '/report.html', log=out + '/log.html')

    def reset_next_build_numb(self):

        next_build_number = self.output + "/nextBuildNumber"
        index = 1
        data = "%d" % (index + 1)
        if not exists_path(next_build_number):
            make_nod(next_build_number)
        else:
            index = int(read_file(next_build_number)["data"])
            data = "%d" % (index + 1)
        write_file(next_build_number, data)

        output = self.output + "/%d" % index
        if not exists_path(output):
            mk_dirs(output)

        return (output, index)

    def reset_last_status(self, index):
        stats = self.result.statistics
        fail = stats.total.critical.failed

        lock = threading.Lock()

        lock.acquire()
        last_fail = self.output + "/lastFail"
        last_passed = self.output + "/lastPassed"
        data = "%d" % index

        if fail != 0:
            if not exists_path(last_fail):
                make_nod(last_fail)

            write_file(last_fail, data)
        else:
            if not exists_path(last_passed):
                make_nod(last_passed)
            write_file(last_passed, data)

        lock.release()