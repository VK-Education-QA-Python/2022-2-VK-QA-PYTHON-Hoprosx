from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, VARCHAR

Base = declarative_base()


class CountedRequestsModel(Base):
    __tablename__ = 'counted_requests'
    __table_arg__ = {'mysql_charset': 'utf8'}

    def __repr__(self):
        return f'counted_requests id={self.id}, amount={self.amount}'

    id = Column(Integer, primary_key=True, autoincrement=True)
    amount = Column(Integer, nullable=False)


class PopularRequestsModel(Base):
    __tablename__ = 'popular_requests'
    __table_arg__ = {'mysql_charset': 'utf8'}

    def __repr__(self):
        return f'popular_requests id={self.id}, url={self.url}, amount={self.amount}'

    id = Column(Integer, primary_key=True, autoincrement=True)
    url = Column(VARCHAR(300), nullable=False)
    amount = Column(Integer, nullable=False)


class CountedRequestsByTypeModel(Base):
    __tablename__ = 'counted_requests_by_type'
    __table_arg__ = {'mysql_charset': 'utf8'}

    def __repr__(self):
        return f'counted_requests_by_type id={self.id}, type={self.type}, amount={self.amount}'

    id = Column(Integer, primary_key=True, autoincrement=True)
    type = Column(VARCHAR(50), nullable=False)
    amount = Column(Integer, nullable=False)


class Big4XXRequestsModel(Base):
    __tablename__ = 'big_4XX_requests'
    __table_arg__ = {'mysql_charset': 'utf8'}

    def __repr__(self):
        return f'big_4XX_requests id={self.id}, ' \
               f'url={self.url}, ' \
               f'status_code={self.status_code}, ' \
               f'size={self.size}, ' \
               f'ip={self.ip}'

    id = Column(Integer, primary_key=True, autoincrement=True)
    url = Column(VARCHAR(300), nullable=None)
    status_code = Column(Integer, nullable=False)
    size = Column(Integer, nullable=False)
    ip = Column(VARCHAR(20), nullable=False)


class Users5XXRequestsModel(Base):
    __tablename__ = '5XX_requests'
    __table_arg__ = {'mysql_charset': 'utf8'}

    def __repr__(self):
        return f'5XX_requests id={self.id}, ' \
               f'ip={self.ip}, ' \
               f'amount={self.amount}'

    id = Column(Integer, primary_key=True, autoincrement=True)
    ip = Column(VARCHAR(20), nullable=False)
    amount = Column(Integer, nullable=False)
