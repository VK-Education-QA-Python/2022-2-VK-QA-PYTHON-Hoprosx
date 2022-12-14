import pymysql
from pymysql.cursors import DictCursor


class MysqlClient:

    def __init__(self, db_name, user, password):
        self.user = user
        self.port = 3306
        self.password = password
        self.host = 'mysql'
        self.db_name = db_name
        self.connection = None

    def connect(self):
        self.connection = pymysql.connect(host=self.host,
                                          port=self.port,
                                          user=self.user,
                                          password=self.password,
                                          db=self.db_name,
                                          charset='utf8',
                                          autocommit=True,
                                          cursorclass=pymysql.cursors.DictCursor
                                          )
