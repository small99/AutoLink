# -*- coding: utf-8 -*-

__author__ = "苦叶子"

"""

公众号: 开源优测

Email: lymking@foxmail.com

"""


from flask_restful import Resource, reqparse

from utils.parsing import parser_robot_keyword_list


class Keyword(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('category', type=str)

    def get(self):
        args = self.parser.parse_args()
        if args["category"] == "robot":
            return parser_robot_keyword_list()
