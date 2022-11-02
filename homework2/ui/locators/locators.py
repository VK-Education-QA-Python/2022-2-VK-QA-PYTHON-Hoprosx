from selenium.webdriver.common.by import By


class BaseLanding:
    LOG_IN_BTN = (By.CSS_SELECTOR, 'div[class*="Head"][class*="button"]')
    LOG_EMAIL_INPUT = (By.CSS_SELECTOR, 'input[name="email"]')
    LOG_EMAIL_PASSWORD = (By.CSS_SELECTOR, 'input[name="password"]')
    LOG_IN_SUBMIT_BTN = (By.CSS_SELECTOR, 'div[class*="auth"][class*="button"]')
    LOG_IN_ERROR = (By.CSS_SELECTOR, 'div[class*="notify-module-error"]')
    LOG_IN_ERROR_WITH_REDIRECT = (By.CSS_SELECTOR, 'div[class*="js_form_msg"]')
    ENTER_BTN = (By.CSS_SELECTOR, 'div[class*="responseHead-module-button"]')


class MyTargetBase:
    # header
    HEADER_BALANCE = (By.CSS_SELECTOR, 'div[class*="right-module"][class*="rightButton"]')
    HEADER_QUIT = (By.XPATH, '//a[@href="/logout"]/parent::li')
    HEADER_USER_NAME = (By.CSS_SELECTOR, 'div[class*="userName"]')


class Dashboard(MyTargetBase):
    CREATE_CAMPAIGN_WITHOUT_EXISTING_CAMPAIGN = (By.CSS_SELECTOR, 'a[href="/campaign/new"]')
    CREATE_CAMPAIGN_WITH_EXISTS_CAMPAIGN = (By.CSS_SELECTOR, 'div[class*="createButton"] div[data-test="button"]')
    REACH = (By.CSS_SELECTOR, 'div[class*=" _reach"]')
    INPUT_LINK_TO_START_CREATE_CAMPAIGN = (By.CSS_SELECTOR, 'input[data-gtm-id="ad_url_text"]')
    BUDGET_PER_DAY = (By.CSS_SELECTOR, 'input[data-test="budget-per_day"]')
    BUDGET_TOTAL = (By.CSS_SELECTOR, 'input[data-test="budget-total"]')
    BANNER_PICTURE_TYPE = (By.CSS_SELECTOR, 'div[id="patterns_banner_4"]')
    INPUT_PICTURE = (By.CSS_SELECTOR, 'div[class*="240x400"] input[type="file"]')
    SAVE_PICTURE = (By.CSS_SELECTOR, 'input[data-translated-lit*="Save image"]')
    INPUT_CAMPAIGN_NAME = (By.CSS_SELECTOR, 'div[class*="bottom"] input[class*="input__inp js-form"]')
    SUBMIT_CREATE_CAMPAIGN = (By.CSS_SELECTOR, 'div[class*="footer__button"] button')
    SEARCH_CAMPAIGN_INPUT = (By.CSS_SELECTOR, 'input[class*="searchInput"]')

class Segments(MyTargetBase):
    CREATE_SEGMENTS_WHEN_ZERO_SEGMENTS = (By.CSS_SELECTOR, 'a[href*="segments_list/new"]')
    CREATE_SEGMENTS_WHEN_NOT_ZERO_SEGMENTS = (
        By.CSS_SELECTOR, 'div[class*="segments-list__btn-wrap"] div[class="button__text"]')
    CHECKBOX = (By.CSS_SELECTOR, 'input[class*="adding-segments-source__checkbox"]')
    APPS_AND_GAMES = (By.CSS_SELECTOR, '//div[contains(@class, "adding-segments-modal__block-left")]/div[8]')
    ADD_SEGMENT_BTN = (By.CSS_SELECTOR, 'div[class*="js-add-button"]')
    INPUT_SEGMENT_NAME = (By.CSS_SELECTOR, 'div[class*="create-segment-form"] input[maxlength="60"]')
    FINAL_ADD_SEGMENT_BTN = (By.XPATH, '//div[@class="create-segment-form"]//*[@class="button__text"]')
    SEARCH_SEGMENT_INPUT = (By.CSS_SELECTOR, 'input[class*="searchInput"]')

    SOURCE_HEADER_WITH_CHECKBOX = (By.XPATH, '//div[contains(@class, "source__header")]')
    DATA_SOURCE_GROUPS_OK_AND_VK = (By.CSS_SELECTOR, 'a[href="/segments/groups_list"]')
    OK_AND_VK_INPUT = (By.CSS_SELECTOR, 'input[class*="searchInput"]')
    OK_AND_VK_INPUT_OK_GROUPS_SHOW_ALL = (By.XPATH, '//span[contains(text(),"(ОК)")]/following::*[@data-test="show"]')
    SELECT_GROUP = (By.CSS_SELECTOR, 'li[class*="optionsList"]')
    ADD_SELECTED_DATA_SOURCE_BTN = (By.CSS_SELECTOR, 'div[data-test="add_selected_items_button"]')
    INPUT_FIND_TO_DELETE_DATA_SOURCE = (By.CSS_SELECTOR, 'input[class*="suggester-ts__input"]')
    REMOVE = (By.CSS_SELECTOR, 'div[data-class-name="RemoveView"]')
    CONFIRM_REMOVE = (By.CSS_SELECTOR, 'button[class*="confirm-remove"]')
    SEARCH_DATA_SOURCE_INPUT = (By.CSS_SELECTOR, 'input[class*="suggester-ts__input"]')
    CHECK_DATA_SOURCE_INPUT = (By.XPATH, '//span[contains(text(), "Ничего") or contains(text(), "Nothing" )]')

    class categories:
        APPS_AND_GAMES = (By.XPATH,
                          '//div[contains(@class,"modal")] /div[contains(text(), "Приложения и игры в соцсетях") or contains(text(), "Apps and games in social networks" )]')
        GROUPS_OK_AND_VK = (By.XPATH,
                            '//div[contains(@class,"modal")] /div[contains(text(), "Группы ОК и VK") or contains(text(), "Groups OK and VK" )]')
