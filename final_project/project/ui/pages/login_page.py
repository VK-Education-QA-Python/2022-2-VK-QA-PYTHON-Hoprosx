import allure

from ui.pages.base_page import BasePage
from ui.locators.locators import LoginPageLocators
from configuration import APP_URL


class LoginPage(BasePage):

    url = APP_URL + '/login'
    locators = LoginPageLocators()

    @allure.step('Логин')
    def log_in(self, username:str, password:str):
        self.element_is_visible(locator=self.locators.INPUT_USERNAME).send_keys(username)
        self.element_is_visible(locator=self.locators.INPUT_PASSWORD).send_keys(password)
        self.log_in_btn()

    @allure.step('переход на страницу регистрации')
    def go_to_registration(self):
        self.element_is_clickable(locator=self.locators.REGISTRATION_PAGE).click()

    @allure.step('проверка на валидность данных')
    def check_is_invalid(self):
        if self.element_is_visible(self.locators.INVALID_DATA_OR_UNAUTHORIZED):
            assert True
        else:
            return False

    @allure.step('кнопка "Войти"')
    def log_in_btn(self):
        self.element_is_clickable(locator=self.locators.SUBMIT_BTN).click()
    @allure.step('Проверка наличия всплывающей ошибки')
    def check_error(self):
        self.element_is_visible(self.locators.INVALID_DATA_OR_UNAUTHORIZED)