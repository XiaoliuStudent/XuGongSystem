from flask.views import MethodView
from flask import request
import datetime


class Singin(MethodView):
    def __init__(self):
        self.db = None

    # 获取签到状态
    def get(self, *args, **kwargs):
        # 基础数据配置
        # 参数获取，student_id 学号，sing_id 签到表id
        singin_id = request.args.get("SinginID")
        self.db = kwargs.get('db')
        print(singin_id)
        singin_details = self.db.execute(f"select * from xugong.SinginTableInfo where SinginID={singin_id}")

        singin_success_size = 0
        singin_error_size = 0
        for i in singin_details:
            if i['SinginStatus'] == '已签到':
                singin_success_size += 1
            else:
                singin_error_size += 1
        return {'status': 200, 'status_context': '签到列表查询成功', 'SinginDetails': {'students': singin_details,
                                                                               'singin_size_info': {
                                                                                   'singin_success_size': singin_success_size,
                                                                                   'singin_error_size': singin_error_size}}}

    # 发起签到
    def post(self, *args, **kwargs):
        # 基础数据配置
        if request.method == "POST":
            self.db = kwargs.get("db")
            # 参数获取，student_id 学号，sing_id 签到表id

            self.student_id = request.json['student_id']
            self.singin_id = request.json['singin_id']
            self.singin_time = datetime.datetime.now()

            # 执行签到
            sql_string = f"update xugong.SinginTableInfo set SinginTime='{self.singin_time}',SinginStatus='已签到' where SinginID={self.singin_id} and StudentID={self.student_id}"
            self.db.execute(sql_string)

            # 再次查询签到结果，并返回
            sql_string = f"select * from xugong.SinginTableInfo where SinginID={self.singin_id} and StudentID={self.student_id}"
            try:
                singin_result = self.db.execute(sql_string)[0]
            except:
                return {"status": 402, "status_context": "未查询到记录"}
            if singin_result['SinginStatus'] == "已签到":
                return {"status": 200, "status_context": "已签到", "singin_result": singin_result}
            else:
                return {"status": 401, "status_context": "未签到", "singin_result": singin_result}
