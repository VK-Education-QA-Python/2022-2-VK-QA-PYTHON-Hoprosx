import os
import random

import allure
import pytest
from _pytest.fixtures import FixtureRequest

from api.api_client import ApiClient
from mysql.mysql_client import MysqlClient
from ui.pages.login_page import LoginPage
from ui.pages.main_page import MainPage
from ui.pages.registration_page import RegistrationPage
from configuration import BaseUser


class BaseUi:
    driver = None
    authorize = True
    api_authorize = None

    @pytest.fixture(scope='function', autouse=True)
    def setup(self, driver, config, logger, db, request: FixtureRequest):
        self.driver = driver
        self.config = config
        self.logger = logger
        self.db: MysqlClient = db
        self.login_page: LoginPage = (request.getfixturevalue('login_page'))
        self.registation_page: RegistrationPage = (request.getfixturevalue('registration_page'))
        self.main_page: MainPage = (request.getfixturevalue('main_page'))
        self.api: ApiClient = (request.getfixturevalue('api'))
        self.user = self.api.builder.user()
        self.username = self.api.builder.user().username
        self.password = self.api.builder.user().password

        if self.authorize:
            self.login_page.log_in(BaseUser.username, BaseUser.password)

        if self.api_authorize:
            self.api.post_login()

    @pytest.fixture(scope='function', autouse=True)
    def ui_report(self, driver, request, temp_dir):
        failed_test_count = request.session.testsfailed
        yield
        if request.session.testsfailed > failed_test_count:
            browser_logs = os.path.join(temp_dir, 'browser.log')
            with open(browser_logs, 'w') as f:
                for i in driver.get_log('browser'):
                    f.write(f"{i['level']} - {i['source']}\n{i['message']}\n")
            screenshot_path = os.path.join(temp_dir, 'failed.png')
            self.driver.save_screenshot(filename=screenshot_path)
            allure.attach.file(screenshot_path, 'failed.png', allure.attachment_type.PNG)
            with open(browser_logs, 'r') as f:
                allure.attach(f.read(), 'test.log', allure.attachment_type.TEXT)
