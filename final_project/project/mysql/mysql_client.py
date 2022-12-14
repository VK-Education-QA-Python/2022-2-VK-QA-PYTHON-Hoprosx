import allure
import sqlalchemy
from sqlalchemy.orm import sessionmaker
from mysql.models.test_users import Base
from mysql.models.test_users import UsersModel
from configuration import BaseUser

class MysqlClient:

    def __init__(self):
        self.user = 'root'
        self.port = '3306'
        self.password = 'password'
        self.host = '127.0.0.1'
        self.db_name = 'vkeducation'

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

    def set_up(self):
        self.connect()
        self.create_table_test_users()
        self.add_user()

    def create_db(self):
        self.connect(db_created=False)
        self.execute_query(f'DROP database IF EXISTS {self.db_name}')
        self.execute_query(f'CREATE database {self.db_name}')

    def drop_db(self):
        self.execute_query(f'DROP database IF EXISTS {self.db_name}')

    def create_table_test_users(self):
        if not sqlalchemy.inspect(self.engine).has_table('test_users'):
            Base.metadata.tables['test_users'].create(self.engine)

    def get_table(self, model, **filters):
        """Получение значений из таблицы по модулю"""
        self.session.commit()
        return self.session.query(model).filter_by(**filters).all()

    @allure.step('запрос таблицы test_user')
    def get_table_test_users(self, **filters):
        """Получение значений из таблицы test_users"""
        return self.get_table(UsersModel, **filters)

    def execute_query(self, query, fetch=False):
        res = self.connection.execute(query)
        if fetch:
            return res.fetchall()

    def add_user(self):
        self.execute_query(f"""insert into `test_users` 
        (`name`, `surname`, `middle_name`, `username`, `password`, `email`)
        values ("{BaseUser.name}", "{BaseUser.surname}", "{BaseUser.middle_name}",
         "{BaseUser.username}", "{BaseUser.password}", "{BaseUser.email}")""")
