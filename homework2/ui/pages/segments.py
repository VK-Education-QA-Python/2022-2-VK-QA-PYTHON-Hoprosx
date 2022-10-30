import random
import time
import uuid

import allure

from ui.locators.locators import Segments
from ui.pages.base_my_target import BaseMyTargetPage
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException


class SegmentsPage(BaseMyTargetPage):
    locators = Segments()
    url = 'https://target-sandbox.my.com/segments'

    @allure.step('Поиск чекбокса')
    def find_and_click_check_box(self, check_box_name):
        CHECK_BOX = (
        By.CSS_SELECTOR, f'//*[contains(text(), "{check_box_name}")]/preceding::input[contains(@class, "add")]')
        self.element_is_clickable(self.locators.SOURCE_HEADER_WITH_CHECKBOX).click()
        CHECK_BOX_ELEM = self.element_is_visible(CHECK_BOX)
        CHECK_BOX_ELEM.click()

    @allure.step('Выбор категории сегмента')
    def select_segment_category(self, segments_category):
        category_elem = self.element_is_clickable(segments_category)
        category_elem.click()

    @allure.step('Создание сегмента: начало')
    def create_segment_button(self):
        # проверяем кнопку в случаях когда сегментов нет и когда есть созданные сегменты
        try:
            self.element_is_clickable(self.locators.CREATE_SEGMENTS_WHEN_ZERO_SEGMENTS).click()
        except TimeoutException:
            self.element_is_clickable(self.locators.CREATE_SEGMENTS_WHEN_NOT_ZERO_SEGMENTS).click()

    @allure.step('Создать сегмент')
    def add_segment_btn(self):
        self.element_is_clickable(self.locators.ADD_SEGMENT_BTN).click()

    @allure.step('Имя сегмента')
    def set_segment_name(self, segment_name: str):
        self.element_is_visible(self.locators.INPUT_SEGMENT_NAME).clear()
        self.element_is_visible(self.locators.INPUT_SEGMENT_NAME).send_keys(segment_name)

    def create_segment(self, segments_category: tuple = None,
                       check_box_name: str = None):
        """
        Метод для создания сегмента

        :param segments_name: Имя сегмента
        :param segments_category: Категория сегмента, локатор
        :param check_box_name: Чекбокc: по дефолту выбирается главный, можно искать по неполному вхождению
        """
        segment_name = str(uuid.uuid1())
        NEW_SEGMENTS_LOCATOR = (By.CSS_SELECTOR, f'a[title="{segment_name}"]')
        self.create_segment_button()
        self.select_segment_category(segments_category)
        if check_box_name is not None:
            self.find_and_click_check_box(check_box_name)
        else:
            self.element_is_visible(self.locators.CHECKBOX).click()
        self.add_segment_btn()
        self.set_segment_name(segment_name)
        self.element_is_clickable(self.locators.FINAL_ADD_SEGMENT_BTN).click()
        new_segment_elem = self.element_is_present(NEW_SEGMENTS_LOCATOR)
        return segment_name

    @allure.step('удаление сегмента')
    def delete_segment(self, segments_name):
        segment_elem = self.element_is_visible((By.CSS_SELECTOR, f'a[title="{segments_name}"]'))
        segment_elem.find_element('xpath', '//*[contains(@data-test, "remove")]').click()
        return self.element_is_clickable(self.locators.CONFIRM_REMOVE).click()

    @allure.step('Поиск сегмента')
    def check_segment(self, segment_name:str):
        """Комплексная проверка
        1) проверка наличия сегмента в инпуте
        2) проверка что такой сегмент в инпуте один
        3) проверка сегмента в списке сегментов
        """
        self.element_is_clickable(self.locators.SEARCH_SEGMENT_INPUT).send_keys(segment_name)
        try:
            if len(self.element_are_present((By.CSS_SELECTOR, f'li[title="{segment_name}"]'))) == 1:
                self.element_is_clickable((By.CSS_SELECTOR, f'li[title="{segment_name}"]')).click()
            else:
                raise Exception(f'Сегментов с {segment_name} более одного')
        except TimeoutException:
            return False
        #try - чтобы корректно выводилось описание ошибки в ассерте если тест падает раньше
        #решил в этом методе попробовать учесть все
        return self.element_is_clickable((By.CSS_SELECTOR, f'a[title="{segment_name}"]'))

    def add_OK_and_VK_link_data_source(self, link):
        self.element_is_clickable(self.locators.DATA_SOURCE_GROUPS_OK_AND_VK).click()
        self.element_is_clickable(self.locators.OK_AND_VK_INPUT).send_keys(link)
        self.element_is_clickable(self.locators.OK_AND_VK_INPUT_OK_GROUPS_SHOW_ALL).click()
        group_name = self.element_is_clickable(self.locators.SELECT_GROUP).text
        self.element_is_clickable(self.locators.SELECT_GROUP).click()
        self.element_is_clickable(self.locators.ADD_SELECTED_DATA_SOURCE_BTN).click()
        return group_name

    @allure.step('Поиск существующего типа сегмента')
    def find_existing_data_source(self, group_name):
        self.element_is_clickable(self.locators.INPUT_FIND_TO_DELETE_DATA_SOURCE).send_keys(group_name)

    @allure.step('Удаление существующего типа сегмента')
    def delete_selecting_data_source(self):
        self.element_is_clickable(self.locators.REMOVE).click()
        self.element_is_clickable(self.locators.CONFIRM_REMOVE).click()

    def delete_OK_and_VK_segments_data_source(self, group_name:str):
        if self.driver.current_url != self.url:
            self.open()
        self.element_is_clickable(self.locators.DATA_SOURCE_GROUPS_OK_AND_VK).click()
        self.find_existing_data_source(group_name)
        self.delete_selecting_data_source()

    def check_OK_and_VK_segments_data_source(self, group_name:str):
        self.element_is_clickable(self.locators.SEARCH_DATA_SOURCE_INPUT).send_keys(group_name)
        return self.element_is_present(self.locators.CHECK_DATA_SOURCE_INPUT)
