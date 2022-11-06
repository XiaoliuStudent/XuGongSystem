from flask.views import MethodView
from flask import request, redirect,url_for
import os, shutil


class MangeFile(MethodView):
    def __init__(self):
        self.db = None

    def get(self, *args, **kwargs):
        CollectID = request.args['CollectID']
        os.system(
            f"cd ./files/student_collectfiles/{CollectID}/; zip {CollectID}.zip *")
        return redirect(f"/files/student_collectfiles/{CollectID}/{CollectID}.zip")

    def post(self, *args, **kwargs):
        return request.json

    def put(self):
        pass

    def delete(self, **kwargs):
        self.db = kwargs.get('db')
        CollectID = request.json['CollectID']
        shutil.rmtree(f"./files/student_collectfiles/{CollectID}")
        os.mkdir(f"./files/student_collectfiles/{CollectID}")
        sql_string = f"update xugong.CollectTableInfo set UploadStatus='未上传',UploadFileNames='',UploadTime='';"
        self.db.execute(sql_string)

        return {'status': 200, 'status_context': '所有文件删除成功'}
