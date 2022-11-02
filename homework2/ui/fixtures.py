import os
import shutil
import sys

import allure
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from ui.pages.base_my_target import BaseMyTargetPage
from ui.pages.dashboard import DashboardPage
from ui.pages.segments import SegmentsPage


def pytest_configure(config):
    if sys.platform.startswith('win'):
        base_dir = 'C:\\tests'
    else:
        base_dir = '/tmp/tests'
    if not hasattr(config, 'workerunput'):
        if os.path.exists(base_dir):
            shutil.rmtree(base_dir)
        os.makedirs(base_dir)

    config.base_temp_dir = base_dir


@pytest.fixture()
def driver(config, temp_dir):
    browser = config['browser']
    url = config['url']
    selenoid = config['selenoid']
    vnc = config['vnc']
    options = Options()
    options.add_experimental_option("prefs", {"download.default_directory": temp_dir})
    if config['headless'] == True:
        options.add_argument("--headless")
    if selenoid:
        capabilities = {
            'browserName': 'chrome',
            'version': '106.0',
        }
        if vnc:
            capabilities['enableVNC'] = True
        driver = webdriver.Remote(
            'http://127.0.0.1:4444/wd/hub',
            options=options,
            desired_capabilities=capabilities
        )
    elif browser == 'chrome':
        driver = webdriver.Chrome(executable_path=ChromeDriverManager(version='105.0.5195.52').install(), options=options)
    else:
        raise RuntimeError(f'Unsupported browser: "{browser}"')
    driver.get(url)
    driver.set_window_size(1920, 1080)
    yield driver
    driver.quit()

@pytest.fixture()
@allure.step('Логин')
def log_in(driver, credentials):
    page = BaseMyTargetPage(driver)
    page.open()
    page.log_in(*credentials)
    return page


@pytest.fixture
def dashboard_page(driver):
    return DashboardPage(driver=driver)


@pytest.fixture
def segments_page(driver):
    return SegmentsPage(driver=driver)

@pytest.fixture()
def file_path_picture(repo_root):
    return os.path.join(repo_root, 'files', 'img.png')

@pytest.fixture()
def path_for_credentials(repo_root):
    return os.path.join(repo_root, 'files', 'userdata')

@pytest.fixture()
def credentials(path_for_credentials):
    with open(path_for_credentials, 'r') as f:
        user = f.readline().strip()
        password = f.readline().strip()

    return user, password