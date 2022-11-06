from flask.views import MethodView
from flask import request
import datetime


class SingIn(MethodView):
    def __init__(self):
        self.db = None

    def get(self, **kwargs):
        self.db = kwargs.get("db")
        if 'SinginID' in request.args:
            SinginID = request.args.get('SinginID')
            sql_string = f"select * from xugong.SinginTable where SinginID='{SinginID}';"
        else:
            sql_string = f"select * from xugong.SinginTable;"
        singin_tables = self.db.execute(sql_string)
        return {'status': 200, 'status_context': '查询成功', 'singin_tables': singin_tables}

    def post(self, **kwargs):
        self.db = kwargs.get('db')
        self.post_type = request.json['PostType']

        if self.post_type == 'Update':
            # ,SinginStartTime='{request.json['SinginStartTime']}',SinginEndTime='{request.json['SinginEndTime']}'
            if request.json['SinginStartTime'] != '':
                try:
                    SinginStartTime = datetime.datetime.strptime(request.json['SinginStartTime'], "%Y-%m-%dT%H:%M:%S.%fZ")
                except:
                    SinginStartTime = ''
            else:
                SinginStartTime = ''
            if request.json['SinginEndTime'] != '':
                try:
                    SinginEndTime = datetime.datetime.strptime(request.json['SinginEndTime'], "%Y-%m-%dT%H:%M:%S.%fZ")
                except:
                    SinginEndTime = ''
            else:
                SinginEndTime = ''
            # , SinginStartTime = '{SinginStartTime}', SinginEndTime = '{SinginEndTime}'
            sql_string = f"update xugong.SinginTable set SinginID={int(request.json['SinginID'])},SinginName='{request.json['SinginName']}',SinginType='{request.json['SinginType']}',SinginStartTime='{SinginStartTime}',SinginEndTime='{SinginEndTime}' where SinginID={request.json['SinginID']};"
            sql_result = self.db.execute(sql_string)
            return {'status': 200, 'status_context': '签到表单修改成功'}

        elif self.post_type == 'Create':
            # 基础数据格式化
            if request.json['SinginStartTime'] != '':
                try:
                    SinginStartTime = datetime.datetime.strptime(request.json['SinginStartTime'], "%Y-%m-%dT%H:%M:%S.%fZ")
                except:
                    SinginStartTime = ''
            else:
                SinginStartTime = ''
            if request.json['SinginEndTime'] != '':
                try:
                    SinginEndTime = datetime.datetime.strptime(request.json['SinginEndTime'], "%Y-%m-%dT%H:%M:%S.%fZ")
                except:
                    SinginEndTime = ''
            else:
                SinginEndTime = ''

            # 创建SinginTable的数据记录
            sql_string = f"insert into xugong.SinginTable values({request.json['SinginID']},'{request.json['SinginName']}','{request.json['SinginType']}','{SinginStartTime}','{SinginEndTime}');"
            self.db.execute(sql_string)

            # 创建SinginTableInfo的数据库
            # 插入数据的例子 insert into xugong.SinginTableinfo values( (SinginID,student['Name'],) )
            values = []
            for student in self.db.execute(f"select ID,Name from xugong.Students;"):
                values.append((int(request.json['SinginID']), request.json['SinginName'], request.json['SinginType'],
                               student['ID'], student['Name'], '未签到', ''))

            # 拼接学生字段的字符串
            values = ','.join(str(i) for i in values)
            sql_string = f"insert into xugong.SinginTableInfo values{values}"
            self.db.execute(sql_string)

            # 返回结果格式化
            SinginUrl = '/student/#/student/singin?singin_id=' + request.json['SinginID']
            return {'status': 200, 'status_context': '签到表单创建成功',
                    'SinginInfo': {'SinginUrl': SinginUrl}}

    def delete(self, **kwargs):
        SinginID = request.json['SinginID']
        self.db = kwargs.get('db')

        singin_delete = self.db.execute(f"delete from xugong.SinginTable where SinginID='{SinginID}';")
        singin_delete = self.db.execute(f"delete from xugong.SinginTableInfo where SinginID='{SinginID}';")
        return {'status': 200, 'status_context': '删除成功'}
