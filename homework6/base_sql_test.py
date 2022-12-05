import pytest
from models.requests import *
from mysql.client import MysqlClient
from utils.builder import MysqlTableBuilder


class MyTest:


    @pytest.fixture(scope='function', autouse=True)
    def setup(self, mysql_client):
        self.client: MysqlClient = mysql_client
        self.builder: MysqlTableBuilder = MysqlTableBuilder(self.client)

    def get_table(self, model, **filters):
        """Получение значений из таблицы по модулю"""
        self.client.session.commit()
        return self.client.session.query(model).filter_by(**filters).all()
