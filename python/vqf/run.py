import click
from celgis import Celgis
from models import Project


def build_project_list(projects) -> list:
    projects_list: list = []
    for i, p in enumerate(projects):
        projects_list.append((i, Project.from_api_dict(p)))
    return projects_list


@click.command()
@click.option("--api_url", default="http://172.28.16.1:8080/api", help="Celgis Url")
@click.option("--username", help="Celgis username")
@click.option("--password", help="Celgis password")
def run_vqf(api_url, username, password):
    print("=================== ODISEO/VQ ===================")
    print("Using API endpoint", api_url)
    celgis = Celgis(api_url, username, password)
    if (not celgis.is_active()):
        print("Could not activate celgis connector")
        return
    print("Celgis connector is active")
    print("=================================================")
    print("Available projects:")
    json_projects = celgis.list_projects()
    projects = build_project_list(json_projects)
    for p in projects:
        print("\t", p[0], str(p[1]))
    print("=================================================")
    index = click.prompt("Enter the project index", type=int, default=0)
    project = projects[index][1]
    print("Selected project:", project.id)


if __name__ == '__main__':
    run_vqf()
