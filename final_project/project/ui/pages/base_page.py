import time

import allure
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.wait import WebDriverWait as wait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains, ActionBuilder

class BasePage:

    url = None

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

    def element_is_visible(self, locator, timeout=5):
        return wait(self.driver, timeout).until(EC.visibility_of_element_located(locator))

    def elements_are_visible(self, locator, timeout=5):
        return wait(self.driver, timeout).until(EC.visibility_of_all_elements_located(locator))

    def element_is_present(self, locator, timeout=5):
        return wait(self.driver, timeout).until(EC.presence_of_element_located(locator))

    def element_are_present(self, locator, timeout=5):
        return wait(self.driver, timeout).until(EC.presence_of_all_elements_located(locator))

    def element_is_clickable(self, locator, timeout=4):
        return wait(self.driver, timeout).until(EC.element_to_be_clickable(locator))

    def go_to_element(self, element):
        self.driver.execute_script("arguments[0].scrollIntoView();", element)

    @allure.step('Переход на новое окно')
    def switch_page(self):
        body = self.element_is_present((By.TAG_NAME, 'body'))
        body.send_keys(Keys.CONTROL + 't')
        self.driver.switch_to.window(self.driver.window_handles[-1])
        return self.driver

    @allure.step('Переход к элементу после наведения курсора')
    def hover_and_click_nav_bar(self, ul, li):
        nav = self.element_is_visible(ul)
        ActionChains(self.driver).move_to_element(nav).perform()
        elem = self.element_is_clickable(li)
        ActionChains(self.driver).click(elem).perform()
        #другие варианты не работают -_-

    def get_attributes(self, elem) -> dict:
        dict = self.driver.execute_script(
            """
            let attr = arguments[0].attributes;
            let items = {}; 
            for (let i = 0; i < attr.length; i++) {
                items[attr[i].name] = attr[i].value;
            }
            return items;
            """,
            elem
        )
        return dict

    @allure.step('получение минимальной и максимальной длины инпута')
    def get_min_and_max_length(self, elem):
        dict = self.get_attributes(elem)
        return (int(dict.get('minlength')), int(dict.get('maxlength')))

    @allure.step('Проверка минимальной и максимальной длины инпута')
    def is_valid(self, data, input_field):
        elem = self.element_is_present((By.NAME, input_field))
        min, max = self.get_min_and_max_length(elem)
        print('Валидация от',min, 'до', max)
        if min <= len(data) <= max:
            return True
        else:
            return False


