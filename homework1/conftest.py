import pytest
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from mytarget.mytarget import MyTarget

def pytest_addoption(parser):
    parser.addoption('--headless', action='store_true')


@pytest.fixture()
def config(request):
    headless = request.config.getoption('--headless')
    return {'headless': headless}


@pytest.fixture()
def driver(config):
    chrome_options = Options()
    if config['headless'] == True:
        chrome_options.add_argument("--headless")
    driver = webdriver.Chrome(ChromeDriverManager(version='105.0.5195.52').install(),options=chrome_options)
    driver.set_window_size(1920, 1080)
    yield driver
    driver.quit()

@pytest.fixture()
def log_in(driver):
    page = MyTarget(driver, 'https://target-sandbox.my.com/')
    page.open()
    page.log_in()
    return page