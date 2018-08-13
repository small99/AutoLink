# -*- coding: utf-8 -*-

__author__ = "苦叶子"

"""

公众号: 开源优测

Email: lymking@foxmail.com

"""


class AutoBeatException(Exception):
    pass


class AutoBeatConfigException(AutoBeatException):
    pass


class AutoBeatExecutorTimeout(AutoBeatException):
    pass


class AutoBeatTaskTimeout(AutoBeatException):
    pass


class AutoBeatWebServerTimeout(AutoBeatException):
    pass


class AutoBeatSkipException(AutoBeatException):
    pass
