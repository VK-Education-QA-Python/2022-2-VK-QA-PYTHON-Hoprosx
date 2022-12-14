from pydantic.error_wrappers import ValidationError


class Response:
    """
    Класс для валидации данных.
    """

    def __init__(self, response):
        self.response = response
        try:
            self.response_json = response.json()
        except Exception:
            self.response_json = None
        self.response_status = response.status_code
        self.parsed_object = None

    def validate(self, schema):
        try:
            if isinstance(self.response_json, list):
                for item in self.response_json:
                    parsed_object = schema.parse_obj(item)
                    self.parsed_object = parsed_object
            else:
                schema.parse_obj(self.response_json)
        except ValidationError:
            raise AssertionError(
                "Could not map received object to pydantic schema"
            )

    def assert_status_code(self, status_code):
        """
        Метод для валидации статус кода.
        """
        if isinstance(status_code, list):
            assert self.response_status in status_code, self
        else:
            assert self.response_status == status_code, self
        return self

    def get_parsed_object(self):
        return self.parsed_object

    def __str__(self):
        """
        Метод отвечает за строковое представление объекта.
        """
        return \
            f"\nStatus code: {self.response_status} \n" \
            f"Requested url: {self.response.url} \n" \
            f"Response body: {self.response_json}"
