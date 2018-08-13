# -*- coding: utf-8 -*-

__author__ = "苦叶子"

"""

公众号: 开源优测

Email: lymking@foxmail.com

"""
from flask import current_app, url_for, redirect, session
from flask_restful import Resource, reqparse
from werkzeug.security import generate_password_hash, check_password_hash
import json
import os
import codecs


class Auth(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('username', type=str)
        self.parser.add_argument('password', type=str)

    def get(self):
        args = self.parser.parse_args()
        username = args["username"]

        if username in session:
            session.pop(username, None)

        return {"status": "success", "msg": "logout success", "url": url_for('routes.index')}, 201

    def post(self):
        args = self.parser.parse_args()
        username = args["username"]
        password = args["password"]
        app = current_app._get_current_object()
        user_path = app.config["AUTO_HOME"] + "/users/" + username
        if os.path.exists(user_path):
            user = json.load(codecs.open(user_path + '/config.json', 'r', 'utf-8'))
            if check_password_hash(user['passwordHash'], password):
                session['username'] = username
                return {"status": "success", "msg": "login success", "url": url_for('routes.dashboard')}, 201

        return {"status": "fail", "msg": "login fail", "url": url_for('routes.index')}, 201
