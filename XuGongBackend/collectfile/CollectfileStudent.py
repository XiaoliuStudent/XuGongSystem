import datetime
import os
import time

from flask.views import MethodView
from flask import request


class UploadFile(MethodView):

    def __init__(self):
        self.db = None
        self.student_key_value = {'学号': 'ID', '班级': 'Class', '姓名': 'Name', '身份证号': 'IDCard', '手机号码': 'Phone',
                                  '宿舍': 'Dorm', '两位学号': '', '_': '_', '-': '-'}

    def get(self, **kwargs):
        # 基础数据配置
        # 参数获取，student_id 学号，sing_id 签到表id
        collect_id = request.args.get("CollectID")
        self.db = kwargs.get('db')
        collect_details = self.db.execute(f"select * from xugong.CollectTableInfo where CollectID={collect_id}")

        collect_success_size = 0
        collect_error_size = 0
        for i in collect_details:
            if i['UploadStatus'] == '已上传':
                collect_success_size += 1
            else:
                collect_error_size += 1
        return {'status': 200, 'status_context': '签到列表查询成功', 'CollectDetails': {'students': collect_details,
                                                                                'collect_size_info': {
                                                                                    'collect_success_size': collect_success_size,
                                                                                    'collect_error_size': collect_error_size}}}

    def post(self, *args, **kwargs):
        # 基础信息配置
        self.db = kwargs.get('db')
        student_id = request.headers.get('student_id')
        collect_id = request.headers.get('collect_id')

        # 配置信息获取
        sql_string = f"select * from xugong.CollectTable where CollectID={collect_id}"
        table_config = self.db.execute(sql_string)[0]

        # 文件保存设置
        collect_file = request.files.get("file")
        if table_config['RenameStatus'] == 'False':
            collect_file_name = collect_file.filename
        else:
            # 文件基础信息
            filename_format = []
            collect_file_name = collect_file.filename
            collect_file_type = '.' + collect_file.filename.split('.')[-1]

            # 学生基础信息
            sql_string = f"select * from xugong.Students where ID={student_id}"
            student_config = self.db.execute(sql_string)[0]
            for model in eval(table_config['RenameModels']):
                if model in self.student_key_value:
                    if model == '两位学号':
                        filename_format.append(str(student_config['ID'])[-2:])
                    else:
                        filename_format.append(str(student_config[self.student_key_value[model]]))
                else:
                    filename_format.append(model)

            collect_file_name = ''.join(filename_format) + collect_file_type
        collect_file.save(f"./files/student_collectfiles/{collect_id}/{collect_file_name}")
        collect_file.close()

        # 数据库更新设置
        upload_time = datetime.datetime.now()
        sql_string = f"update xugong.CollectTableInfo set UploadStatus='已上传',UploadFileNames='{collect_file_name}',UploadTime='{upload_time}' where CollectID={collect_id} and StudentID={student_id};"
        self.db.execute(sql_string)
        return {"status": "success", "status_context": "文件上传成功"}

    def delete(self, **kwargs):
        self.db = kwargs.get('db')
        CollectID = request.json['CollectID']
        file_name = request.json['file_name']
        StudentID = request.json['StudentID']
        os.remove(f"./files/student_collectfiles/{CollectID}/{file_name}")
        sql_string = f"update xugong.CollectTableInfo set UploadStatus='未上传',UploadFileNames='',UploadTime='' where CollectID={CollectID} and StudentID={StudentID};"
        self.db.execute(sql_string)
        return {"status": 200, "status_context": "文件删除成功"}
