import re
import requests
from flask.views import MethodView
from flask import request

class WordSearch(MethodView):
    def __init__(self):
        self.db = None

    def post(self, **kwargs):
        self.db = kwargs.get('db')

        if request.json['type'] == 'textarea':
            textarea = request.json['textarea']
        elif request.json['type'] == 'files':
            textarea = ''.join(request.json['files'])
        sql_string = f"select ID,Name from xugong.Students;"
        students = self.db.execute(sql_string)



        # 算计计算
        for student in students:
            if str(student['ID']) in textarea or student['Name'] in textarea:
                student['SearchStatus'] = "True"
            else:
                student['SearchStatus'] = 'False'
        return {"status":200, "status_context":"检索成功","search_result":students}