import requests


class Celgis:

    def __init__(self, api_url: str, username: str, password: str):
        self.api_url = api_url
        self.token: str = self._signin(username, password)
        self.headers: dict = {"Authorization": f"Bearer {self.token}"}

    def _signin(self, username, password) -> str:
        url = f"{self.api_url}/users/sign-in"
        payload = dict(username=username, password=password)
        response = requests.post(url, json=payload)
        token = response.headers.get("bearer")
        return token

    def is_active(self) -> bool:
        return self.token is not None

    def list_projects(self):
        url = f"{self.api_url}/projects"
        response = requests.get(url, headers=self.headers)
        return response.json()

    def get_project(self, id):
        url = f"{self.api_url}/projects/{id}"
        response = requests.get(url, headers=self.headers)
        return response.json()

    def get_project_signal_level(self, id, latitude, longitude):
        url = f"{self.api_url}/projects/{id}/signal-level"
        payload = dict(latitude=latitude, longitude=longitude)
        response = requests.get(url, json=payload, headers=self.headers)
        try:
            return response.json()
        except:
            return None

    def get_project_tiff(self, id):
        url = f"{self.api_url}/projects/{id}/tiff"
        response = requests.get(url, headers=self.headers)
        return response.content

    def get_transmitter_tiff(self, id):
        url = f"{self.api_url}/transmitters/{id}/tiff"
        response = requests.get(url, headers=self.headers)
        return response.content
