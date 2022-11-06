from flask.views import MethodView
from flask import request


class SingIn(MethodView):
    def __init__(self):
        self.db = None

    def get(self, **keyword):
        self.db = keyword.get("db")
        singin_tables = self.db.execute(r"select * from xugong.SinginTable;")
        return {'status': 200, 'status_context': '查询成功', 'singin_tables': singin_tables}

    def post(self):
        pass

    def delete(self):
        pass
