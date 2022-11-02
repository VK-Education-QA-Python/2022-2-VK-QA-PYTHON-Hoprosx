import os
import random
import time
import uuid

import allure
import pytest
from selenium.common import TimeoutException
from selenium.webdriver.common.by import By

from ui.locators.locators import Dashboard
from ui.pages.base_my_target import BaseMyTargetPage


class DashboardPage(BaseMyTargetPage):
    locators = Dashboard()
    url = 'https://target-sandbox.my.com/dashboard'

    @allure.step('Создание кампании: начало')
    def create_campaign(self):
        try:
            self.element_is_clickable(self.locators.CREATE_CAMPAIGN_WITHOUT_EXISTING_CAMPAIGN).click()
        except:
            self.element_is_clickable(self.locators.CREATE_CAMPAIGN_WITH_EXISTS_CAMPAIGN).click()

    @allure.step('Выбор цели компании')
    def select_purpose_of_campaign(self, locator):
        self.element_is_clickable(locator).click()

    @allure.step('Добавление ссылки для раскрутки')
    def add_link_to_create_campaign(self, link):
        self.element_is_clickable(self.locators.INPUT_LINK_TO_START_CREATE_CAMPAIGN).send_keys(link)

    @allure.step('Установка дневного бюджета')
    def budget_per_day(self, summ:int|float):
        self.element_is_clickable(self.locators.BUDGET_PER_DAY).send_keys(summ)

    @allure.step('Установка всего бюджета')
    def budget_total(self, summ:int|float):
        self.element_is_clickable(self.locators.BUDGET_TOTAL).send_keys(summ)

    @allure.step('Тип компании - баннер')
    def select_banner_picture_type(self):
        self.element_is_clickable(self.locators.BANNER_PICTURE_TYPE).click()

    @allure.step('Загрузка картинки 240х400')
    def add_picture_200x400(self, file_path:str):
        try:
            self.element_is_present(self.locators.INPUT_PICTURE).send_keys(file_path)
        except:
            raise Exception("format is not a suitable")
        self.element_is_clickable(self.locators.SAVE_PICTURE).click()

    @allure.step('Имя компании')
    def set_campaign_name(self) -> str:
        campaign_name = str(uuid.uuid1())
        self.element_is_clickable(self.locators.INPUT_CAMPAIGN_NAME).clear()
        self.element_is_clickable(self.locators.INPUT_CAMPAIGN_NAME).send_keys(campaign_name)
        return campaign_name

    @allure.step('Подтверждение создания кампании')
    def submit_campaign_creation(self):
        self.element_is_clickable(self.locators.SUBMIT_CREATE_CAMPAIGN).click()

    def create_campaign_with_banner_type(self, link, picture_path:str, budget_per_day:int|float=100, budget_total:int|float=20000) -> str:
        self.create_campaign()
        self.select_purpose_of_campaign(self.locators.REACH)
        self.add_link_to_create_campaign(link)
        self.budget_per_day(budget_per_day)
        self.budget_total(budget_total)
        self.select_banner_picture_type()
        self.add_picture_200x400(picture_path)
        campaign_name = self.set_campaign_name()
        self.submit_campaign_creation()
        self.refresh()
        return campaign_name

    @allure.step('Поиск кампании')
    def check_campaign(self, campaign_name:str):
        self.element_is_clickable(self.locators.SEARCH_CAMPAIGN_INPUT).send_keys(campaign_name)
        self.element_is_clickable((By.XPATH, f'//li[@title="{campaign_name}"]')).click()
        return self.element_is_clickable((By.XPATH, f'//a[@title="{campaign_name}"]'))
