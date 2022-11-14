from base_sql_test import MyTest


class TestMysql(MyTest):

    def prepare(self):
        self.builder.create_all_tables()

    def test_table_counted_requests_by_type(self):
        table = self.get_counted_requests_by_type()
        assert len(table) == 4, f'Ожидаемая длина таблицы {5}, получили {len(table)}'
        expected_types = {'GET', 'POST', 'PUT', 'DELETE'}
        types = set()
        for row in table:
            types.add(row.type)
        assert types == expected_types, f'просочился запрос отличный от GET, POST, PUT, DELETE'

    def test_table_popular_reuests(self):
        table = self.get_popular_requests()
        assert len(table) == 10, f'Ожидаемая длина таблицы {10}, получили {len(table)}'
        assert table[0].amount > 20000, f'Самый популярный запрос не преодолел отметку в 20000'

    def test_table_counted_requests(self):
        table = self.get_counted_requests()
        assert len(table) == 1, f'Ожидаемая длина таблицы {1}, получили {len(table)}'

    def test_table_with_4xx_requests(self):
        table = self.get_4xx_requests()
        assert len(table) == 5, f'Ожидаемая длина таблицы {5}, получили {len(table)}'
        for row in table:
            if row.status_code // 400 == 1:
                assert True
            else:
                assert False, 'В таблицу попал запрос отличный от формата 4xx'

    def test_table_with_5xx_requests(self):
        table = self.get_5xx_requests()
        assert len(table) == 5, f'Ожидаемая длина таблицы {5}, получили {len(table)}'
