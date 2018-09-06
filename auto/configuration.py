# -*- coding: utf-8 -*-

__author__ = "苦叶子"

"""

公众号: 开源优测

Email: lymking@foxmail.com

"""
import logging
import os
import json
import codecs
from apscheduler.executors.pool import ProcessPoolExecutor

from utils.file import exists_path


class Config:
    # conf_path = os.getcwd() + "/.beats/auto.json"

    #if exists_path(conf_path):
    #    config = json.load(codecs.open(conf_path, 'r', 'utf-8'))

    #    MAIL_SERVER = config["smtp"]["server"]
    #    MAIL_PORT = config["smtp"]["port"]
    #    MAIL_USE_TLS = True
    #    MAIL_USERNAME = config["smtp"]["username"]
    #    MAIL_PASSWORD = config["smtp"]["password"]
    #    DEFAULT_MAIL_SENDER = "lymking@foxmail.com"
    #    FLASKY_ADMIN = config["smtp"]["username"]
    #    MAIL_USE_SSL = config["smtp"]["ssl"]

    # MAIL_DEBUG = True
    SSL_REDIRECT = False

    SECRET_KEY = 'QWERTYUIOPASDFGHJ'
    # logging level
    LOGGING_LEVEL = logging.INFO
    AUTO_HOME = os.getcwd().replace('\\', '/') + '/.beats'

    AUTO_ROBOT = []

    executors = {
        'default': {'type': 'threadpool', 'max_workers': 20},
        'processpool': ProcessPoolExecutor(max_workers=5)
    }

    job_defaults = {
        'coalesce': False,
        'max_instances': 10
    }

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True


class ProductionConfig(Config):
    DEBUG = False

    @classmethod
    def init_app(cls, app):
        Config.init_app(app)

        # 发送服务启动初始化时错误信息给管理员
        import logging
        from logging.handlers import SMTPHandler
        credentials = None
        secure = None
        if getattr(cls, 'MAIL_USERNAME', None) is not None:
            credentials = (cls.MAIL_USERNAME, cls.MAIL_PASSWORD)
            if getattr(cls, 'MAIL_USE_TLS', None):
                secure = ()

        mail_handler = SMTPHandler(
            mailhost=(cls.MAIL_SERVER, cls.MAIL_PORT),
            fromaddr=cls.FLASKY_MAIL_SENDER,
            toaddrs=[cls.FLASKY_ADMIN],
            subject=cls.FLASKY_MAIL_SUBJECT_PREFIX + ' AutoLine Startup Error',
            credentials=credentials,
            secure=secure)

        mail_handler.setLevel(logging.ERROR)
        app.logger.addHandler(mail_handler)


config = {
    "development": DevelopmentConfig,
    "production": ProductionConfig,

    "default": DevelopmentConfig
}
