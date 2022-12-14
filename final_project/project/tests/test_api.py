import allure
import pytest

from api.src.builder.user import Builder
from configuration import BaseUser
from tests.base_test.base_api import BaseApi
from api.base.response import Response
from api.api_client import ResponseStatusCodeException


@pytest.mark.API
@allure.feature('Api тесты')
class TestApi(BaseApi):
    authorize = True

    @allure.title('Добавление юзера с корректными данными')
    def test_add_valid_user(self):
        """Добавление юзера с валидными данными
        Ожидаемый результат: юзер добавлен в бд, статус код 201"""
        username = self.username
        with allure.step(f'Создание юзера через API'):
            Response(self.api.add_user(username=username)).assert_status_code(201)
        with allure.step(f'Проверка что пользователь добавлен в бд'):
            assert len(self.db.get_table_test_users(username=username)) == 1, \
                f'Пользователь с username: {username} не был добавлен в бд'
            assert False, f'Неверный статус код, пользовтелен добавлен в бд'

    @allure.title('Добавление юзера с некоректными данными')
    def test_add_non_valid_user(self):
        """Добавление юзера с невалидными данными
        Ожидаемый результат: юзер добавлен в бд, статус код 400"""
        username = 'usernameusernameusername'
        with allure.step(f'Создание юзера через API'):
            Response(self.api.add_user(username=username)).assert_status_code(400)

    @allure.title('Добавление юзера с корректными данными без middlename API')
    def test_add_valid_user_without_middle_name(self):
        """Добавление юзера с валидными данными без поля middle_name
        Ожидаемый результат: юзер добавлен в бд, статус код 201"""
        username = self.username
        with allure.step(f'Создание юзера через API'):
            try:
                Response(self.api.add_user(middle_name='', username=username)).assert_status_code(201)
            except ResponseStatusCodeException:
                with allure.step(f'Проверка что пользователь добавлен в бд'):
                    assert len(self.db.get_table_test_users(username=username)) == 1, \
                        f'Пользователь с username: {username} не был добавлен в бд'
                    assert False, f'Неверный статус код, пользовтелен добавлен в бд'

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
    @allure.title('Валидация поля name API')
    def test_validation_name_user(self, name, exp):
        """Тест валидации поля name
        Ожидаемый результат: exp True - добавление  бд, False юзер не добавляется в бд"""
        username = self.username
        with allure.step(f'Создание юзера через API c name: {name}'):
            self.create_user_api(name=name, username=username)
        with allure.step(f'Проверка юзера в дб, name: {name}'):
            if exp:
                assert len(self.db.get_table_test_users(name=name, username=username)) == 1, \
                    f"Ошибка валидации, пользователь не добавлен в бд, name: {name}, username: {username}"
            else:
                assert len(self.db.get_table_test_users(name=name, username=username)) == 0, \
                    f"Ошибка валидации, пользователь был добавлен в бд, name: {name}, username: {username}"

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
    @allure.title('Валидация поля surname API')
    def test_validation_surname_user(self, surname, exp):
        """Тест валидации поля surname
        Ожидаемый результат: exp True - добавление  бд, False юзер не добавляется в бд"""
        username = self.username
        with allure.step(f'Создание юзера через API c surname: {surname}'):
            self.create_user_api(surname=surname, username=username)
        with allure.step(f'Проверка юзера в дб, surname: {surname}'):
            if exp:
                assert len(self.db.get_table_test_users(surname=surname, username=username)) == 1, \
                    f"Ошибка валидации, пользователь не добавлен в бд, surname: {surname}, username: {username}"
            else:
                assert len(self.db.get_table_test_users(surname=surname, username=username)) == 0, \
                    f"Ошибка валидации, пользователь был добавлен в бд, surname: {surname}, username: {username}"

    @pytest.mark.parametrize('middle_name, exp',
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
    @allure.title('Валидация поля middlename API')
    def test_validation_middle_name_user(self, middle_name, exp):
        """Тест валидации поля middle name
        Ожидаемый результат: exp True - добавление  бд, False юзер не добавляется в бд"""
        username = self.username
        with allure.step(f'Создание юзера через API c middle_name: {middle_name}'):
            self.create_user_api(middle_name=middle_name, username=username)
        with allure.step(f'Проверка юзера в дб, middle_name: {middle_name}'):
            if exp:
                assert len(self.db.get_table_test_users(middle_name=middle_name,
                                                        username=username)) == 1, \
                    f"Ошибка валидации, пользователь не добавлен в бд, " \
                    f"middle_name: {middle_name}, username: {username}"
            else:
                assert len(self.db.get_table_test_users(middle_name=middle_name,
                                                        username=username)) == 0, \
                    f"Ошибка валидации, пользователь был добавлен в бд, " \
                    f"middle_name: {middle_name}, username: {username}"

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
    @allure.title('Валидация поля username API')
    def test_validation_username_user(self, username, exp):
        """Тест валидации поля username
        Ожидаемый результат: exp True - добавление  бд, False юзер не добавляется в бд"""
        password = self.password
        with allure.step(f'Создание юзера через API c username: {username}'):
            self.create_user_api(username=username, password=password)
        with allure.step(f'Проверка юзера в дб, username: {username}'):
            if exp:
                assert len(self.db.get_table_test_users(username=username,
                                                        password=password)) == 1, \
                    f"Ошибка валидации, пользователь не добавлен в бд, " \
                    f"username: {username}"
            else:
                assert len(self.db.get_table_test_users(username=username,
                                                        password=password)) == 0, \
                    f"Ошибка валидации, пользователь был добавлен в бд, " \
                    f"username: {username}"

    @pytest.mark.parametrize('password, exp',
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
    @allure.title('Валидация поля password API')
    def test_validation_password_user(self, password, exp):
        """Тест валидации поля password
        Ожидаемый результат: exp True - добавление  бд, False юзер не добавляется в бд"""
        username = self.username
        with allure.step(f'Создание юзера через API c password: {password}'):
            self.create_user_api(middle_name=password, username=username)
        with allure.step(f'Проверка юзера в дб, password: {password}'):
            if exp:
                assert len(self.db.get_table_test_users(password=password,
                                                        username=username)) == 1, \
                    f"Ошибка валидации, пользователь не добавлен в бд, " \
                    f"password: {password}, username: {username}"
            else:
                assert len(self.db.get_table_test_users(password=password,
                                                        username=username)) == 0, \
                    f"Ошибка валидации, пользователь был добавлен в бд, " \
                    f"password: {password}, username: {username}"

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
    @allure.title('Валидация поля email API')
    def test_validation_email_user(self, email, exp):
        """Тест валидации поля email
        Ожидаемый результат: exp True - добавление  бд, False юзер не добавляется в бд"""
        username = self.username
        with allure.step(f'Создание юзера через API c email: {email}'):
            self.create_user_api(email=email, username=username)
        with allure.step(f'Проверка юзера в дб, email: {email}'):
            if exp:
                assert len(self.db.get_table_test_users(email=email,
                                                        username=username)) == 1, \
                    f"Ошибка валидации, пользователь не добавлен в бд, " \
                    f"email: {email}, username: {username}"
            else:
                assert len(self.db.get_table_test_users(email=email,
                                                        username=username)) == 0, \
                    f"Ошибка валидации, пользователь был добавлен в бд, " \
                    f"email: {email}, username: {username}"

    @allure.title('Удаление юзера API')
    def test_remove_existing_user(self):
        """Тест удаления сещуствующего юзера
        Ожидаемый результат: узер удален из бд, статус код 204"""
        with allure.step(f'Создание юзера через API'):
            username = self.create_user_api()
        with allure.step(f'Удаление юзера через API'):
            Response(self.api.delete_user(username=username)).assert_status_code(204)
        with allure.step(f'Проверка юзера в бд'):
            assert len(self.db.get_table_test_users(username=username)) == 0, \
                f'Пользователь с username: {username} не удален из бд'

    @allure.title('Удаление несуществующего юзера API')
    def test_delete_not_existing_user(self):
        """Тест удаления несещуствующего юзера
        Ожидаемый результат: статус код 404"""
        username = self.username
        with allure.step(f'Удаление юзера через API'):
            Response(self.api.delete_user(username)).assert_status_code(404)

    @allure.title('Смена пароля API')
    def test_change_password(self):
        """Тест смены пароля
        Ожидаемый результат: пароль изменен"""
        password = self.password
        with allure.step(f'Создание юзера через API'):
            username = self.create_user_api()
        with allure.step(f'Смена пароля через API'):
            try:
                Response(self.api.change_password(username=username, password=password)) \
                    .assert_status_code(200)
            except AssertionError:
                assert self.db.get_table_test_users(username=username)[0].password == password
                assert False

    @allure.title('Смена пароля несуществующего пользователя API')
    def test_change_password_user_not_exist(self):
        """Тест изменения пароля несуществующего юзера
        Ожидаемый результат: статус код 404"""
        password = self.password
        username = self.username
        with allure.step(f'Смена пароля через API'):
            Response(self.api.change_password(username=username, password=password)) \
                .assert_status_code(404)

    @allure.title('Смена пароля на идентичный API')
    def test_change_password_for_equal(self):
        """Тест изменение пароля на текущий
        Ожидаемый результат: статсус код 400"""
        password = self.password
        with allure.step(f'Создание юзера через API'):
            username = self.create_user_api(password=password)
        with allure.step(f'Смена пароля через API'):
            Response(self.api.change_password(username=username, password=password)) \
                .assert_status_code(400)  # 304?

    @allure.title('Блокировка юзера API')
    def test_block_users(self):
        """Тест удаления блокировки существующего юзера
        Ожидаемый результат: юзер заблокирован, access = 0"""
        with allure.step(f'Создание юзера через API'):
            username = self.create_user_api()
        with allure.step(f'Проверка на то, что пользователь активен'):
            assert self.db.get_table_test_users(username=username)[0].access == 1, \
                f'Пользователь {username} не активен'
        with allure.step(f'Блокировка пользователя API'):
            Response(self.api.block_user(username=username)) \
                .assert_status_code(200)
        with allure.step(f'Проверка на то, что пользователь заблокирован'):
            assert self.db.get_table_test_users(username=username)[0].access == 0, \
                f'Пользователь {username} активен'

    @allure.title('Блокировка несуществующего юзера API')
    def test_block_not_existing_users(self):
        """Тест удаления блокировки сущеcnвующего юзера
        Ожидаемый результат: статус код 404"""
        username = self.username
        with allure.step(f'Блокировка пользователя API'):
            Response(self.api.block_user(username=username)) \
                .assert_status_code(404)

    @allure.title('Разблокировка юзера API')
    def test_unblock_user(self):
        """Тест разблокировки юзера
        Ожидаемый результат: юзер разблокирован, статус код 200"""
        with allure.step(f'Создание юзера через API'):
            username = self.create_user_api()
        with allure.step(f'Блокировка юзера через API'):
            Response(self.api.block_user(username=username)) \
                .assert_status_code(200)
        with allure.step(f'Проверка на то, что пользователь не активен'):
            assert self.db.get_table_test_users(username=username)[0].access == 0, \
                f'Пользователь {username} активен'
        with allure.step(f'Разблокировка юзера через API'):
            Response(self.api.unblock_user(username=username)) \
                .assert_status_code(200)
        with allure.step(f'Проверка на то, что пользователь активен'):
            assert self.db.get_table_test_users(username=username)[0].access == 1, \
                f'Пользователь {username} не активен'

    @allure.title('Разблокировка несуществующего юзера API')
    def test_unblock_not_existing_user(self):
        """Тест разблокировки не существующего юзера
        Ожидаемый результат: статус код 404"""
        username = self.username
        with allure.step(f'Разблокировка несуществующего юзера через API'):
            Response(self.api.unblock_user(username=username)) \
                .assert_status_code(404)

    @allure.title('Получение статуса запущенного приложения API')
    def test_status(self):
        """Тест статус работающего приложения
        Ожидаемый результат: статсус код 200"""
        with allure.step(f'Запрос статуса юзера через API'):
            Response(self.api.status()).assert_status_code(200)

    @allure.title('Разблокировка активного пользователя API')
    def test_activate_activated_user(self):
        """Тест разблокировки активного юзера
        Ожидаемый результат: статус код 400"""
        with allure.step(f'Создание юзера через API'):
            username = self.create_user_api()
        with allure.step(f'Разблокировка юзера через API'):
            Response(self.api.unblock_user(username=username)) \
                .assert_status_code(400)

    @allure.title('Блок блокированного пользователя API')
    def test_block_blocked_user(self):
        """Тест блокировки заблокированного юзера
        Ожидаемый результат: статус код 400"""
        with allure.step(f'Создание юзера через API'):
            username = self.create_user_api()
        with allure.step(f'Разблокирование юзера через API'):
            Response(self.api.block_user(username=username)) \
                .assert_status_code(200)
        with allure.step(f'Разблокирование юзера через API'):
            Response(self.api.block_user(username=username)) \
                .assert_status_code(400)
