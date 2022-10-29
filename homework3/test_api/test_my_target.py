from test_api.base import ApiBase
import pytest


@pytest.mark.API
class TestMyTarget(ApiBase):
    authorize = True

    def test_create_campaign(self):
        """Тест на работу  с кампанией:

        1)Создание кампании
        2)Проверка существования кампании
        3)Удаление кампании
        4)Проверка удаления кампании

        Ожидаемый результат: Кампания успешно создана и удалена
        """
        campaign = self.api_client.create_campaign_special()
        assert self.api_client.check_campaign(campaign) is True, \
            f"Campaign doesn't created, " \
            f"but response was successes, response: {campaign}"

        self.api_client.delete_campaign(campaign)
        assert self.api_client.check_campaign(campaign) is False, \
            f"Campaign doesn't deleted, " \
            f"but response was successes, response: {campaign}"

    def test_create_segment(self):
        """Тест на работу с сегментом:

        1)Создание сегмента
        2)Проверка существования сегмента
        3)Удаление сегмента
        4)Проверка удаления сегмента

        Ожидаемый результат: Кампания успешно создана и удалена
        """
        segment = self.api_client.create_segment_apps_and_games_in_social_media()
        assert self.api_client.check_segment(segment) is True, \
            f"Segment doesn't created, " \
            f"but response was successes, response: {segment}"

        self.api_client.delete_segment(segment)
        assert self.api_client.check_segment(segment) is False, \
            f"Segment doesn't deleted, " \
            f"but response was successes, response: {segment}"

    def test_create_segment_with_OK_and_VK_data_sourse(self):
        """Тест на создание сегмента, с источником данных - группа VK образования
           (https://education.vk.company/):

        1)Добавление в источники данных группы VK образования
        2)Проверка существования источника данных
        3)Создание сегмента с источником данных - группа VK образования
        4)Удаление сегмента
        5)Проверка удаления сегмента
        6)Удаление источника данных группы VK образования
        7)Проверка удаления источника данных

        Ожидаемый результат: созданы и удалены источник данных и сегмент
        """
        social_media = 'ok'

        data_source = self.api_client.create_groups_OK_and_VK_data_source('https://education.vk.company/', group=social_media)
        assert self.api_client.check_groups_OK_and_VK_data_source(data_source, group=social_media) is True, \
            f"Data source was created with id:{data_source} " \
            f"but this data source didn't exist in api/v2/remarketing/{social_media}_groups.json"

        segment = self.api_client.create_segment_groups_OK_and_VK(data_source_id=data_source)
        assert self.api_client.check_segment(segment) is True, \
            f"Segment doesn't created, " \
            f"but response was successes, response: {segment}"

        self.api_client.delete_segment(segment)
        assert self.api_client.check_segment(segment) is False, \
            f"Segment doesn't deleted, " \
            f"but response was successes, response: {segment}"

        self.api_client.delete_groups_OK_and_VK_data_source(data_source, group=social_media)
        assert self.api_client.check_groups_OK_and_VK_data_source(data_source, group=social_media) is False, \
            f"Data source with id:{data_source} didn't delete"
