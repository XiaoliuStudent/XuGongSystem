import pymysql
import pymysql.cursors
import redis
from config import GlobalConfig


# 定义一个数据库实例
class MySql():
    def __init__(self):
        self.connectdb = self.initConnect()

    # 初始化mysql数据库
    def initConnect(self):
        connectdb = pymysql.connect(host=GlobalConfig.get()["ServerConfig"]["mysql_host"], user='root',
                                    passwd='177633@hangyu',
                                    charset='utf8',
                                    cursorclass=pymysql.cursors.DictCursor)
        self.connectdb = connectdb
        return connectdb

    # 定义游标，并执行数据库sql语句的操作
    # sql_string sql语句
    def execute(self, sql_string):
        cursor = self.connectdb.cursor()
        try:
            cursor.execute(sql_string)
        except:
            self.initConnect()
            cursor.execute(sql_string)
        self.connectdb.commit()
        return cursor.fetchall()
        # result = []
        # for i in list(cursor.fetchall()):
        #     result.append(list(i))
        # return result


# 定义一个Redis实例
class Redis():
    def __init__(self):
        self.redis_object = self.initConnect()

    # 初始化Redis连接池，并设置redis链接对象
    def initConnect(self):
        return redis.StrictRedis(host=GlobalConfig.get()['ServerConfig']['redis_host'], port=6379,
                                 decode_responses=True)

    # 定义redis查询方法
    # param get_value 需要查询的键
    def get(self, get_key):
        return self.redis_object.get(get_key)

    # 定义redis设置方法，
    # set_key 需要设置的键
    # set_value 需要设置键的值
    def set(self, set_key, set_value):
        self.redis_object.set(set_key, set_value)
        return 0


# 定义MySql和Redis链接实例
class initDB():
    def __init__(self):
        self.mysql = MySql()
        self.redis = Redis()

    def sql_get(self, sql_string):
        return self.mysql.execute(sql_string)

    def set(self, sql_string):
        self.mysql.execute(sql_string)
