import time
import allure
import pytest
from tests.base_test.base_ui import BaseUi


@pytest.mark.Logic
@allure.feature('Тестирование логики')
class TestLogic(BaseUi):
    authorize = False
    api_authorize = True

    @allure.title('Поле access db')
    def test_check_access(self):
        """Тестирование логики поля access бд
        'Поле access проверяется на каждый запрос, если доступ запрещен - пользователь деавторизовывается'
        Ожидаемый результат: выбрасывает на страниу логина с ошибкой"""
        with allure.step('Открытие основной страницы'):
            self.registation_page.open()
        with allure.step('Регистрация пользователя'):
            user = self.registation_page.registration()
        with allure.step('Проверка поля access = 1'):
            assert self.db.get_table_test_users(username=user.username, password=user.password)[0].access == 1
        with allure.step('Изменение поля access = 0'):
            self.api.block_user(user.username)
        with allure.step('Проверка поля access = 0'):
            assert self.db.get_table_test_users(username=user.username, password=user.password)[0].access == 0
        with allure.step('Обновление страницы'):
            self.main_page.refresh()
        with allure.step('Проверка деавторизации пользователя'):
            self.login_page.check_error()

    @allure.title('Поле start_active_time db')
    def test_check_start_active_time(self):
        """Тестирование start_active_time
        Ождиание - поле start_active_time в бд проставляется после авторизации
        корректными данными"""
        with allure.step('Открытие основной страницы'):
            self.registation_page.open()
        with allure.step('Регистрация пользователя'):
            user = self.registation_page.registration()
        with allure.step('Выход'):
            self.main_page.log_out()
        with allure.step('Логин пользователя'):
            self.login_page.log_in(user.username, user.password)
            start_time = self.db.get_table_test_users(username=user.username, password=user.password)[0].start_active_time
        with allure.step('Проверка поля start_active_time после логина'):
            assert start_time is not None, f'start_active_time не проставился при логине'
        with allure.step('Выход'):
            self.main_page.log_out()
        with allure.step('Ожидание 10 секунд'):
            time.sleep(3)
        with allure.step('Логин пользователя'):
            self.login_page.log_in(user.username, user.password)
            end_time = self.db.get_table_test_users(username=user.username, password=user.password)[0].start_active_time
            assert end_time is not None, f'start_active_time не проставился при логине'
        with allure.step('Проверка изменения поля start_active_time при новом входе'):
            assert start_time != end_time, f'поле start_sctive_time не изменилось'

    @allure.title('Поле active db')
    def test_check_active(self):
        """Тестирование поля db Active
        Ожидаемый результат:Любой выход пользователя проставляет поле active в 0."""
        with allure.step('Открытие основной страницы'):
            self.registation_page.open()
        with allure.step('Регистрация пользователя'):
            user = self.registation_page.registration()
        with allure.step('Выход'):
            self.main_page.log_out()
        with allure.step('Логин пользователя'):
            self.login_page.log_in(user.username, user.password)
        with allure.step('Проверка поля после логина active'):
            assert self.db.get_table_test_users(username=user.username,
                                                password=user.password)[0].active == 1, \
                f'Пользовтель находится на странцие, но по данным бд не активен, active = 0'
        with allure.step('Выход'):
            self.main_page.log_out()
        with allure.step('Проверка поля после логаута active'):
            assert self.db.get_table_test_users(username=user.username,
                                                password=user.password)[0].active == 0, \
                f'Пользовтель не находится на странцие, но по данным бд активен, active = 1'

    @allure.title('Поле active db после блокировки')
    def test_check_active_after_block(self):
        """Тестирование поля db Active после блокировки
        Ожидаемый результат: поле active = 0."""
        with allure.step('Открытие основной страницы'):
            self.registation_page.open()
        with allure.step('Регистрация пользователя'):
            user = self.registation_page.registration()
        with allure.step('Выход'):
            self.main_page.log_out()
        with allure.step('Логин пользователя'):
            self.login_page.log_in(user.username, user.password)
        with allure.step('Проверка поля active = 1'):
            assert self.db.get_table_test_users(username=user.username,
                                                password=user.password)[0].active == 1, \
                f'Пользователь username f{user.username} после логина не имеет статус active'
        with allure.step('Изменение поля access = 0'):
            self.api.block_user(user.username)
        with allure.step('Обновление страницы'):
            self.main_page.refresh()
        with allure.step('Проверка деавторизации пользователя'):
            self.login_page.check_error()
        with allure.step('Проверка поля active = 0'):
            assert self.db.get_table_test_users(username=user.username,
                                                password=user.password)[0].active == 0, \
                f'Пользователь username f{user.username} после блокировки имеет статус active 0'
