import time
from selenium.webdriver.support.ui import WebDriverWait as wait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from locators.locators import Locators
from mytarget.constants import Consts

CLICK_RETRY = 3


class MyTarget:
    def __init__(self, driver, url):
        self.driver = driver
        self.url = url

    locators = Locators()

    def open(self):
        self.driver.get(self.url)

    def element_is_visible(self, locator, timeout=10):
        return wait(self.driver, timeout).until(EC.visibility_of_element_located(locator))

    def elements_are_visible(self, locator, timeout=10):
        return wait(self.driver, timeout).until(EC.visibility_of_all_elements_located(locator))

    def element_is_present(self, locator, timeout=10):
        return wait(self.driver, timeout).until(EC.presence_of_element_located(locator))

    def element_are_present(self, locator, timeout=10):
        return wait(self.driver, timeout).until(EC.presence_of_all_elements_located(locator))

    def element_is_clickable(self, locator, timeout=10):
        return wait(self.driver, timeout).until(EC.element_to_be_clickable(locator))

    def go_to_element(self, element):
        self.driver.execute_script("arguments[0].scrollIntoView();", element)

    def check_invalid_log_out_msg(self):
        elem = self.element_is_visible(self.locators.LOG_ERROR)
        return elem

    def log_in(self, email_or_phone: str = Consts.CORRECT_EMAIL, password: str = Consts.CORRECT_PASSWORD):
        self.email_or_phone = email_or_phone
        self.password = password

        self.element_is_clickable(self.locators.LOG_IN_BTN).click()
        self.element_is_visible(self.locators.LOG_EMAIL_INPUT).send_keys(self.email_or_phone)
        self.element_is_visible(self.locators.LOG_EMAIL_PASSWORD).send_keys(self.password)
        self.element_is_clickable(self.locators.LOG_IN_SUBMIT_BTN).click()

    def log_out(self):
        self.driver.set_window_size(1920, 1080)
        while self.driver.current_url == Consts.DASHBOARD_URL:
            try:
                self.element_is_clickable(self.locators.DASHBOARD_BALANCE).click()
                time.sleep(1)
                self.element_is_visible(self.locators.DASHBOARD_QUIT).click()
            except:
                pass

    def update_fio(self, fio='Иванов К.С.'):
        self.element_is_visible(self.locators.FIO).clear()
        self.element_is_visible(self.locators.FIO).send_keys(fio)
        self.element_is_clickable(self.locators.PROFILE_SUBMIT).click()
        return self.element_is_present(self.locators.DASHBOARD_USER_NAME).text

    def dashboard_navigate(self, dashboard_elem_name):
        self.driver.set_window_size(1920, 1080)
        self.element_is_clickable((By.CSS_SELECTOR, f'a[class*="center-module-{dashboard_elem_name}"]')).click()
