import re
import requests
from flask.views import MethodView
from flask import request
from .flushData import flushData


class HistoryDoc(MethodView):
    def __init__(self):
        pass

    def get(self, *args, **kwargs):
        redis = kwargs.get("redis")
        return {"history_doc_url": redis.get("history_doc_url"), "history_doc_title": redis.get("history_doc_title")}


# 定义核酸检测类
class UserList(MethodView):
    def __init__(self):
        self.db = None

    def get(self, *args, **kwargs):
        # 数据库初始化
        self.redis = kwargs.get("redis")

        # 获取腾讯文档的URL和文档ID

        class_name = request.args.get('class_name')
        doc_url = request.args.get('doc_url')
        doc_id = re.findall(r'sheet/.*', doc_url)[0][6:6 + 17]
        doc_url = f"https://docs.qq.com/sheet/{doc_id}"
        # 通过URL和ID请求腾讯文档
        res = requests.get(
            f"https://docs.qq.com/dop-api/opendoc?noEscape=1&id={doc_id}&normal=1&outformat=1&startrow=0&endrow=400&wb=1&nowb=0",
            headers={
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36',
                'Referer': f'https://docs.qq.com/sheet/{doc_id}'})
        # open("HeSuan/doc_res.json", 'wb').write(res.content)

        # 根据请求文档返回的数据进行数据清洗
        flush_data = flushData(res_context=res.content, doc_url=doc_url, class_name=class_name)
        if flush_data['status'] == 200:
            # 部分历史初始化
            self.redis.set("history_doc_url", doc_url)
            self.redis.set("history_doc_title", str(flush_data['doc_title']))
            return flush_data


class SendMail(MethodView):
    def __init__(self):
        self.db = None

    def post(self, **kwargs):
        # 数据库初始化
        self.db = kwargs.get("db")

        # 获取发送邮件对象的列表并转换成元组
        object_list = list(request.json['objects'])
        object_list.append(20090102139)
        object_list.append(00000000000)
        object_tuple = tuple(object_list)

        sql_query = f"select Mail from xugong.Students where ID in {object_tuple};"
        # 用学号通过数据库拿到邮箱地址，将邮箱地址转换成功list，

        mail_list = []
        for i in self.db.execute(sql_query):
            mail_list.append(i['Mail'])

        # 将需要发送邮件列表的邮件地址发送到推送系统API之中
        hesuan_data = {'title': '核酸检测提醒', 'context': "请及时完成核酸并填好在线表格", 'objects': mail_list}
        res = requests.post("http://api.doisnot.com/message/mail", json=hesuan_data)
        return_data = res.json()
        return return_data
