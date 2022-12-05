import sqlalchemy
from sqlalchemy.orm import sessionmaker
from models.requests import *

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

    def create_table(self, model):
        if not sqlalchemy.inspect(self.engine).has_table(model.__tablename__):
            Base.metadata.tables[model.__tablename__].create(self.engine)

    def drop_table(self, model):
        if sqlalchemy.inspect(self.engine).has_table(model.__tablename__):
            self.session.query(model).delete()
            self.session.commit()

    def create_all_schema(self):
        self.create_table(CountedRequestsModel)
        self.create_table(CountedRequestsByTypeModel)
        self.create_table(PopularRequestsModel)
        self.create_table(Big4XXRequestsModel)
        self.create_table(Users5XXRequestsModel)

    def drop_all_tables(self):
        self.drop_table(CountedRequestsModel)
        self.drop_table(CountedRequestsByTypeModel)
        self.drop_table(PopularRequestsModel)
        self.drop_table(Big4XXRequestsModel)
        self.drop_table(Users5XXRequestsModel)

    def execute_query(self, query, fetch=False):
        res = self.connection.execute(query)
        if fetch:
            return res.fetchall()
