# -*- coding: utf-8 -*-

__author__ = "苦叶子"

"""

公众号: 开源优测

Email: lymking@foxmail.com

"""

import os
import json
import codecs
from flask import Flask
from flask_login import LoginManager
# from flask_mail import Mail
from flask_apscheduler import APScheduler
from auto.configuration import config
from utils.file import list_dir
from utils.run import robot_job

# mail = Mail()
scheduler = APScheduler()
login_manager = LoginManager()
login_manager.login_view = 'auto.login'


def load_all_task(app):
    with app.app_context():
        user_path = app.config["AUTO_HOME"] + "/users/"
        users = list_dir(user_path)
        for user in users:
            if os.path.exists(user_path + user):
                if not os.path.exists(user_path + user + '/config.json'):
                    continue

                conf = json.load(codecs.open(user_path + user + '/config.json', 'r', 'utf-8'))
                data = conf['data']
                # 遍历项目
                for p in data:
                    if p["cron"] == "* * * * * *":
                        continue

                    cron = p["cron"].replace("\n", "").strip().split(" ")
                    if scheduler.get_job("%s_%s" % (user, p["name"])) is None:
                        scheduler.add_job(id="%s_%s" % (user, p["name"]),
                                          name=p["name"],
                                          func=robot_job,
                                          args=(app, p["name"], user),
                                          trigger="cron",
                                          replace_existing=True,
                                          second=cron[0],
                                          minute=cron[1],
                                          hour=cron[2],
                                          day=cron[3],
                                          month=cron[4],
                                          day_of_week=cron[5])
                    else:
                        scheduler.remove_job("%s_%s" % (user, p["name"]))
                        scheduler.add_job(id="%s_%s" % (user, p["name"]),
                                          name=p["name"],
                                          func=robot_job,
                                          args=(app, p["name"], user),
                                          trigger="cron",
                                          replace_existing=True,
                                          second=cron[0],
                                          minute=cron[1],
                                          hour=cron[2],
                                          day=cron[3],
                                          month=cron[4],
                                          day_of_week=cron[5])


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    login_manager.init_app(app)

    # mail.init_app(app)

    # app.config["MAIL"] = mail

    scheduler.init_app(app)
    scheduler.start()

    # for blueprints
    from .blueprints import routes as routes_blueprint
    app.register_blueprint(routes_blueprint)

    from .api import api_bp as api_blueprint
    app.register_blueprint(api_blueprint, url_prefix='/api/v1')

    if app.config['SSL_REDIRECT']:
        from flask_sslify import SSLify
        sslify = SSLify(app)

    return app
