from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, INTEGER, VARCHAR, SMALLINT, DATETIME, UniqueConstraint

Base = declarative_base()

class UsersModel(Base):
    __tablename__ = 'test_users'
    __table_arg__ = {'mysql_charset': 'utf8'}

    def __repr__(self):
        return f'test_users, id={self.id}, name={self.name}, ' \
               f'surname={self.surname}, middle_name={self.middle_name}, ' \
               f'username={self.username}, password={self.password}, ' \
               f'email={self.email}, access={self.access}, active={self.active}, ' \
               f'start_active_time={self.start_active_time}'

    id = Column(INTEGER, primary_key=True, autoincrement=True, nullable=False)
    name = Column(VARCHAR(255), nullable=False)
    surname = Column(VARCHAR(255), nullable=False)
    middle_name = Column(VARCHAR(255), nullable=True)
    username = Column(VARCHAR(16), nullable=True)
    password = Column(VARCHAR(255), nullable=False)
    email = Column(VARCHAR(64), nullable=False)
    access = Column(SMALLINT, nullable=True)
    active = Column(SMALLINT, nullable=True)
    start_active_time = Column(DATETIME, nullable=True)
    UniqueConstraint('email', name='email')
    UniqueConstraint('username', name='ix_test_users_username')
