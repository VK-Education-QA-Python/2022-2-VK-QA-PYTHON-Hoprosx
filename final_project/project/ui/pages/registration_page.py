import allure
import pytest

from api.src.builder.user import Builder
from ui.pages.base_page import BasePage
from ui.locators.locators import RegistrationPageLocators
from configuration import APP_URL


class RegistrationPage(BasePage):
    url = APP_URL + '/reg'

    locators = RegistrationPageLocators()

    @allure.step('регистрация')
    def registration(self,
                     name: str=None,
                     surname: str=None,
                     middlename: str=None,
                     username: str=None,
                     email: str=None,
                     password: str=None,
                     confirm_pass: str=None,
                     sdet: bool=True):

        user = Builder.user(name=name, surname=surname, middle_name=middlename,
                            username=username,
                            email=email, password=password)
        self.element_is_clickable(locator=self.locators.INPUT_NAME).send_keys(user.name)
        self.element_is_clickable(locator=self.locators.INPUT_SURNAME).send_keys(user.surname)
        self.element_is_clickable(locator=self.locators.INPUT_MIDDLE_NAME).send_keys(user.middle_name)
        if username is not None:
            self.element_is_clickable(locator=self.locators.INPUT_USERNAME).send_keys(username)
        else:
            self.element_is_clickable(locator=self.locators.INPUT_USERNAME).send_keys(user.username)
        self.element_is_clickable(locator=self.locators.INPUT_EMAIL).send_keys(user.email)
        self.element_is_clickable(locator=self.locators.INPUT_PASSWORD).send_keys(user.password)
        if confirm_pass is None:
            self.element_is_clickable(locator=self.locators.INPUT_CONFIRM_PASS).send_keys(user.password)
        else:
            self.element_is_clickable(locator=self.locators.INPUT_CONFIRM_PASS).send_keys(confirm_pass)
        if sdet:
            self.sdet_checkbox()
        else:
            pass
        self.confirm_reg()
        return user

    @allure.step('переход на страницу логина')
    def log_in_page(self):
        self.element_is_clickable(self.locators.LOG_IN_PAGE).click()

    @allure.step('SDET чекбокс')
    def sdet_checkbox(self):
        self.element_is_clickable(locator=self.locators.SDET_CHECKBOX).click()

    @allure.step('подтвердить регистрацию')
    def confirm_reg(self):
        self.element_is_clickable(locator=self.locators.SUBMIT_BTN).click()
