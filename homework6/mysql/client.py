import sqlalchemy
from sqlalchemy.orm import sessionmaker
from models.requests import Base


class MysqlClient:

    def __init__(self, db_name, user, password):
        self.user = user
        self.port = '3306'
        self.password = password
        self.host = '127.0.0.1'
        self.db_name = db_name

        self.connection = None
        self.engine = None
        self.session = None

    def connect(self, db_created=True):
        db = self.db_name if db_created else ''
        url = f'mysql+pymysql://{self.user}:{self.password}@{self.host}:{self.port}/{db}'
        self.engine = sqlalchemy.create_engine(url)
        self.connection = self.engine.connect()

        session = sessionmaker(bind=self.connection.engine)
        self.session = session()

    def create_db(self):
        self.connect(db_created=False)
        self.execute_query(f'DROP database IF EXISTS {self.db_name}')
        self.execute_query(f'CREATE database {self.db_name}')

    def create_table_counted_requests(self):
        if not sqlalchemy.inspect(self.engine).has_table('counted_requests'):
            Base.metadata.tables['counted_requests'].create(self.engine)

    def create_table_counted_requests_by_type(self):
        if not sqlalchemy.inspect(self.engine).has_table('counted_requests_by_type'):
            Base.metadata.tables['counted_requests_by_type'].create(self.engine)

    def create_table_popular_requests(self):
        if not sqlalchemy.inspect(self.engine).has_table('popular_requests'):
            Base.metadata.tables['popular_requests'].create(self.engine)

    def create_table_4xx_requests(self):
        if not sqlalchemy.inspect(self.engine).has_table('big_4XX_requests'):
            Base.metadata.tables['big_4XX_requests'].create(self.engine)

    def create_table_5xx_requests(self):
        if not sqlalchemy.inspect(self.engine).has_table('5XX_requests'):
            Base.metadata.tables['5XX_requests'].create(self.engine)

    def create_all_schema(self):
        self.create_table_counted_requests()
        self.create_table_counted_requests_by_type()
        self.create_table_popular_requests()
        self.create_table_4xx_requests()
        self.create_table_5xx_requests()

    def execute_query(self, query, fetch=False):
        res = self.connection.execute(query)
        if fetch:
            return res.fetchall()
