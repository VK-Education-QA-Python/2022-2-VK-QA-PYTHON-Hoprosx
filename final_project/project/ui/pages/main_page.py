import allure

from ui.pages.base_page import BasePage
from configuration import APP_URL
from ui.locators.locators import MainPageLocators

class MainPage(BasePage):

    url = APP_URL + '/welcome/'

    locators = MainPageLocators()

    @allure.step('Кнопка выйти')
    def log_out(self):
        self.element_is_clickable(self.locators.LOGOUT).click()

    @allure.step('Основной контент: API')
    def content_api(self):
        self.element_is_clickable(self.locators.CONTENT_API).click()

    @allure.step('Основной контент: История интернета')
    def content_internet(self):
        self.element_is_clickable(self.locators.CONTENT_INTERNET).click()

    @allure.step('Основной контент: SMTP')
    def content_smtp(self):
        self.element_is_clickable(self.locators.CONTENT_SMTP).click()

    @allure.step('Клик лого')
    def click_logo(self):
        self.element_is_clickable(locator=self.locators.LOGO).click()

    @allure.step('Клик HOME')
    def click_home(self):
        self.element_is_clickable(locator=self.locators.NAV_HOME).click()

    @allure.step('Nav bar python - history')
    def python_history_nav(self):
        self.hover_and_click_nav_bar(self.locators.NAV_PYTHON, self.locators.PYTHON_HISTORY)

    @allure.step('Nav bar python - flask')
    def python_flask_nav(self):
        self.hover_and_click_nav_bar(self.locators.NAV_PYTHON, self.locators.FLASK)

    @allure.step('Nav bar linux - download')
    def linux_download(self):
        self.hover_and_click_nav_bar(self.locators.NAV_LINUX, self.locators.LINUX_DOWNLOAD)

    @allure.step('Nav bar network - wireshark - news')
    def network_wireshark_news(self):
        self.hover_and_click_nav_bar(self.locators.NAV_NETWORK, self.locators.NETWORK_WIRESHARK_NEWS)

    @allure.step('Nav bar network - wireshark - download')
    def network_wireshark_download(self):
        self.hover_and_click_nav_bar(self.locators.NAV_NETWORK, self.locators.NETWORK_WIRESHARK_DOWNLOAD)

    @allure.step('Nav bar tcpdump - examples')
    def network_tcpdump_example(self):
        self.hover_and_click_nav_bar(self.locators.NAV_NETWORK, self.locators.TCPDUMP_EXAMPLES)


