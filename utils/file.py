# -*- coding: utf-8 -*-

__author__ = "苦叶子"

"""

公众号: 开源优测

Email: lymking@foxmail.com

"""

import os, stat, codecs
import shutil


def mk_dirs(path, mode=0o777):
    try:
        os.makedirs(path, mode=mode)
    except OSError:
        if not os.path.isdir(path):
            raise


def walk_dir(path):
    try:
        return os.walk(path)
    except OSError:
        if not os.path.exists(path):
            raise


def list_dir(path):
    try:
        return os.listdir(path)
    except OSError:
        if not os.path.exists(path):
            raise


def exists_path(path):
    if not os.path.exists(path):
        return False

    return True


def rename_file(src, dst):
    if exists_path(src) and not exists_path(dst):
        os.rename(src, dst)

        return True

    return False


def remove_readonly(func, path, _):
    """Clear the readonly bit and reattempt the removal"""
    os.chmod(path, stat.S_IWRITE)
    func(path)


def remove_dir(path):
    shutil.rmtree(path, onerror=remove_readonly)


def remove_file(path):
    os.remove(path)


def get_splitext(path):
    return os.path.splitext(path)


def make_nod(path, mode="w", encoding="utf-8"):
    if exists_path(path):
        return False

    f = codecs.open(path, mode, encoding)

    f.close()

    return True


def write_file(path, data, mode="w", encoding="utf-8"):
    if not exists_path(path):
        return False

    f = codecs.open(path, mode, encoding)

    f.write(data)

    f.close()

    return True


def read_file(path, mode="r", encoding="utf-8"):
    if not exists_path(path):
        return {"status": False, "data": ""}

    f = codecs.open(path, mode, encoding)

    data = f.read()

    f.close()

    return {"status": True, "data": data}

