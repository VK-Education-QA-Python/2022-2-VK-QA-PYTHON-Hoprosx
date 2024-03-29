import time

import allure
from selenium.webdriver.remote.webelement import WebElement
from ui.locators import locators
from selenium.webdriver.support.wait import WebDriverWait as wait
from selenium.webdriver.support import expected_conditions as EC


class PageNotOpenedExeption(Exception):
    pass


class BaseMyTargetPage:
    locators = locators.BaseLanding()
    url = 'https://target-sandbox.my.com'

    def __init__(self, driver):
        self.driver = driver

    def open(self):
        self.driver.get(self.url)

    @allure.step('Обновление страницы')
    def refresh(self):
        self.driver.get(self.url)

    @allure.step('Смена страницы')
    def change_page(self, url):
        self.driver.get(url)

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

    def log_in(self, email_or_phone=False, password=False):
        """Что бы логин можно было использовать в негативных кейсах"""
        self.element_is_clickable(self.locators.LOG_IN_BTN).click()
        self.element_is_visible(self.locators.LOG_EMAIL_INPUT).send_keys(email_or_phone)
        self.element_is_visible(self.locators.LOG_EMAIL_PASSWORD).send_keys(password)
        self.element_is_clickable(self.locators.LOG_IN_SUBMIT_BTN).click()
