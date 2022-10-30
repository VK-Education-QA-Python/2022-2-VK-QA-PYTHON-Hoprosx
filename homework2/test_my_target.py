import allure
import pytest

from base import BaseCase
from ui.locators.locators import Segments


@pytest.mark.UI
@allure.feature('Ui тесты: сегменты')
class TestMyTargetSegments(BaseCase):

    @allure.title('Cоздание сегмента в аудиториях с типом "Приложения и игры в соцсетях"')
    def test_create_new_segment(self, log_in, segments_page):
        with allure.step('Открытие страницы с сегментами'):
            segments_page.open()
        with allure.step('Создание сегмента с категорией: Приложения и игры'):
            segment_name = segments_page.create_segment(segments_category=Segments.categories.APPS_AND_GAMES)
        with allure.step('Проверка наличия нового сегмента'):
            assert segments_page.check_segment(segment_name), f"New segment with name {segment_name} doesn't found"

    @allure.title('Создание сегмента с типом группы ОК и ВК и его удаление')
    def test_add_VK_and_OK_data_sourcre(self, log_in, segments_page):
        with allure.step('Открытие страницы с сегментами'):
            segments_page.open()
        with allure.step('Создание источника данных https://education.vk.company/'):
            group_name = segments_page.add_OK_and_VK_link_data_source('https://education.vk.company/')
            segments_page.refresh()
        with allure.step('Создание сегмента с категорией - Группы ОК и ВК'):
            segment_name = segments_page.create_segment(segments_category=Segments.categories.GROUPS_OK_AND_VK)
        with allure.step('Удаление'):
            segments_page.delete_segment(segment_name),
        with allure.step('Проверка удаления сегмента'):
            segments_page.check_segment(segment_name), f"Segment with name: {segment_name} doesn't delete"
        with allure.step('Удаление источника данных https://education.vk.company/'):
            segments_page.delete_OK_and_VK_segments_data_source(group_name)
        with allure.step('Проверка удаления источника данных https://education.vk.company/'):
            assert segments_page.check_OK_and_VK_segments_data_source(group_name), f"Data source with name: {group_name} exist"

@pytest.mark.UI
@allure.feature('Ui тесты: кампании')
class TestMyTargetCampaign(BaseCase):

    @allure.title('Cоздание рекламной кампании: Охват + баннер')
    def test_create_new_campaign(self, log_in, dashboard_page, file_path_picture):
        with allure.step('Открытие страницы с кампаниями'):
            dashboard_page.open()
        with allure.step('Создание кампании'):
            campaign_name = dashboard_page. \
                create_campaign_with_banner_type("https://www.google.com/", picture_path=file_path_picture)
        with allure.step('Проверка наличия кампании'):
            assert dashboard_page.check_campaign(campaign_name), f"Campaign  with name: {campaign_name} doesn't exist"
