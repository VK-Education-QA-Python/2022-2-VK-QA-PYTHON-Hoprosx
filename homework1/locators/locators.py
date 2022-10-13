from selenium.webdriver.common.by import By


class Locators:
    # main page
    LOG_IN_BTN = (By.CSS_SELECTOR, 'div[class*="Head"][class*="button"]')
    LOG_EMAIL_INPUT = (By.CSS_SELECTOR, 'input[name="email"]')
    LOG_EMAIL_PASSWORD = (By.CSS_SELECTOR, 'input[name="password"]')
    LOG_IN_SUBMIT_BTN = (By.CSS_SELECTOR, 'div[class*="auth"][class*="button"]')
    LOG_ERROR = (By.CSS_SELECTOR, 'div[class*="js_form_msg"]')
    ENTER_BTN = (By.CSS_SELECTOR, 'div[class*="responseHead-module-button"]')
    LOG_IN_ERROR = (By.CSS_SELECTOR, 'div[class*="notify-module-error"]')

    # dashboard
    DASHBOARD_BALANCE = (By.CSS_SELECTOR, 'div[class*="right-module"][class*="rightButton"]')
    DASHBOARD_QUIT = (By.XPATH, '//a[@href="/logout"]/parent::li')
    DASHBOARD_USER_NAME = (By.CSS_SELECTOR, 'div[class*="userName"]')

    # profile
    PROFILE = (By.CSS_SELECTOR, 'a[href="/profile"]')
    FIO = (By.CSS_SELECTOR, 'div[data-name="fio"] input')
    PROFILE_SUBMIT = (By.CSS_SELECTOR, 'button[class*="button_submit"]')
    SUCCESS_UPDATE = (By.CSS_SELECTOR, 'div[class*="success"][style="display: block;"]')
