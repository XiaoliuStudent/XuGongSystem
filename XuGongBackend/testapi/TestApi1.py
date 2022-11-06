from flask.views import MethodView
from flask import request


class TestApi1(MethodView):
    def __init__(self):
        pass

    def get(self, *args, **kwargs):
        print('args', request.args.get("class_name"))
        print('json', request.json)
        print('form', request.form)
        return {"user": "getuser", "password": "123456"}

    def post(self, *args, **kwargs):
        print('args', request.args)
        print('json', request.json)
        print('form', request.form)
        return request.json

    def put(self):
        pass

    def delete(self):
        pass
