import allure
import pytest
from api.src.builder.user import Builder
from base_test.base_ui import BaseUi
from configuration import BaseUser


@pytest.mark.Registration
@allure.feature('Тесты регистрации')
class TestRegistration(BaseUi):
    """Класс содержащий тесты с регистрацией"""

    authorize = False

    @pytest.mark.parametrize('name, exp',
                             [('', False),
                              (BaseUser.name, True),
                              ('13213', False),
                              ('a', True),
                              ('a' * 45, True),
                              ('a' * 46, False),
                              ('#$%&‘*+—/=?^_`{|}~', False),
                              ('.', False),
                              ('    ', False)],
                             ids=['empty', 'existing db name', 'numbers', 'one letter',
                                  '45 letters', '46 letters', 'symbols', 'dot', 'spaces'])
    @allure.title('Валидация поля name')
    def test_name(self, name, exp):
        """Проверка поля name при регистрации через ui
        Ожидаемый результат: успешная регистрация или ошибка в зависимости от входных данных"""
        username = self.username
        with allure.step('Открытие страницы регистрации'):
            self.registation_page.open()
        with allure.step('Проверка валидации со стороны ui'):
            validation = self.registation_page.is_valid(name, 'name')
        with allure.step('Регистрация с валидными данными и тестируемым полем name'):
            self.registation_page.registration(username=username, name=name)
        with allure.step('Проверка базы и валидаци'):
            if exp:
                assert len(self.db.get_table_test_users(username=username, name=name)) > 0, \
                    f"Пользователь с name: {name} и username: {username} не был добавлен в бд"
                assert validation, f'Валидация не пройдена, но пользователь добавлен в бд'
                self.main_page.log_out()
            else:
                assert len(self.db.get_table_test_users(username=username, email=name)) == 0, \
                    f"Пользователь с name: {name} и username: {username} был добавлен в бд"
                self.registation_page.confirm_reg()

    @pytest.mark.parametrize('surname, exp',
                             [('', False),
                              (BaseUser.surname, True),
                              ('13213', False),
                              ('a', True),
                              ('a' * 300, True),
                              ('a' * 301, False),
                              ('#$%&‘*+—/=?^_`{|}~', False),
                              ('.', False),
                              ('     ', False)],
                             ids=['empty', 'existing db surname', 'numbers', 'one letter',
                                  '300 letters', '301 letters', 'symbols', 'dot', 'spaces'])
    @allure.title('Валидация поля surname')
    def test_surname(self, surname, exp):
        """Проверка поля surname при регистрации через ui
        Ожидаемый результат: успешная регистрация или ошибка в зависимости от входных данных"""
        username = self.username
        with allure.step('Открытие страницы регистрации'):
            self.registation_page.open()
        with allure.step('Проверка валидации со стороны ui'):
            validation = self.registation_page.is_valid(surname, 'surname')
        with allure.step('Регистрация с валидными данными и тестируемым полем email'):
            self.registation_page.registration(username=username, surname=surname)
        with allure.step('Проверка базы и валидаци'):
            if exp:
                assert len(self.db.get_table_test_users(username=username, surname=surname)) > 0, \
                    f"Пользователь с surname: {surname} и username: {username} не был добавлен в бд"
                assert validation, f'Валидация не пройдена, но пользователь добавлен в бд'
                self.main_page.log_out()
            else:
                assert len(self.db.get_table_test_users(username=username, surname=surname)) == 0, \
                    f"Пользователь с surname: {surname} и username: {username} был добавлен в бд"
                self.registation_page.confirm_reg()

    @pytest.mark.parametrize('middlename, exp',
                             [('', True),
                              (BaseUser.middle_name, True),
                              ('13213', False),
                              ('a', True),
                              ('a' * 500, False),
                              ('#$%&‘*+—/=?^_`{|}~', False),
                              ('.', False),
                              ('     ', False)],
                             ids=['empty', 'existing db middlename', 'numbers', 'one letter',
                                  '500 letters', 'symbols', 'dot', 'spaces'])
    @allure.title('Валидация поля middlename')
    def test_middlename(self, middlename, exp):
        """Проверка поля middlename при регистрации через ui
        Ожидаемый результат: успешная регистрация или ошибка в зависимости от входных данных"""
        username = self.username
        with allure.step('Открытие страницы регистрации'):
            self.registation_page.open()
        with allure.step('Регистрация с валидными данными и тестируемым полем middlename'):
            self.registation_page.registration(username=username, middlename=middlename)
        with allure.step('Проверка базы и валидаци'):
            if exp:
                assert len(self.db.get_table_test_users(username=username)) > 0, \
                    f"Пользователь с middlename: {middlename} и username: {username} не был добавлен в бд"
                self.main_page.log_out()
            else:
                assert len(self.db.get_table_test_users(username=username)) == 0, \
                    f"Пользователь с middlename: {middlename} и username: {username} был добавлен в бд"
                self.registation_page.confirm_reg()

    @pytest.mark.parametrize('username, exp',
                             [(BaseUser.username, False),
                              ('', False),
                              ('l', False),
                              ('Misha', False),
                              ('Valera', True),
                              ('A' * 17, False),
                              ('     ', False),
                              (' Leonid', False),
                              ('Leonid ', False),
                              ('#$%&‘*+—/=?^_`{|}~', False),
                              ('', False),
                              ],
                             ids=['existing', 'empty', '1 letter', '5 letters', '6 letters',
                                  '17 letters', 'spaces', 'space in start', 'space in end',
                                  'symbols', 'numbers'])
    @allure.title('Валидация поля username')
    def test_username(self, username, exp):
        """Проверка поля username при регистрации через ui
        Ожидаемый результат: успешная регистрация или ошибка в зависимости от входных данных"""
        password = self.password
        with allure.step('Открытие страницы регистрации'):
            self.registation_page.open()
        with allure.step('Проверка валидации со стороны ui'):
            validation = self.registation_page.is_valid(username, 'username')
        with allure.step('Регистрация с валидными данными и тестируемым полем email'):
            print(username)
            self.registation_page.registration(username=username, password=password)
        with allure.step('Проверка базы и валидаци'):
            if exp:
                self.main_page.log_out()
                assert len(self.db.get_table_test_users(username=username)) > 0, \
                    f"Пользователь с username: {username} не был добавлен в бд"
                assert validation, f'Валидация не пройдена, но пользователь добавлен в бд'
            else:
                self.registation_page.confirm_reg()
                assert len(self.db.get_table_test_users(username=username)) == 0, \
                    f"Пользователь с username: {username} был добавлен в бд"

    @pytest.mark.parametrize('email, exp',
                             [(Builder.user().email, True),
                              (Builder.user().email.replace('@', ''), False),
                              (Builder.user().email.replace('.', ''), False),
                              (Builder.user().email[0:5], False),
                              (Builder.user().name[0:1] + '@a.ru', True),
                              ('b' * 56 + '@mail.ru', True),
                              ('b' * 57 + '@mail.ru', False),
                              ('#$%&‘*+—/=?^_`{|}~@mail.ru', False),
                              (('ab' + Builder.user().email).replace('b', '.'), True),
                              (('abc' + Builder.user().email).replace('bc', '..'), False),
                              (('abc' + Builder.user().email).replace('a', '.'), False),
                              (BaseUser.email, False),
                              ],
                             ids=['valid_email', 'without @', 'without .', '5 len', '6 len',
                                  '64 len', '65len', 'symbols', 'with another dot', 'with two dot',
                                  'with first dot', 'current db email'])
    @allure.title('Валидация поля email')
    def test_email(self, email, exp):
        """Проверка поля email при регистрации через ui
        Ожидаемый результат: успешная регистрация или ошибка в зависимости от входных данных"""
        username = self.username
        with allure.step('Открытие страницы регистрации'):
            self.registation_page.open()
        with allure.step('Проверка валидации со стороны ui'):
            validation = self.registation_page.is_valid(email, 'email')
        with allure.step('Регистрация с валидными данными и тестируемым полем email'):
            self.registation_page.registration(username=username, email=email)
        with allure.step('Проверка базы и валидаци'):
            if exp:
                assert len(self.db.get_table_test_users(username=username, email=email)) > 0, \
                    f"Пользователь с email: {email} и username: {username} не был добавлен в бд"
                assert validation, f'Валидация не пройдена, но пользователь добавлен в бд'
                self.main_page.log_out()
            else:
                assert len(self.db.get_table_test_users(username=username, email=email)) == 0, \
                    f"Пользователь с email: {email} и username: {username} был добавлен в бд"
                self.registation_page.confirm_reg()

    @pytest.mark.parametrize('password, exp',
                             [('', False),
                              ('    ', False),
                              ('a' * 500, False),
                              ('.', False),
                              (' w', False),
                              ('w ', False),
                              ('#$%&‘*+—/=?^_`{|}~', False)],
                             ids=['empty', 'spaces', '500 letters', 'dot', 'space in start',
                                  'space in end', 'symbols'])
    @allure.title('Валидация поля password')
    def test_password(self, password, exp):
        """Проверка поля password при регистрации через ui
        Ожидаемый результат: успешная регистрация или ошибка в зависимости от входных данных"""
        username = self.username
        with allure.step('Открытие страницы регистрации'):
            self.registation_page.open()
        with allure.step('Регистрация с валидными данными и тестируемым полем email'):
            self.registation_page.registration(username=username, password=password)
        with allure.step('Проверка базы и валидаци'):
            if exp:
                assert len(self.db.get_table_test_users(username=username, password=password)) > 0, \
                    f"Пользователь с password: {password} и username: {username} не был добавлен в бд"
                self.main_page.log_out()
            else:
                assert len(self.db.get_table_test_users(username=username, password=password)) == 0, \
                    f"Пользователь с password: {password} и username: {username} был добавлен в бд"
                self.registation_page.confirm_reg()

    @allure.title('Чекбокс SDET')
    def test_reg_without_sdet(self):
        """Регистрация без чекбокса
        Ожидаемый результат: пользователь не зарегестрирован и остается на странице регистрации"""
        with allure.step('Открытие страницы регистрации'):
            self.registation_page.open()
        with allure.step('Регистрация с валидными данными без чекбокса SDET'):
            self.registation_page.registration(sdet=False)
        with allure.step('Проверка'):
            self.registation_page.confirm_reg()

    @allure.title('Подтверждение пароля некорректным паролем')
    def test_reg_with_different_passwords(self):
        """Регистрация с некорректным подтверждением ввода пароля
        Ожидаемый результат: пользователь не зарегестрирован и остается на странице регистрации"""
        with allure.step('Открытие страницы регистрации'):
            self.registation_page.open()
        with allure.step('Регистрация с некорректным подтверждением ввода пароля'):
            self.registation_page.registration(password='245245pol', confirm_pass='234we24d')
        with allure.step('Проверка'):
            self.registation_page.confirm_reg()
