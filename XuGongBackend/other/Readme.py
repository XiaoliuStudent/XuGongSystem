from flask.views import MethodView
from flask import request
import os


class Readme(MethodView):
    def __init__(self):
        self.db = None

    def get(self):
        with open("Readme.md", 'r') as f:
            readme_md = f.read()
        return {'sttaus': 200, "status_context": '请求成功', 'readme': readme_md}
