from api.api_client import ApiClient
from api.fixtures import *
import pytest


def pytest_addoption(parser):
    parser.addoption('--url', default='https://target-sandbox.my.com/')


@pytest.fixture(scope='session')
def repo_root():
    return os.path.abspath(os.path.join(__file__, os.path.pardir))


@pytest.fixture(scope='session')
def config(request):
    url = request.config.getoption('--url')
    return {
        'url': url,
    }


@pytest.fixture(scope='session')
def credentials(file_path_creds):
    with open(file_path_creds, 'r') as f:
        user = f.readline().strip()
        password = f.readline().strip()
    return user, password


@pytest.fixture(scope='session')
def api_client(credentials, config):
    return ApiClient(base_url=config['url'], email=credentials[0], password=credentials[1])
