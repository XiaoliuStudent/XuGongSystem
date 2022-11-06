import time

from flask.views import MethodView
from flask import request
import datetime, os
import shutil


class CollectTable(MethodView):

    def __init__(self):
        self.db = None

    def get(self, **kwargs):
        self.db = kwargs.get("db")
        if 'CollectID' in request.args:
            CollectID = request.args.get('CollectID')
            sql_string = f"select * from xugong.CollectTable where CollectID='{CollectID}';"
        else:
            sql_string = f"select * from xugong.CollectTable;"
        collect_table = self.db.execute(sql_string)

        return {'status': 200, 'status_context': '查询成功', 'collect_table': collect_table}

    def post(self, *args, **kwargs):
        self.db = kwargs.get('db')
        self.post_type = request.json['PostType']

        if self.post_type == 'Update':
            if request.json['CollectStartTime'] != '':
                try:
                    CollectStartTime = datetime.datetime.strptime(request.json['CollectStartTime'],
                                                                  "%Y-%m-%dT%H:%M:%S.%fZ")
                except:
                    CollectStartTime = ''
            else:
                CollectStartTime = ''
            if request.json['CollectEndTime'] != '':
                try:
                    CollectEndTime = datetime.datetime.strptime(request.json['CollectEndTime'], "%Y-%m-%dT%H:%M:%S.%fZ")
                except:
                    CollectEndTime = ''
            else:
                CollectEndTime = ''

            # 主要操作
            sql_string = f"update xugong.CollectTable set CollectID={int(request.json['CollectID'])},CollectName='{request.json['CollectName']}',FileType='{request.json['FileType']}'," \
                         f"RenameStatus='{request.json['RenameStatus']}',RenameModels=\"{str(request.json['RenameModels'])}\",CollectStartTime='{CollectStartTime}',CollectEndTime='{CollectEndTime}' where CollectID={request.json['CollectID']};"
            sql_result = self.db.execute(sql_string)
            return {'status': 200, 'status_context': '签到表单修改成功'}

        elif self.post_type == 'Create':
            # 基础数据格式化
            if request.json['CollectStartTime'] != '':
                try:
                    CollectStartTime = datetime.datetime.strptime(request.json['CollectStartTime'],
                                                                  "%Y-%m-%dT%H:%M:%S.%fZ")
                except:
                    CollectStartTime = ''
            else:
                CollectStartTime = ''
            if request.json['CollectEndTime'] != '':
                try:
                    CollectEndTime = datetime.datetime.strptime(request.json['CollectEndTime'], "%Y-%m-%dT%H:%M:%S.%fZ")
                except:
                    CollectEndTime = ''
            else:
                CollectEndTime = ''

            # 主要操作
            # 创建SinginTable的数据记录
            sql_string = f"insert into xugong.CollectTable values({request.json['CollectID']},'{request.json['CollectName']}','{request.json['FileType']}','{request.json['RenameStatus']}',\"{str(request.json['RenameModels'])}\",'{CollectStartTime}','{CollectEndTime}');"
            self.db.execute(sql_string)

            # 创建SinginTableInfo的数据库
            # 插入数据的例子 insert into xugong.SinginTableinfo values( (SinginID,student['Name'],) )
            values = []
            for student in self.db.execute(f"select ID,Name from xugong.Students;"):
                values.append((int(request.json['CollectID']), request.json['CollectName'],
                               student['ID'], student['Name'], '未上传', '',''))

            # 拼接学生字段的字符串
            values = ','.join(str(i) for i in values)
            sql_string = f"insert into xugong.CollectTableInfo values{values}"
            self.db.execute(sql_string)

            # 保存文件初始化
            os.mkdir(f"./files/student_collectfiles/{request.json['CollectID']}")

            # 返回结果格式化
            CollectUrl = '/student/#/student/collectfile?collect_id=' + request.json['CollectID']
            return {'status': 200, 'status_context': '文件表单创建成功',
                    'CollectInfo': {'CollectUrl': CollectUrl}}

    def delete(self, **kwargs):
        CollectID = request.json['CollectID']
        self.db = kwargs.get('db')

        collect_delete = self.db.execute(f"delete from xugong.CollectTable where CollectID='{CollectID}';")
        collect_delete = self.db.execute(f"delete from xugong.CollectTableInfo where CollectID='{CollectID}';")


        # 删除保存文件
        shutil.rmtree(f"./files/student_collectfiles/{request.json['CollectID']}")
        return {'status': 200, 'status_context': '删除成功'}
