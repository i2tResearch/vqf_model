import requests


class Celgis:

    def __init__(self, api_url: str, username: str, password: str):
        self.api_url = api_url
        self.token: str = self._signin(username, password)

    def _signin(self, username, password) -> str:
        url = f"{self.api_url}/users/sign-in"
        payload = dict(username=username, password=password)
        response = requests.post(url, json=payload)
        token = response.headers.get("bearer")
        return token

    def is_active(self) -> bool:
        return self.token is not None
