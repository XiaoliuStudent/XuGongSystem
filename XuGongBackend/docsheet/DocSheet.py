import re
import requests
from flask.views import MethodView
from flask import request

class Students(MethodView):
    def __init__(self):
        self.db = None

    def get(self, **kwargs):
        self.db = kwargs.get('db')

        students = self.db.execute(r"select * from xugong.Students;")
        for i in students:
            i['IDCard'] = i['IDCard'][0:5] + "XXXXXXXX" + i['IDCard'][14:]
            i['Phone'] = i['Phone'][0:3] + "XXX" + i['Phone'][7:]
            i['QQID'] = i['QQID'][0:4] + "XXXXXXXX"
        return {'status':200, 'students':students}
