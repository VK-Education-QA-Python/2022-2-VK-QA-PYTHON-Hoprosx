import os
import random
import uuid

import allure
import pytest
from _pytest.fixtures import FixtureRequest
from mysql.mysql_client import MysqlClient
from api.api_client import ApiClient, ResponseStatusCodeException


class BaseApi():
    authorize = True

    @pytest.fixture(scope='function', autouse=True)
    def setup(self, request: FixtureRequest, db):
        self.db: MysqlClient = db
        self.api: ApiClient = (request.getfixturevalue('api'))
        self.username = self.api.builder.user().name
        self.password = self.api.builder.user().password

        if self.authorize:
            self.api.post_login()

    def create_user_api(self, name=None, surname=None, middle_name=None,
                        username=None, password=None, email=None):
        username = self.username if username is None else username
        try:
            self.api.add_user(name=name, surname=surname, middle_name=middle_name,
                              username=username, password=password, email=email)
        except ResponseStatusCodeException:
            pass
        return username
