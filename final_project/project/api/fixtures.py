import pytest
from api.api_client import ApiClient

@pytest.fixture(scope='session')
def api(config):
    return ApiClient(base_url=config['url'])