from api.api_client import ResponseStatusCodeException

import allure
import pytest

from tests.base_test.base_ui import BaseUi
from configuration import BaseUser


@pytest.mark.Login
@allure.feature('Тесты формы авторизации')
class TestUi(BaseUi):
    authorize = False
    api_authorize = True

    @pytest.mark.parametrize('username, password, is_logined',
                             [(BaseUser.username, BaseUser.password, True),
                              (BaseUser.username.upper(), BaseUser.password, True),
                              (BaseUser.username, BaseUser.password.upper(), False),
                              ('incorrect', BaseUser.password, False),
                              (BaseUser.username, '245784qwc', False),
                              (' ' + BaseUser.username, BaseUser.password, False),
                              (BaseUser.username + ' ', BaseUser.password, False),
                              (BaseUser.username, BaseUser.password + ' ', False),
                              (BaseUser.username, ' ' + BaseUser.password, False),
                              ],
                             ids=['correct_data', 'CAPS username', 'CAPS password',
                                  'incorrect username', 'incorrect password',
                                  'login and space', 'space and login',
                                  'password and space', 'space and password'])
    @allure.title('Авторизация')
    def test_log_in(self, username, password, is_logined):
        """Тестирование формы логина с набором разных входных данных
        Ожидание результата: в случае валидных данных пользователь авторизируется и делает логаут,
        в случае неудачи проверяется всплывающее сообщение об ошибке"""

        with allure.step('Авторизация'):
            self.login_page.log_in(username, password)
        with allure.step('Проверка'):
            if is_logined:
                self.main_page.log_out()
            else:
                self.login_page.check_is_invalid()

    @pytest.mark.parametrize('username, password',
                             [('', BaseUser.password),
                              (BaseUser.username, '')],
                             ids=['empty username', 'empty password'])
    @allure.title('Авторизация с пустыми полями')
    def test_empty_filed(self, username, password):
        """Тестирование логина с пустыми полями"""
        self.login_page.log_in(username, password)
        self.login_page.go_to_registration()

    @allure.title('Авторизация после смены пароля')
    def test_log_in_after_change_password(self):
        """Тест авторизации после изменнения пароля через API
        Ожидаемы результат: корректный логин"""
        username = self.username
        with allure.step('Создания пользователя через API'):
            self.api.add_user(username=username)
        with allure.step('Смена пароля через API'):
            password = self.db.get_table_test_users(username=username)[0].password
            new_password = '21345678'
            self.api.change_password(username, new_password)
        with allure.step('Проверка в бд, что пароль изменился'):
            assert new_password != password, f'Пароль не изменился'
            assert new_password == self.db.get_table_test_users(username=username)[0].password
        with allure.step('Логин с новым паролем'):
            self.login_page.log_in(username, new_password)
        with allure.step('Логаут'):
            self.main_page.log_out()

    @allure.title('Авторизация после блокировки через API')
    def test_log_in_after_block(self):
        """Тест авторизации после блокировки пользователя через API
        Ожидаемы результат: пользователь не может авторизироваться"""
        username = self.username
        password = self.password
        with allure.step('Создания пользователя через API'):
            self.api.add_user(username=username, password=password)
        with allure.step(f'Проверка что у пользователя username: {username}'
                         f' access = 1'):
            assert self.db.get_table_test_users(username=username)[0].access == 1, \
                f'Пользователь заблокирован после создания через API'
        with allure.step('Блокировка юзера через API'):
            self.api.block_user(username=username)
        with allure.step(f'Проверка что у пользователя username: {username}'
                         f' access = 0'):
            assert self.db.get_table_test_users(username=username)[0].access == 0, \
                f'Пользователь не заблокирован после блокировки через API'
        with allure.step('Проверка, что пользовтеля не логинит'):
            self.login_page.log_in(username, password)
            self.login_page.check_is_invalid()
            self.api.unblock_user(username=username)
            self.login_page.log_in(username, password)
            self.main_page.log_out()
