from base_sql_test import MyTest
from models.requests import *

class TestMysql(MyTest):

    def test_table_counted_requests_by_type(self):
        self.builder.create_counted_requests_by_type()
        table = self.get_table(CountedRequestsByTypeModel)
        assert len(table) == 4, f'Ожидаемая длина таблицы {5}, получили {len(table)}'
        expected_types = {'GET', 'POST', 'PUT', 'DELETE'}
        types = set()
        for row in table:
            types.add(row.type)
        assert types == expected_types, f'просочился запрос отличный от GET, POST, PUT, DELETE'

    def test_table_popular_requests(self):
        self.builder.create_popular_requests()
        table = self.get_table(PopularRequestsModel)
        assert len(table) == 10, f'Ожидаемая длина таблицы {10}, получили {len(table)}'
        assert table[0].amount > 20000, f'Самый популярный запрос не преодолел отметку в 20000'

    def test_table_counted_requests(self):
        self.builder.create_counted_requests()
        table = self.get_table(CountedRequestsModel)
        assert len(table) == 1, f'Ожидаемая длина таблицы {1}, получили {len(table)}'

    def test_table_with_4xx_requests(self):
        self.builder.create_4xx_requests()
        table = self.get_table(Big4XXRequestsModel)
        assert len(table) == 5, f'Ожидаемая длина таблицы {5}, получили {len(table)}'
        for row in table:
            if row.status_code // 400 == 1:
                assert True
            else:
                assert False, 'В таблицу попал запрос отличный от формата 4xx'

    def test_table_with_5xx_requests(self):
        self.builder.create_5xx_requests()
        table = self.get_table(Users5XXRequestsModel)
        assert len(table) == 5, f'Ожидаемая длина таблицы {5}, получили {len(table)}'
