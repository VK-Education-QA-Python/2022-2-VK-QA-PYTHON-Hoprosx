import json
from api.base.response import Response
from typing import Optional, Union
from urllib.parse import urljoin
import requests
from requests import Response
from api.src.builder.user import Builder

class ApiClientException(Exception):
    ...


class ResponseStatusCodeException(Exception):
    ...


class RespondErrorException(Exception):
    ...


class ApiClient:
    """
    Клиент для работы с апи
    """

    def __init__(self, base_url: str):
        self.base_url = base_url
        self.session = requests.session()
        self.builder = Builder()

    def _request(self, method: str, location: str, headers: Optional[dict] = None, data: str = None,
                 params: str = None, allow_redirects: bool = False,
                 expected_status_code: Union[int, list] = 200,
                 jsonify: bool = False) -> 'Response or json':

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

    def add_user(self, name: str=None, surname: str=None, middle_name: str=None,
                 username: str=None, password: str=None, email: str=None) -> Response:
        """Авторизация апи клиента"""

        headers = {"Content-Type": "application/json"}

        user = self.builder.user(name, surname, middle_name, username, password, email)
        data = {
            "name": f"{user.name}",
            "surname": f"{user.surname}",
            "middle_name": f"{user.middle_name}",
            "username": f"{user.username if username is None else username}",
            "password": f"{user.password}",
            "email": f"{user.email}"
        }

        json_data = json.dumps(data)

        response = self._request(method='POST', data=json_data, headers=headers,
                                 location='api/user', expected_status_code=[201, 400, 210])#210 убрать после фикса
        return response

    def delete_user(self, username: str) -> Response:
        """удаление юзера"""
        response = self._request(method='DELETE', location=f'api/user/{username}',
                                 expected_status_code=[204, 404])
        return response

    def change_password(self, username: str, password: str):
        """смена пароля"""
        headers = {"Content-Type": "application/json"}
        data = {
            "password": f"{password}"
        }
        json_data = json.dumps(data)
        response = self._request(method='PUT', headers=headers,
                                 location=f'api/user/{username}/change-password',
                                 data=json_data, expected_status_code=[200, 404, 400, 204])# 204 убрать после фикса
        return response

    def block_user(self, username: str):
        """блокировка юзера"""
        response = self._request(method='POST', location=f'api/user/{username}/block',
                                 expected_status_code=[200, 400, 404, 210]) #210убрать после фикса
        return response

    def unblock_user(self, username: str):
        """разблокировка юзера"""
        response = self._request(method='POST', location=f'api/user/{username}/accept',
                                 expected_status_code=[200, 400, 404])
        return response

    def status(self):
        """проверка статуса приложения"""
        response = self._request(method='GET', location='status', expected_status_code=200)
        return response

    def post_login(self):
        """логин"""
        data = {
            'username': 'Kirill',
            'password': 'Kirill',
            'sumbit': 'Login'
        }
        response = self._request(method='POST', location='/login', expected_status_code=[302], data=data, allow_redirects=False)
        return response
