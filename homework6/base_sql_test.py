import pytest
from models.requests import *
from mysql.client import MysqlClient
from utils.builder import MysqlTableBuilder


class MyTest:

    def prepare(self):
        pass

    @pytest.fixture(scope='function', autouse=True)
    def setup(self, mysql_client):
        self.client: MysqlClient = mysql_client
        self.builder: MysqlTableBuilder = MysqlTableBuilder(self.client)
        self.prepare()

    def get_counted_requests(self, **filters):
        """Получение значений из таблицы counted_requests"""
        self.client.session.commit()
        return self.client.session.query(CountedRequestsModel).filter_by(**filters).all()

    def get_counted_requests_by_type(self, **filters):
        """Получение значений из таблицы counted_requests_by_type"""
        self.client.session.commit()
        return self.client.session.query(CountedRequestsByTypeModel).filter_by(**filters).all()

    def get_popular_requests(self, **filters):
        """Получение значений из таблицы popular_requests"""
        self.client.session.commit()
        return self.client.session.query(PopularRequestsModel).filter_by(**filters).all()

    def get_4xx_requests(self, **filters):
        """Получение значений из таблицы counted_requests"""
        self.client.session.commit()
        return self.client.session.query(Big4XXRequestsModel).filter_by(**filters).all()

    def get_5xx_requests(self, **filters):
        """Получение значений из таблицы 5XX_requests"""
        self.client.session.commit()
        return self.client.session.query(Users5XXRequestsModel).filter_by(**filters).all()
