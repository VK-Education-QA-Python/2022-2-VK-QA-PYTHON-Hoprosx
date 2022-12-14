import allure
import pytest
from tests.base_test.base_ui import BaseUi


@pytest.mark.UI
@allure.feature('Ui тесты: страница логина')
class TestLoginPageUi(BaseUi):
    authorize = False

    @allure.title('Переход со страницы авторизации на страницу регистрации')
    def test_switch_from_log_in_page_to_registration_page(self):
        """Тест перехода со страницы авторизации на страницу регистрации
        Ожидаемый результат: текущий url = url страницы регистрации"""
        with allure.step('Открытие основной страницы'):
            self.login_page.open()
        with allure.step('Переход на страницу регистрации'):
            self.login_page.go_to_registration()
        with allure.step('Проверка текущего url'):
            assert self.driver.current_url == self.registation_page.url, \
                f'Переход на страницу регистрации не осуществлен'


@pytest.mark.UI
@allure.feature('Ui тесты: страница регистрации')
class TestRegistrationPageUi(BaseUi):
    authorize = False

    @allure.title('Переход со страницы регистрации на страницу авторизации')
    def test_switch_from_registration_page_to_log_in_page(self):
        """Тест перехода со страницы регистрации на страницу авторизации
        Ожидаемый результат: текущий url = url страницы авторизации"""
        with allure.step('Открытие основной страницы'):
            self.registation_page.open()
        with allure.step('Переход на страницу авторизации'):
            self.registation_page.log_in_page()
        with allure.step('Проверка текущего url'):
            self.login_page.log_in_btn(), \
            f'Переход на страницу авторизации не осуществлен'


@pytest.mark.UI
@allure.feature('Ui тесты: основная страница')
class TestMainPageUi(BaseUi):
    authorize = True

    @allure.title('Тест кнопки Logout')
    def test_log_out_btn(self):
        """Тест кнопки лог аут
        Ожидаемый результат: пользователь находится на странице логина"""
        with allure.step('Открытие основной страницы'):
            self.main_page.open()
        with allure.step('Логаут'):
            self.main_page.log_out()
        with allure.step('Проверка'):
            assert self.driver.current_url == self.login_page.url, \
                f'Пользователь не разлогинился'

    @allure.title('Тест релевантности контента основной страницы: Api')
    def test_main_content_api(self):
        """Тест релевантности контента основной страницы: Api
        Ожидаемый результат: страница релевантна"""
        with allure.step('Переход по ссылке: Api'):
            self.main_page.content_api()
        with allure.step('Проверка релевантности контента'):
            title = self.main_page.switch_page().title.lower()
            assert 'api' in title, f'Контент нерелевантен заявленной теме Api'

    @allure.title('Тест релевантности контента основной страницы: Internet')
    def test_main_content_internet(self):
        """Тест релевантности контента основной страницы: Internet
        Ожидаемый результат: страница релевантна"""
        with allure.step('Переход по ссылке: Api'):
            self.main_page.content_internet()
        with allure.step('Проверка релевантности контента'):
            title = self.main_page.switch_page().title.lower()
            assert 'internet' in title, f'Контент нерелевантен заявленной теме Internet'

    @allure.title('Тест релевантности контента основной страницы: smtp')
    def test_main_content_smtp(self):
        """Тест релевантности контента основной страницы: smtp
        Ожидаемый результат: страница релевантна"""
        with allure.step('Переход по ссылке: smtp'):
            self.main_page.content_smtp()
        with allure.step('Проверка релевантности контента'):
            title = self.main_page.switch_page().title.lower()
            assert 'smtp' in title, f'Контент нерелевантен заявленной теме smtp'

    @allure.title('Тестирование функционала логотипа')
    def test_logo(self):
        """Тестирование функционала логотипа
        Ожидаемый результат: логотип кликабельный и возвращает на основную страницу"""
        with allure.step('Клик по лого'):
            self.main_page.click_logo()
        with allure.step('Проверка текущего url'):
            assert self.driver.current_url == self.main_page.url, \
                f'Логотип вернул не на домашнюю страницу'

    @allure.title('Тестирование функционала кнопки домой')
    def test_home_btn(self):
        """Тестирование функционала кнопки домой
        Ожидаемый результат: возвращает на основную страницу"""
        with allure.step('Клик - домой'):
            self.main_page.click_home()
        with allure.step('Проверка текущего url'):
            assert self.driver.current_url == self.main_page.url, \
                f'Кнопка домой не вернула на домашнюю страницу'

    @allure.title('Тест релевантности контента nav bar python: history')
    def test_python_history_nav(self):
        """Тест релевантности контента nav bar python: history
        Ожидаемый результат: релевантный контент"""
        with allure.step('Переход nav bar -> python -> history'):
            self.main_page.python_history_nav()
        with allure.step('Проверка релевантности контента'):
            title = self.main_page.switch_page().title.lower().split()
            assert 'history' in title, 'Контент нерелевантен'
            assert 'python' in title, 'Контент нерелевантен'

    @allure.title('Тест релевантности контента nav bar python: flask')
    def test_python_flask(self):
        """Тест релевантности контента nav bar python: flask
        Ожидаемый результат: релевантный контент"""
        with allure.step('Переход nav bar -> python -> flask'):
            self.main_page.python_flask_nav()
        with allure.step('Проверка релевантности контента'):
            title = self.main_page.switch_page().title.lower().split()
            assert 'flask' in title, 'Контент нерелевантен'

    @allure.title('Тест релевантности контента linux: download Centos7')
    def test_centos_download(self):
        """Тест релевантности контента nav bar linux: download Centos7
        Ожидаемый результат: релевантный контент"""
        with allure.step('Переход nav bar -> linux -> download Centos7'):
            self.main_page.linux_download()
        with allure.step('Проверка релевантности контента'):
            title = self.main_page.switch_page().title.lower().split()
        assert 'centos' in title, 'Контент нерелевантен'

    @allure.title('Тест релевантности контента nework: whireshark news')
    def test_network_wireshark_news(self):
        """Тест релевантности контента nav bar network: whireshark news
        Ожидаемый результат: релевантный контент"""
        with allure.step('Переход nav bar -> network -> whireshark news'):
            self.main_page.network_wireshark_news()
        with allure.step('Проверка релевантности контента'):
            title = self.main_page.switch_page().title.lower().split()
            assert 'wireshark' in title, 'Контент нерелевантен'
            assert 'news' in title, 'Контент нерелевантен'

    @allure.title('Тест релевантности контента nework: whireshark download')
    def test_network_wireshark_download(self):
        """Тест релевантности контента nav bar network: whireshark download
        Ожидаемый результат: релевантный контент"""
        with allure.step('Переход nav bar -> network -> whireshark download'):
            self.main_page.network_wireshark_download()
        with allure.step('Проверка релевантности контента'):
            title = self.main_page.switch_page().title.lower().split()
            assert 'wireshark' in title, 'Контент нерелевантен'

    @allure.title('Тест релевантности контента nework: tcpdump examples')
    def test_network_tcpdump_example(self):
        """Тест релевантности контента nav bar network: tcpdump examples
        Ожидаемый результат: релевантный контент"""
        with allure.step('Переход nav bar -> network -> tcpdump examples'):
            self.main_page.network_tcpdump_example()
        with allure.step('Проверка релевантности контента'):
            title = self.main_page.switch_page().title.lower().split()
            assert 'tcpdump' in title, 'Контент нерелевантен'
            assert 'examples' in title, 'Контент нерелевантен'
