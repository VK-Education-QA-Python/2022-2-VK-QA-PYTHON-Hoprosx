import pytest
from mysql.client import MysqlClient


def pytest_configure(config):
    mysql_client = MysqlClient(user='root', password='pass', db_name='TEST_SQL')
    if not hasattr(config, 'workerinput'):
        mysql_client.create_db()
    mysql_client.connect(db_created=True)
    if not hasattr(config, 'workerinput'):
        mysql_client.create_all_schema()

    config.mysql_client = mysql_client

def pytest_unconfigure(config):
    if not hasattr(config, 'workerinput'):
        config.mysql_client.drop_all_tables()
    config.mysql_client.session.close()

@pytest.fixture(scope='session')
def mysql_client(request) -> MysqlClient:
    client = request.config.mysql_client
    yield client

