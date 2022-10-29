import json
import random
import uuid
from urllib.parse import urljoin
import requests
from requests import Response


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

    def _request(self, method: str, location: str, headers: dict, data: str = None, params: str = None, allow_redirects: bool = False, expected_status_code: int = 200,
                 jsonify: bool = True) -> 'Response or json':

        url = urljoin(self.base_url, location)

        response = self.session.request(method=method, url=url, headers=headers, data=data, params=params,
                                        allow_redirects=allow_redirects)

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
            "Cookie": f"mc={self.session.cookies['mc']}; "
                      f"mrcu={self.session.cookies['mrcu']}; "
                      f"sdc={self.session.cookies['sdc']};"
        }
        self.session.post('https://auth-ac.my.com/auth', data=data, headers=headers)

        headers = {
            "Cookie": f"mc={self.session.cookies['mc']}; "
                      f"mrcu={self.session.cookies['mrcu']}; "
                      f"sdc={self.session.cookies['sdc']};",
            "Host": 'target-sandbox.my.com',
            "Referer": "https://target-sandbox.my.com/dashboard"
        }

        self.session.get('https://target-sandbox.my.com/csrf/', headers=headers)

    def create_campaign_special(self, name: str = "My campaign") -> json:
        """Создание кампании с типом 'Специальные возможности'"""

        campaign_name = name + ' ' + str(uuid.uuid1())
        headers = {
            "Cookie": f"mrcu={self.session.cookies['mrcu']}; "
                      f"csrftoken={self.session.cookies['csrftoken']}; "
                      f"mc={self.session.cookies['mc']}; "
                      f"sdc={self.session.cookies['sdc']};",
            "X-CSRFToken": f"{self.session.cookies['csrftoken']}",
        }

        data = {
            "name": f"{campaign_name}",
            "read_only": False,
            "conversion_funnel_id": None,
            "objective": "special",
            "targetings": {
                "sex": ["male", "female"],
                "age": {"age_list": [75], "expand": True},
                "pads": [784699, 784700],
            },
            "age_restrictions": None,
            "date_start": None,
            "date_end": None,
            "budget_limit_day": "600",
            "budget_limit": "1000",
            "mixing": "recommended",
            "price": "0.01",
            "max_price": "0",
            "package_id": 2266,  # задается автоматически при выборе кампании с типом "специальные возможности"
            "banners": [
                {
                    "textblocks": {"billboard_video": {"text": "Hello World"}},
                    "urls": {"primary": {"id": f"{self.get_url_for_campaign('https://www.google.com/')}"}},
                    "name": "",
                }
            ],
        }

        data = json.dumps(data)
        create_campaign_response = self._request(method='POST', location="api/v2/campaigns.json",
                                                 headers=headers, data=data, allow_redirects=False,
                                                 expected_status_code=200, jsonify=True)
        return create_campaign_response

    def check_campaign(self, create_campaign_response) -> bool:
        """Проверка существования кампании"""

        campaign_id = self.get_main_id(create_campaign_response)
        headers = {
            "Cookie": f"mrcu={self.session.cookies['mrcu']}; "
                      f"csrftoken={self.session.cookies['csrftoken']}; "
                      f"mc={self.session.cookies['mc']}; "
                      f"sdc={self.session.cookies['sdc']};",
        }

        params = 'sorting=-id&_status__in=active'
        response = self._request(method='GET', location="api/v2/campaigns.json", headers=headers,
                                 params=params, allow_redirects=False, expected_status_code=200)

        return str(campaign_id) in str(response)

    def get_main_id(self, create_campaign_response: json) -> int:
        """Получает id кампании из json полученного после создания кампании"""

        return create_campaign_response['id']

    def get_url_for_campaign(self, url:str) -> int:
        """Получает id рекламируемого url"""

        headers = {
            "Cookie": f"mrcu={self.session.cookies['mrcu']}; "
                      f"csrftoken={self.session.cookies['csrftoken']}; "
                      f"mc={self.session.cookies['mc']}; "
                      f"sdc={self.session.cookies['sdc']};",
        }

        params = 'url=' + url
        response = self._request(method='GET', location="api/v1/urls", headers=headers, params=params, expected_status_code=200, allow_redirects=True, jsonify=True)

        return response['id']

    def delete_campaign(self, create_campaign_response: json) -> Response:
        """Удаление кампании"""

        id = self.get_main_id(create_campaign_response)
        headers = {
            "Cookie": f"mrcu={self.session.cookies['mrcu']}; "
                      f"csrftoken={self.session.cookies['csrftoken']}; "
                      f"mc={self.session.cookies['mc']}; "
                      f"sdc={self.session.cookies['sdc']};",
            "X-CSRFToken": f"{self.session.cookies['csrftoken']}",
        }

        data = """{"status":"deleted"}"""

        response = self._request(method='POST', location=f'api/v2/campaigns/{id}.json',
                                 headers=headers, data=data, allow_redirects=False,
                                 expected_status_code=204, jsonify=False)
        return response

    def create_segment_apps_and_games_in_social_media(self, name: str = "My simple segment") -> json:
        """Создание сегмента с типом 'Приложения и игры в социальных сетях'"""

        segment_name = name + ' ' + str(uuid.uuid1())
        headers = {
            "Cookie": f"mrcu={self.session.cookies['mrcu']}; "
                      f"csrftoken={self.session.cookies['csrftoken']}; "
                      f"mc={self.session.cookies['mc']}; "
                      f"sdc={self.session.cookies['sdc']};",
            "X-CSRFToken": f"{self.session.cookies['csrftoken']}",
        }

        data = {
            "name": f"{segment_name}",
            "pass_condition": 1,
            "relations": [
                {
                    "object_type": "remarketing_player",
                    "params": {"type": "positive", "left": 365, "right": 0},
                }
            ],
            "logicType": "or",
        }

        data = json.dumps(data)
        response = self._request(method='POST', location='api/v2/remarketing/segments.json?',
                                 headers=headers, data=data, allow_redirects=False,
                                 expected_status_code=200, jsonify=True)
        return response

    def create_segment_groups_OK_and_VK(self, name: str = "My simple segment", data_source_id: int = None, groups: str = 'OK') -> Response:
        """Создание сегмента с типом 'группы OK и ВК'

        :param groups: 'OK' or 'VK"
        """
        segment_name = name + ' ' + str(uuid.uuid1())
        headers = {
            "Cookie": f"mrcu={self.session.cookies['mrcu']}; "
                      f"csrftoken={self.session.cookies['csrftoken']}; "
                      f"mc={self.session.cookies['mc']}; "
                      f"sdc={self.session.cookies['sdc']};",
            "X-CSRFToken": f"{self.session.cookies['csrftoken']}",
        }

        data = {
            "name": f"{segment_name}",
            "pass_condition": 1,
            "relations": [
                {
                    "object_type": "remarketing_group",
                    "params": {
                        "source_id": f"{self.get_data_source_source_id_by_id(data_source_id, groups)}",
                        "source_type": "group",
                        "type": "positive"
                    }
                }
            ],
            "logicType": "or"
        }

        data = json.dumps(data)
        response = self._request(method='POST', location='api/v2/remarketing/segments.json', headers=headers, data=data, expected_status_code=200)
        return response

    def check_segment(self, create_segment_response: json) -> bool:
        """Проверка существования сегмента"""

        segment_id = self.get_main_id(create_segment_response)
        headers = {
            "Cookie": f"mrcu={self.session.cookies['mrcu']}; "
                      f"csrftoken={self.session.cookies['csrftoken']}; "
                      f"mc={self.session.cookies['mc']}; "
                      f"sdc={self.session.cookies['sdc']};",
        }
        params = 'limit=50'
        response = self._request(method='GET', location='api/v2/remarketing/segments.json',
                                 headers=headers, params=params, allow_redirects=True,
                                 expected_status_code=200, jsonify=True)
        return str(segment_id) in str(response)

    def delete_segment(self, create_segment_response: json) -> Response:
        """Удаление сегмента"""

        segment_id = self.get_main_id(create_segment_response)
        headers = {
            "Cookie": f"mrcu={self.session.cookies['mrcu']}; "
                      f"csrftoken={self.session.cookies['csrftoken']}; "
                      f"mc={self.session.cookies['mc']}; "
                      f"sdc={self.session.cookies['sdc']};",
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

        headers = {
            "Cookie": f"mrcu={self.session.cookies['mrcu']}; "
                      f"csrftoken={self.session.cookies['csrftoken']}; "
                      f"mc={self.session.cookies['mc']}; "
                      f"sdc={self.session.cookies['sdc']};",
        }

        params = '_q=' + url

        if group == 'VK' or group == 'vk':
            response = self._request(method='GET', location='api/v2/vk_groups.json',
                                     headers=headers, params=params, expected_status_code=200,
                                     allow_redirects=False)
            return response['items'][random.randint(0, len(response['items']))]['id']
        elif group == 'OK' or group == 'ok':
            response = self._request(method='GET', location='api/v1/odkl_groups.json',
                                     headers=headers, params=params, expected_status_code=200,
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
            "Cookie": f"mrcu={self.session.cookies['mrcu']}; "
                      f"csrftoken={self.session.cookies['csrftoken']}; "
                      f"mc={self.session.cookies['mc']}; "
                      f"sdc={self.session.cookies['sdc']};",
            "X-CSRFToken": f"{self.session.cookies['csrftoken']}",
        }

        data = {"items": [{"object_id": f"{url_id}"}]}
        data = json.dumps(data)

        if group == 'VK' or group == 'vk':
            response = self._request(method='POST', location='api/v2/remarketing/vk_groups/bulk.json',
                                     headers=headers, data=data, expected_status_code=201)
        elif group == 'OK' or group == 'ok':
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
            "Cookie": f"mrcu={self.session.cookies['mrcu']}; "
                      f"csrftoken={self.session.cookies['csrftoken']}; "
                      f"mc={self.session.cookies['mc']}; "
                      f"sdc={self.session.cookies['sdc']};",
            "X-CSRFToken": f"{self.session.cookies['csrftoken']}",
        }

        if group == 'VK' or group == 'vk':
            response = self._request(method='DELETE', location=f'api/v2/remarketing/vk_groups/{id}.json',
                                     headers=headers, expected_status_code=204, jsonify=False)
            return response
        elif group == 'OK' or group == 'ok':
            response = self._request(method='DELETE', location=f'api/v2/remarketing/ok_groups/{id}.json',
                                     headers=headers, expected_status_code=204, jsonify=False)
            return response
        else:
            raise ApiClientException('Group must be equal to OK(ok) or VK(vk)')

    def check_groups_OK_and_VK_data_source(self, id: int, group: str = 'OK') -> bool:
        """Проверка наличия источника данных с типом 'группы OK и ВК'

        :param groups: 'OK' or 'VK"
        """

        headers = {
            "Cookie": f"mrcu={self.session.cookies['mrcu']}; "
                      f"csrftoken={self.session.cookies['csrftoken']}; "
                      f"mc={self.session.cookies['mc']}; "
                      f"sdc={self.session.cookies['sdc']};",
        }
        if group == 'VK' or group == 'vk':
            response = self._request(method='GET',
                                     location=f'api/v2/remarketing/vk_groups.json?fields=id&limit=50',
                                     headers=headers, expected_status_code=200)
            return str(id) in str(response)
        elif group == 'OK' or group == 'ok':
            response = self._request(method='GET',
                                     location=f'api/v2/remarketing/ok_groups.json?fields=id&limit=50',
                                     headers=headers, expected_status_code=200)
            return str(id) in str(response)
        else:
            raise ApiClientException('Group must be equal to OK(ok) or VK(vk)')

    def get_data_source_source_id_by_id(self, id: int, group: str = 'OK') -> int:
        """Получение source_id для источника данных с типом 'группы OK и ВК'

        :param groups: 'OK' or 'VK"
        """

        headers = {
            "Cookie": f"mrcu={self.session.cookies['mrcu']}; "
                      f"csrftoken={self.session.cookies['csrftoken']}; "
                      f"mc={self.session.cookies['mc']}; "
                      f"sdc={self.session.cookies['sdc']};",
        }

        if group == 'VK' or group == 'vk':
            response = self._request(method='GET',
                                     location='api/v2/remarketing/vk_groups.json',
                                     headers=headers, expected_status_code=200)
            for item in range(response['count']):
                if response['items'][item]['id'] == id:
                    source_id = response['items'][item]['object_id']
                    return source_id

        elif group == 'OK' or group == 'ok':
            response = self._request(method='GET',
                                     location='api/v2/remarketing/ok_groups.json',
                                     headers=headers, expected_status_code=200)
            for item in range(response['count']):
                if response['items'][item]['id'] == id:
                    source_id = response['items'][item]['object_id']
                    return source_id
        else:
            raise ApiClientException('Group must be equal to OK(ok) or VK(vk)')
