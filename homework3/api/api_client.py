import json
import random
import uuid
from typing import Optional, Union
from urllib.parse import urljoin
import requests
from requests import Response
from api.api_data import *

class ApiClientException(Exception):
    ...


class ResponseStatusCodeException(Exception):
    ...


class RespondErrorException(Exception):
    ...


class ApiClient:
    """Клиент для работы с апи https://target-sandbox.my.com/"""

    def __init__(self, base_url: str, email: str, password: str):
        self.password = password
        self.email = email
        self.base_url = base_url
        self.session = requests.session()

    def _request(self, method: str, location: str, headers: Optional[dict], data: str = None,
                 params: str = None, allow_redirects: bool = False,
                 expected_status_code: Union[int, list] = 200,
                 jsonify: bool = True) -> 'Response or json':

        url = urljoin(self.base_url, location)

        response = self.session.request(method=method, url=url, headers=headers, data=data, params=params,
                                        allow_redirects=allow_redirects)
        if type(expected_status_code) is list:
            if response.status_code not in expected_status_code:
                raise ResponseStatusCodeException(f'Expected {expected_status_code}, but got {response.status_code}')
        if type(expected_status_code) is int:
            if response.status_code != expected_status_code:
                raise ResponseStatusCodeException(f'Expected {expected_status_code}, but got {response.status_code}')
        if jsonify:
            json_response: dict = response.json()

            return json_response
        return response

    def post_login(self) -> None:
        """Авторизация апи клиента"""

        data = {
            'email': self.email,
            'password': self.password,
            'continue': 'https://target-sandbox.my.com/auth/mycom?state=target_login%3D1%26ignore_opener%3D1#email',
            'failure': 'https://account.my.com/login/'
        }

        headers = {"Referer": "https://target-sandbox.my.com/"}

        self.session.post('https://auth-ac.my.com/auth', data=data, headers=headers)

        headers = {
            "Referer": "https://target-sandbox.my.com/",
        }
        self.session.post('https://auth-ac.my.com/auth', data=data, headers=headers)

        headers = {
            "Host": 'target-sandbox.my.com',
            "Referer": "https://target-sandbox.my.com/dashboard"
        }

        self.session.get('https://target-sandbox.my.com/csrf/', headers=headers)

    def create_campaign_special(self, name: str = "My campaign") -> json:
        """Создание кампании с типом 'Специальные возможности'"""

        campaign_name = name + ' ' + str(uuid.uuid1())
        headers = {
            "X-CSRFToken": f"{self.session.cookies['csrftoken']}",
        }

        data = campaign_data
        data['name'] = campaign_name
        data['banners'][0]['urls']['primary']['id'] = self.get_url_for_campaign('https://www.google.com/')
        data = json.dumps(data)

        create_campaign_response = self._request(method='POST', location="api/v2/campaigns.json",
                                                 headers=headers, data=data, allow_redirects=False,
                                                 expected_status_code=200, jsonify=True)
        return create_campaign_response

    def check_campaign(self, create_campaign_response) -> bool:
        """Проверка существования кампании"""

        campaign_id = self.get_main_id(create_campaign_response)

        location = f"api/v2/campaigns/{campaign_id}.json?fields=id,name,status"
        response = self._request(method='GET', location=location, headers=None,
                                 allow_redirects=False, expected_status_code=[200, 404])
        print(response)

        if response['status'] == 'active':
            return True
        elif response['status'] == 'deleted':
            return False
        else:
            raise ApiClientException('undefined status')

    def get_main_id(self, create_campaign_response: json) -> int:
        """Получает id кампании из json полученного после создания кампании"""

        return create_campaign_response['id']

    def get_url_for_campaign(self, url:str) -> int:
        """Получает id рекламируемого url"""

        params = 'url=' + url
        response = self._request(method='GET', location="api/v1/urls", headers=None,
                                 params=params, expected_status_code=200,
                                 allow_redirects=True, jsonify=True)

        return response['id']

    def delete_campaign(self, create_campaign_response: json) -> Response:
        """Удаление кампании"""

        id = self.get_main_id(create_campaign_response)

        headers = {
            "X-CSRFToken": f"{self.session.cookies['csrftoken']}",
        }

        location = f'api/v2/campaigns/{id}.json'
        response = self._request(method='DELETE', location=location,
                                 headers=headers, allow_redirects=False,
                                 expected_status_code=204, jsonify=False)
        return response

    def create_segment_apps_and_games_in_social_media(self, name: str = "My simple segment") -> json:
        """Создание сегмента с типом 'Приложения и игры в социальных сетях'"""

        segment_name = name + ' ' + str(uuid.uuid1())
        headers = {
            "X-CSRFToken": f"{self.session.cookies['csrftoken']}",
        }

        data = segment_segment_apps_and_games_in_social_media_data
        data['name'] = segment_name
        data = json.dumps(data)

        response = self._request(method='POST', location='api/v2/remarketing/segments.json?',
                                 headers=headers, data=data, allow_redirects=False,
                                 expected_status_code=200, jsonify=True)
        return response

    def create_segment_groups_OK_and_VK(self, name: str = "My simple segment",
                                        data_source_id: int = None,
                                        groups: str = 'OK') -> Response:
        """Создание сегмента с типом 'группы OK и ВК'

        :param groups: 'OK' or 'VK"
        """
        segment_name = name + ' ' + str(uuid.uuid1())
        headers = {
            "X-CSRFToken": f"{self.session.cookies['csrftoken']}",
        }

        data = segment_groups_OK_and_VK_data
        data['name'] = segment_name
        data['relations'][0]['params']['source_id'] = self.get_data_source_source_id_by_id(data_source_id, groups)
        data = json.dumps(data)

        response = self._request(method='POST', location='api/v2/remarketing/segments.json',
                                 headers=headers, data=data, expected_status_code=200)
        return response

    def check_segment(self, create_segment_response: json) -> bool:
        """Проверка существования сегмента"""

        segment_id = self.get_main_id(create_segment_response)
        location = f'api/v2/remarketing/segments/{segment_id}.json'
        response = self._request(method='GET', location=location,
                                 headers=None, allow_redirects=True,
                                 expected_status_code=[200, 404], jsonify=True)

        return str(segment_id) in str(response)

    def delete_segment(self, create_segment_response: json) -> Response:
        """Удаление сегмента"""

        segment_id = self.get_main_id(create_segment_response)
        headers = {
            "X-CSRFToken": f"{self.session.cookies['csrftoken']}",
        }

        location = f'api/v2/remarketing/segments/{segment_id}.json'

        response = self._request(method='DELETE', location=location,
                                 headers=headers, expected_status_code=204,
                                 allow_redirects=False, jsonify=False)
        return response

    def get_url_id_for_data_source(self, url: str, group: str) -> int:
        """Получение url id для создания источника данных с типом 'группы OK и ВК'

        :param groups: 'OK' or 'VK"
        """

        params = '_q=' + url

        if group.lower() == 'vk':
            response = self._request(method='GET', location='api/v2/vk_groups.json',
                                     headers=None, params=params, expected_status_code=200,
                                     allow_redirects=False)
            return response['items'][random.randint(0, len(response['items']))]['id']
        elif group.lower() == 'ok':
            response = self._request(method='GET', location='api/v1/odkl_groups.json',
                                     headers=None, params=params, expected_status_code=200,
                                     allow_redirects=False)
            return response[random.randint(0, len(response))]['id']
        else:
            raise ApiClientException('Group must be equal to OK(ok) or VK(vk)')

    def create_groups_OK_and_VK_data_source(self, url: str, group: str = 'OK') -> int:
        """Создание источника данных с типом 'группы OK и ВК'

        :param groups: 'OK' or 'VK"
        """

        url_id = self.get_url_id_for_data_source(url, group)
        headers = {
            "X-CSRFToken": f"{self.session.cookies['csrftoken']}",
        }

        data = {"items": [{"object_id": f"{url_id}"}]}
        data = json.dumps(data)

        if group == 'VK' or group == 'vk':
            response = self._request(method='POST', location='api/v2/remarketing/vk_groups/bulk.json',
                                     headers=headers, data=data, expected_status_code=201)
        elif group.lower() == 'ok':
            response = self._request(method='POST', location='api/v2/remarketing/ok_groups/bulk.json',
                                     headers=headers, data=data, expected_status_code=201)
        else:
            raise ApiClientException('Group must be equal to OK(ok) or VK(vk)')

        data_source_id = response['items'][0]['id']
        return data_source_id

    def delete_groups_OK_and_VK_data_source(self, id: int, group: str = 'OK') -> Response:
        """Удаление источника данных с типом 'группы OK и ВК'

        :param groups: 'OK' or 'VK"
        """

        headers = {
            "X-CSRFToken": f"{self.session.cookies['csrftoken']}",
        }

        if group.lower() == 'vk':
            response = self._request(method='DELETE', location=f'api/v2/remarketing/vk_groups/{id}.json',
                                     headers=headers, expected_status_code=204, jsonify=False)
            return response
        elif group.lower() == 'ok':
            response = self._request(method='DELETE', location=f'api/v2/remarketing/ok_groups/{id}.json',
                                     headers=headers, expected_status_code=204, jsonify=False)
            return response
        else:
            raise ApiClientException('Group must be equal to OK(ok) or VK(vk)')

    def check_groups_OK_and_VK_data_source(self, id: int, group: str = 'OK') -> bool:
        """Проверка наличия источника данных с типом 'группы OK и ВК'

        :param groups: 'OK' or 'VK"
        """

        if group.lower() == 'vk':
            response = self._request(method='GET',
                                     location=f'api/v2/remarketing/vk_groups.json?fields=id&limit=50',
                                     headers=None, expected_status_code=200)
            return str(id) in str(response)
        elif group.lower() == 'ok':
            response = self._request(method='GET',
                                     location=f'api/v2/remarketing/ok_groups.json?fields=id&limit=50',
                                     headers=None, expected_status_code=200)
            return str(id) in str(response)
        else:
            raise ApiClientException('Group must be equal to OK(ok) or VK(vk)')

    def get_data_source_source_id_by_id(self, id: int, group: str = 'OK') -> int:
        """Получение source_id для источника данных с типом 'группы OK и ВК'

        :param groups: 'OK' or 'VK"
        """

        if group.lower() == 'vk':
            response = self._request(method='GET',
                                     location='api/v2/remarketing/vk_groups.json',
                                     headers=None, expected_status_code=200)
            for item in range(response['count']):
                if response['items'][item]['id'] == id:
                    source_id = response['items'][item]['object_id']
                    return source_id

        elif group.lower() == 'ok':
            response = self._request(method='GET',
                                     location='api/v2/remarketing/ok_groups.json',
                                     headers=None, expected_status_code=200)
            for item in range(response['count']):
                if response['items'][item]['id'] == id:
                    source_id = response['items'][item]['object_id']
                    return source_id
        else:
            raise ApiClientException('Group must be equal to OK(ok) or VK(vk)')

