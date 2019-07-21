import os
from sqlalchemy import create_engine

basedir = os.path.abspath(os.path.dirname(__file__))


MYSQL = {"db_host": "100.127.2.24",
         "db_port": 3306,
         "db_name": "nbs_conf",
         "db_user": "haproxy",
         "db_pass": "haproxy",
         "db_connector": "pymysql"}


class Config(object):

    DEBUG = False
    SECRET_KEY = 'MY_SUPPER_SECRET Key'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MEDIA_PATH = '/media/conference'
    SQLALCHEMY_POOL_SIZE = 7
    SQLALCHEMY_POOL_RECYCLE = 599


class LocalConfig(Config):
    DEBUG = True
    DEVELOPMENT = True
    SQLALCHEMY_DATABASE_URI = "mysql+{db_connector}://{db_user}:{db_pass}@{db_host}:{db_port}/{db_name}".format(
        **MYSQL)
    # ENGINE = create_engine(os.environ['SQLALCHEMY_DATABASE_URI'])


# config_by_name = dict(loc=LocalConfig)
