import os
from contextlib import contextmanager
import allure
import pytest
from _pytest.fixtures import FixtureRequest
from ui.pages.base_my_target import BaseMyTargetPage
from ui.pages.dashboard import DashboardPage
from ui.pages.segments import SegmentsPage


class BaseCase:
    driver = None

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

    @pytest.fixture(scope='function', autouse=True)
    def setup(self, driver, config, logger, request: FixtureRequest):
        self.driver = driver
        self.config = config
        self.logger = logger
        self.dashboard_page: DashboardPage = (request.getfixturevalue('dashboard_page'))
        self.segments_page: SegmentsPage = (request.getfixturevalue('segments_page'))