import socket

globalConfig = {
    "dev": {
        "ServerConfig": {
            "listen_port": 8085,
            "mysql_host": "doisnot.com",
            "mysql_user": "root",
            "mysql_password": "177633@hangyu",
            "redis_host": "doisnot.com"
        },
        "XuGongConfig": {
            "class_name": "20计转本"
        }
    },
    "product": {
        "ServerConfig": {
            "listen_port": 8085,
            "mysql_host": "localhost",
            "mysql_user": "root",
            "mysql_password": "177633@hangyu",
            "redis_host": "localhost"
        },
        "XuGongConfig": {
            "class_name": "20计转本"
        }}
}


def get():
    hostname = socket.gethostname()
    if hostname == "MagicBook":
        return globalConfig['dev']
    elif hostname == "hyserver1":
        return globalConfig['product']


def set(config_key, config_value):
    pass

