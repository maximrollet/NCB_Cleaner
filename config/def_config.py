"""
Created on Sat Jul 27 17:57:39 2019
@author: maximrollet
"""
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

basedir = os.path.abspath(os.path.dirname(__file__))

# MYSQL = dict(db_host="100.127.2.24", db_port=3306, db_name="nbs_conf", db_user="haproxy", db_pass="haproxy", db_connector="pymysql")
MYSQL = {'db_host': "192.168.1.7", 'db_port': 3306, 'db_name': "nbs_conf", 'db_user': "haproxy", 'db_pass': "haproxy",
         'db_connector': "pymysql"}

SQLALCHEMY_DATABASE_URI = "mysql+{db_connector}://{db_user}:{db_pass}@{db_host}:{db_port}/{db_name}".format(**MYSQL)

condb = create_engine(SQLALCHEMY_DATABASE_URI, echo=False)
Session = sessionmaker(bind=condb)
session = Session()

LOGGER = {'version': 1,
          'formatters': {
              'default': {'format': '%(asctime)s - %(levelname)s - %(message)s', 'datefmt': '%Y-%m-%d %H:%M:%S'},
              'with_line': {'format': '%(asctime)s %(filename)s:%(lineno)s; %(levelname)s: %(message)s',
                            'datefmt': '%Y-%m-%d %H:%M:%S'}
          },
          'handlers': {
              'console': {
                  'level': 'DEBUG',
                  'class': 'logging.StreamHandler',
                  'formatter': 'default',
                  'stream': 'ext://sys.stdout'
              },
              'file': {
                  'level': 'DEBUG',
                  'class': 'logging.FileHandler',
                  'formatter': 'with_line',
                  # 'filename': 'logs/ncb_app.log',
                  # 'filename': '/var/log/modCleaner/ConRoomCleaner,log.log',
                  'filename': '/home/maxim/WORK/PYTHON-SANDBOX/classes.log',
                  'encoding': 'utf8'
              }
          },
          'loggers': {
              '': {
                  'level': 'DEBUG',  # Top level of logging configuration
                  'handlers': ['console', 'file']
              }
          },
          'disable_existing_loggers': False
          }
