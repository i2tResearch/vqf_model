import click
from celgis import Celgis, CelgisClient


@click.command()
@click.option("--api_url", default="http://172.28.16.1:8080/api", help="Celgis Url")
@click.option("--username", help="Celgis username")
@click.option("--password", help="Celgis password")
def run_vqf(api_url, username, password):
    if username is None or password is None:
        username = click.prompt("Enter the username", type=str)
        password = click.prompt("Enter the password", type=str)

    print("=================== ODISEO/VQF ==================")
    print("Using API endpoint", api_url)

    celgis_client = CelgisClient(api_url, username, password)
    if (not celgis_client.is_active()):
        print("Could not activate celgis client. Check api_url and credentials")
        return
    celgis = Celgis(celgis_client)
    
    print("Celgis client is active")

    print("=================================================")
    print("Available projects:")

    projects = celgis.list_projects()
    for i, p in enumerate(projects):
        print("\t", i, p)

    print("=================================================")
    index = click.prompt("Enter the project index", type=int, default=0)
    project_id = projects[index].id
    print("Selected project:", projects[index].id)

    project = celgis.load_project(project_id)

    print("=================================================")
    print("Project", project)
    [print(pc) for pc in project.coverage_matrix]
    for s in project.sites:
        print("Site", s)
        for t in s.transmitters:
            print("Transmitter", t)
            [print(tc) for tc in t.coverage_matrix]

    print("End")


if __name__ == '__main__':
    run_vqf()
