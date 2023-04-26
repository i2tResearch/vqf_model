import requests
import tifffile
from models import Project
import numpy as np
import rasterio


class Celgis:

    def __init__(self, client: "CelgisClient"):
        self.client: "CelgisClient" = client
        self.project = None

    def list_projects(self) -> list[Project]:
        json_projects = self.client.list_projects()
        projects = [Project.from_api_dict(j) for j in json_projects]
        return projects

    def load_project(self, id) -> Project:
        json_project = self.client.get_project(id)
        project = Project.from_api_dict_detailed(json_project)

        tiff_bin = self.client.get_project_tiff(id)
        tiff_path = "./tmp/project.tiff"
        open(tiff_path, "wb").write(tiff_bin)
        project.coverage_matrix = tifffile.imread(tiff_path)

        for s in project.sites:
            for t in s.transmitters:
                t_tiff_bin = self.client.get_transmitter_tiff(id, t.id)
                t_tiff_path = f"./tmp/transmitter_{t.id}.tiff"
                open(t_tiff_path, "wb").write(t_tiff_bin)
                t.coverage_matrix = tifffile.imread(t_tiff_path)

        d_tiff_bin = self.client.get_transmitter_distribution_tiff(id)
        d_tiff_path = f"./tmp/transmitter_distribution.tiff"
        open(d_tiff_path, "wb").write(d_tiff_bin)
        tiff_data = tifffile.imread(d_tiff_path)
        distribution_matrix = np.array(tiff_data).astype(int)
        project.distribution_matrix = distribution_matrix

        with rasterio.open(d_tiff_path) as dataset:
            transform = dataset.transform
            project.transformation_matrix = transform

        return project


class CelgisClient:

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

    def get_transmitter_tiff(self, id, tid):
        url = f"{self.api_url}/projects/{id}/transmitters/{tid}/tiff"
        response = requests.get(url, headers=self.headers)
        return response.content

    def get_transmitter_distribution_tiff(self, id):
        url = f"{self.api_url}/projects/{id}/transmitters/tiff"
        response = requests.get(url, headers=self.headers)
        return response.content
