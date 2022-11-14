from files.analyze_scripts import *


class MysqlTableBuilder:
    """Методы для заполенения таблиц на основании скриптов"""

    def __init__(self, client):
        self.client = client

    def create_counted_requests(self):
        """Заполнение таблицы counted_requests"""
        result_file_path = count_all_requests()
        with open(result_file_path, 'r') as file:
            data = file.read()
            data = json.loads(data)

        self.client.execute_query(f'insert into `counted_requests` (`amount`) values ("{data["AMOUNT"]}")')

    def create_counted_requests_by_type(self):
        """Заполнение таблицы counted_requests_by_type"""
        result_file_path = types_of_requests()
        with open(result_file_path, 'r') as file:
            data = file.read()
            data = json.loads(data)

        for row in data.items():
            self.client.execute_query(f"""insert into `counted_requests_by_type` (`type`, `amount`)
             values ("{row[0]}", "{row[1]}")""")

    def create_popular_requests(self):
        """Заполнение таблицы popular_requests"""
        result_file_path = top_ten_popular_requests()
        with open(result_file_path, 'r') as file:
            data = file.read()
            data = json.loads(data)

        for row in data.values():
            self.client.execute_query(f"""insert into `popular_requests` (`url`, `amount`)
             values ("{row['url']}", "{row['amount']}")""")

    def create_4xx_requests(self):
        """Заполнение таблицы big_4XX_requests"""
        result_file_path = top_five_big_requests_with_4xx_status_code()
        with open(result_file_path, 'r') as file:
            data = file.read()
            data = json.loads(data)

        for row in data.values():
            self.client.execute_query(f"""insert into `big_4XX_requests` (`url`, `status_code`, `size`, `ip` )
             values ("{row['url'].split('?')[0]}", "{row['code']}", "{row['size']}", "{row['ip']}")""")

    def create_5xx_requests(self):
        """Заполнение таблицы 5XX_requests"""
        result_file_path = top_five_users_with_5xx_status_code_requests()
        with open(result_file_path, 'r') as file:
            data = file.read()
            data = json.loads(data)

        for row in data.values():
            self.client.execute_query(f"""insert into `5XX_requests` (`ip`, `amount`)
             values ("{row['ip']}", "{row['amount']}")""")

    def create_all_tables(self):
        """Заполняет все таблицы класса Builder"""
        self.create_counted_requests()
        self.create_counted_requests_by_type()
        self.create_popular_requests()
        self.create_4xx_requests()
        self.create_5xx_requests()
