import time

import pytest

from mytarget.mytarget import MyTarget
from mytarget.constants import Consts


@pytest.mark.UI
class TestUi:

    def test_log_in_positive(self, driver):
        """Тест на логин c корректными данными"""
        page = MyTarget(driver, Consts.BASIC_URL)
        page.open()
        elem_after_log_in = page.log_in()
        assert elem_after_log_in != None, f"LOGIN FAILED"

    def test_log_out(self, log_in):
        """Тест на лог аут"""
        page = log_in
        enter_btn = page.log_out()
        assert enter_btn != None, f"LOGOUT FAILED"

    def test_log_in_email_without_at(self, driver):
        """Негативный тест на авторизацию (email без @)"""
        EMAIL = 'kirillrespgmail.com'
        page = MyTarget(driver, Consts.BASIC_URL)
        page.open()
        error = page.log_in_negative(email_or_phone=EMAIL)
        assert error == True, f"FAILED LOGIN with email:{EMAIL}, password {Consts.CORRECT_PASSWORD}"

    def test_log_in_email_with_incorrect_pass(self, driver):
        """Негативный тест на авторизацию c неверным паролем"""
        password = '1'
        page = MyTarget(driver, Consts.BASIC_URL)
        page.open()
        error = page.log_in_negative(password=password)
        assert error == True, f"FAILED LOGIN with email:{Consts.CORRECT_EMAIL}, password {password}"

    def test_change_contact_info(self, log_in, data='Кирилл'):
        """Тест на редактирование поля ФИО в профиле"""
        page = log_in
        result = page.update_fio(data)
        assert result.lower() == data.lower(), f"New input data: {data.lower()}, but actual data: {result.lower()}"

    @pytest.mark.parametrize(
        'dashboard_elem',
        ['profile', 'statistics'],
        ids=['profile', 'statistics']
    )
    def test_dashboard_navigation(self, dashboard_elem, driver, log_in):
        """Тест на переход на страницы портала через кнопки Статистика/Профиль/ в шапке меню.
        Каждый из этих тестов переходит по выбранным меню и проверяет текущий url"""
        page = log_in
        page.dashboard_navigate(dashboard_elem)
        assert dashboard_elem in driver.current_url, f"current dashboard_elem:{dashboard_elem}, current url: {driver.current_url}"
