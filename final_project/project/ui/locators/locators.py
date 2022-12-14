from selenium.webdriver.common.by import By

class BaseLocators:
    SUBMIT_BTN = (By.CSS_SELECTOR, 'input[name="submit"]')
    INPUT_USERNAME = (By.CSS_SELECTOR, 'input[name="username"]')
    INPUT_PASSWORD = (By.CSS_SELECTOR, 'input[name="password"]')

class LoginPageLocators(BaseLocators):
    REGISTRATION_PAGE = (By.CSS_SELECTOR, 'a[href="/reg"]')
    INVALID_DATA_OR_UNAUTHORIZED = (By.ID, 'flash')

class RegistrationPageLocators(BaseLocators):
    INPUT_NAME = (By.CSS_SELECTOR, 'input[name="name"]')
    INPUT_SURNAME = (By.CSS_SELECTOR, 'input[name="surname"]')
    INPUT_MIDDLE_NAME = (By.CSS_SELECTOR, 'input[name="middlename"]')
    INPUT_EMAIL = (By.CSS_SELECTOR, 'input[name="email"]')
    INPUT_CONFIRM_PASS = (By.CSS_SELECTOR, 'input[name="confirm"]')
    SDET_CHECKBOX = (By.CSS_SELECTOR, 'input[name="term"]')
    LOG_IN_PAGE = (By.CSS_SELECTOR, 'a[href="/login"]')

class MainPageLocators(BaseLocators):
    LOGO = (By.CSS_SELECTOR, 'a[class*="brand"]')
    NAV_HOME = (By.LINK_TEXT, 'HOME')
    NAV_PYTHON = (By.XPATH, '//a[text()="Python"]//parent::li')
    PYTHON_HISTORY = (By.LINK_TEXT, 'Python history')
    FLASK = (By.LINK_TEXT, 'About Flask')
    NAV_LINUX = (By.XPATH, '//a[text()="Linux"]//parent::li')
    LINUX_DOWNLOAD = (By.LINK_TEXT, 'Download Centos7')
    NAV_NETWORK = (By.XPATH, '//a[text()="Network"]//parent::li')
    NETWORK_WIRESHARK_NEWS = (By.XPATH, '//li[contains(text(), "Wireshark")]//a[contains(text(), "News")]')
    NETWORK_WIRESHARK_DOWNLOAD = (By.XPATH, '//li[contains(text(), "Wireshark")]//a[contains(text(), "Download")]')
    TCPDUMP_EXAMPLES = (By.XPATH, '//li[contains(text(), "Tcpdump")]//a[contains(text(), "Examples")]')
    LOGGED = (By.XPATH, '//li[contains(text(), "Logged")]')
    USER = (By.XPATH, '//li[contains(text(), "User")]')
    LOGOUT = (By.CSS_SELECTOR, 'a[href="/logout"]')
    CONTENT_API = (By.XPATH, '//div[contains(text(),"API")]//parent::div//a')
    CONTENT_INTERNET = (By.XPATH, '//div[contains(text(),"internet")]//parent::div//a')
    CONTENT_SMTP = (By.XPATH, '//div[contains(text(),"SMTP")]//parent::div//a')