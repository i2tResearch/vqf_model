from vqf import Optimizer
from celgis import Celgis, CelgisClient
import click
import logging


logging.basicConfig(filename="./tmp/vqf_logs.log", level=logging.DEBUG)


@click.command()
@click.option("--api_url", default="http://172.28.16.1:8080/api", help="URL de Celgis")
@click.option("--username", help="Usuario Celgis")
@click.option("--password", help="Contraseña de Celgis")
@click.option("--maxpow", default=100.0, help="Máxima potencia permitida (dBm)")
@click.option("--randomize", default=False, help="Población aleatoria (falso = 1 por punto)")
@click.option("--minsol", default=10, help="Número mínimo de sectores que deberían poder atender el servicio")
def run_vqf(api_url, username, password, maxpow, randomize, minsol):

    print("=================== ODISEO/VQF ==================")
    print("Using API endpoint", api_url)

    celgis_client = CelgisClient(api_url, username, password)
    if (not celgis_client.is_active()):
        print("Could not activate celgis client. Check api_url and credentials")
        return
    celgis = Celgis(celgis_client)

    print("Celgis client is active")
    print("Randomize population:", randomize)

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
    for s in project.sites:
        print("Site", s)
        for t in s.transmitters:
            print("Transmitter", t)

    print("=================================================")
    print("Building optimizer... this will take some time while we calculate the distances")
    optimizer = Optimizer(
        project, "../../minizinc/models/vqf_okumura_hata.mzn", maxpow, randomize, minsol)
    optimizer.build_parameters()

    print("Running optimizer...")
    result = optimizer.optimize("gecode")

    print("=================================================")
    print(result)

    print("End")


def print_matrix(matrix):
    for r in matrix:
        rf = [str(i) if i != -9999.0 else "_" for i in r]
        print(rf)


if __name__ == '__main__':
    run_vqf()
