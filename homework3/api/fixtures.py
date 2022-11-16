import os
import pytest


@pytest.fixture(scope='session')
def file_path_creds(repo_root):
    return os.path.join(repo_root, 'files', 'userdata')


