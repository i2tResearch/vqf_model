import click
from celgis import Celgis
from models import Project


@click.command()
@click.option("--api_url", default="http://172.28.16.1:8080/api", help="Celgis Url")
@click.option("--username", help="Celgis username")
@click.option("--password", help="Celgis password")
def run_vqf(api_url, username, password):
    print("=================== ODISEO/VQ ===================")
    print("Using API endpoint", api_url)

    celgis = Celgis(api_url, username, password)
    if (not celgis.is_active()):
        print("Could not activate celgis connector. Check api_url and credentials")
        return
    
    print("Celgis connector is active")
    print("=================================================")
    print("Available projects:")

    json_projects = celgis.list_projects()
    projects = [Project.from_api_dict(j) for j in json_projects]
    for i, p in enumerate(projects):
        print("\t", i, p)

    print("=================================================")
    index = click.prompt("Enter the project index", type=int, default=0)
    selected = projects[index]
    print("Selected project:", projects[index].id)

    json_project = celgis.get_project(selected.id)
    project = Project.from_api_dict_detailed(json_project)
    
    print("=================================================")
    print("Project", project)
    for s in project.sites:
        print("\t", "Site", s)
        for a in s.antennas:
            print("\t", "\t", "Antenna", a)


if __name__ == '__main__':
    run_vqf()
