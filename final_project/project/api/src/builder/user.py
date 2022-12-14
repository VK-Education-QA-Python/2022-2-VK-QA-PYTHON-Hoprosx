
import uuid
from faker import Faker

from dataclasses import dataclass

faker_ru = Faker('ru_RU')
Faker.seed()



class Builder:

    @staticmethod
    def user(name=None, surname=None, middle_name=None,
             username=None, password=None, email=None):
        @dataclass
        class User:
            name: str
            surname: str
            middle_name: str
            username: str
            password: str
            email: str

        if name is None:
            name = faker_ru.first_name()

        if surname is None:
            surname = faker_ru.last_name()

        if middle_name is None:
            middle_name = faker_ru.middle_name()

        if username is None:
            username = faker_ru.user_name()

        if password is None:
            password = faker_ru.password()

        if email is None:
            email = faker_ru.email()

        return User(name=name, surname=surname, middle_name=middle_name,
                    username=(username + str(uuid.uuid4()))[0:16], password=password, email=email)

