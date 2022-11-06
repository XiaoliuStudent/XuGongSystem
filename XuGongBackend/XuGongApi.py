import json
import flask
from flask_cors import CORS

# 创建程序入口
app = flask.Flask('XuGongApi')
app.debug = True
cors = CORS(app, resources={r"/*": {"origins": "*"}})

# 初始化数据库池和redis连接池
from database import DataBase

db = DataBase.MySql()
redis = DataBase.Redis()

# 读取配置文件
from config import GlobalConfig

globalConfig = GlobalConfig.get()
baseConfig = {}
defaultsdata = {"db": db, "redis": redis, "globalConfig": globalConfig, "baseConfig": baseConfig}

# 添加路由规则
"""
    针对核酸检测页面提供关于api
"""
from hesuan import HeSuanApi

app.add_url_rule("/api/hesuan/historydoc", methods=['GET'],
                 view_func=HeSuanApi.HistoryDoc.as_view("/api/hesuan/historydoc"), defaults=defaultsdata)
app.add_url_rule("/api/hesuan/userlist", methods=['GET'], view_func=HeSuanApi.UserList.as_view("/api/hesuan/userlist"),
                 defaults=defaultsdata)
app.add_url_rule("/api/hesuan/sendmail", methods=['POST'], defaults=defaultsdata,
                 view_func=HeSuanApi.SendMail.as_view("/api/hesuan/sendmail"))

"""
    针对测试通过测试相关的api
"""
from testapi import TestApi1

app.add_url_rule("/api/testapi", methods=['GET', 'POST', 'PUT', 'DELETE'],
                 view_func=TestApi1.TestApi1.as_view("/api/testapi"), defaults=defaultsdata)

"""
    针对签到提供相关的api
"""
from singin import SingInStudent
from singin import SinginTable
# 针对管理员后台提供api支持
app.add_url_rule("/api/singin/singintable", methods=['GET', "POST","DELETE"],
                 view_func=SinginTable.SingIn.as_view("/api/singin/singintable"),
                 defaults=defaultsdata)
# 针对学生提供api支持
app.add_url_rule("/api/singin/student/singin", methods=['GET', "POST"],
                 view_func=SingInStudent.Singin.as_view("/api/singin/student/singin"),
                 defaults=defaultsdata)

"""
    针对文件收集提供相关的api
"""
from collectfile import CollectfileStudent
# 针对管理员后台提供api支持
from collectfile import CollectTable
app.add_url_rule("/api/collectfile/collecttable", methods=['GET', 'POST', 'PUT', 'DELETE'],
                 view_func=CollectTable.CollectTable.as_view("/api/collectfile/collecttable"), defaults=defaultsdata)
from collectfile import MangeFile
app.add_url_rule("/api/collectfile/managefile", methods=['GET', 'POST', 'PUT', 'DELETE'],
                 view_func=MangeFile.MangeFile.as_view("/api/collectfile/managefile"), defaults=defaultsdata)
# 针对学生端提供api支持
app.add_url_rule("/api/collectfile/uploadfile", methods=['GET', 'POST', 'PUT', 'DELETE'],
                 view_func=CollectfileStudent.UploadFile.as_view("/api/collectfile/uploadfile"), defaults=defaultsdata)

"""
    针对电子表格提供相关的api
"""
from docsheet import DocSheet

app.add_url_rule("/api/docsheet/students", methods=['GET'],
                 view_func=DocSheet.Students.as_view("/api/docsheet/getusers"), defaults=defaultsdata)

"""
    针对文字检索提供相关的api
"""
from wordsearch import WordSearch
app.add_url_rule("/api/wordsearch/wordsearch", methods=['POST'],
                 view_func=WordSearch.WordSearch.as_view("/api/wordsearch/wordsearch"), defaults=defaultsdata)
"""
    针对Readme说明提供相关的api
"""
from other import Readme
app.add_url_rule("/api/readme", methods=['GET'],
                 view_func=Readme.Readme.as_view("/api/readme"))

if __name__ == '__main__':
    # 运行实例
    app.run(host='0.0.0.0', port=globalConfig['ServerConfig']['listen_port'], debug=True)
