import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

basedir = os.path.abspath(os.path.dirname(__file__))

# MYSQL = dict(db_host="100.127.2.24", db_port=3306, db_name="nbs_conf", db_user="haproxy", db_pass="haproxy", db_connector="pymysql")
MYSQL = dict(db_host="localhost", db_port=3306, db_name="nbs_conf", db_user="haproxy", db_pass="haproxy", db_connector="pymysql")

SQLALCHEMY_DATABASE_URI = "mysql+{db_connector}://{db_user}:{db_pass}@{db_host}:{db_port}/{db_name}".format(**MYSQL)

condb = create_engine(SQLALCHEMY_DATABASE_URI, echo=True)
Session = sessionmaker(bind=condb)
session = Session()
