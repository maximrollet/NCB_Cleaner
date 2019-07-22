import os

basedir = os.path.abspath(os.path.dirname(__file__))


class LocalConfig(object):
    MYSQL = {"db_host": "100.127.2.24",
             "db_port": 3306,
             "db_name": "nbs_conf",
             "db_user": "haproxy",
             "db_pass": "haproxy",
             "db_connector": "pymysql"}
    DEBUG = True
    DEVELOPMENT = True
    SQLALCHEMY_DATABASE_URI = "mysql+{db_connector}://{db_user}:{db_pass}@{db_host}:{db_port}/{db_name}".format(**MYSQL)

