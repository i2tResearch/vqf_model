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
@click.option("--maxsolfactor", default=100, help="Máximo porcentaje de sectores que deberían poder atender el servicio (1-100)")
@click.option("--wpob", default=1, help="Peso del objetivo Cantidad de población atendida (0-100)")
@click.option("--wpts", default=1, help="Peso del objetivo Cantidad de puntos con cobertura superior al mínimo definido (0-100)")
def run_vqf(api_url, username, password, maxpow, randomize, minsol, maxsolfactor, wpob, wpts):

    print("=================== ODISEO/VQF ==================")
    print("Usando la URL de Celgis", api_url)

    celgis_client = CelgisClient(api_url, username, password)
    if (not celgis_client.is_active()):
        print("No fue posible activar Celgis. Revise la URL y las credenciales")
        return
    celgis = Celgis(celgis_client)

    print("Cliente Celgis activo")

    print("=================================================")
    print("Proyectos disponibles:")

    projects = celgis.list_projects()
    for i, p in enumerate(projects):
        print("\t", i, p)

    print("=================================================")
    index = click.prompt("Indique el número de proyecto", type=int, default=0)
    project_id = projects[index].id
    print("Proyecto seleccionado:", projects[index].id)

    project = celgis.load_project(project_id)

    print("=================================================")
    print("Proyecto", project)
    for s in project.sites:
        print("Sitio", s)
        for t in s.transmitters:
            print("Transmisor", t)

    print("=================================================")

    actual_minSol = max(minsol, 1)
    actual_maxSol = int(project.number_of_points() * maxsolfactor / 100)

    print("Población aleatoria:", randomize)
    print("Puntos disponibles:", project.number_of_points())
    print("minSol:", actual_minSol)
    print("maxSol:", actual_maxSol)
    print("W1 Peso Cantidad de población atendida:", wpob)
    print("W2 Peso Cantidad de puntos con cobertura:", wpts)

    print("=================================================")
    print("Construyendo el optimizador... Puede tomar unos minutos mientras se calculan las distancias")
    optimizer = Optimizer(
        project, "../../minizinc/models/vqf_okumura_hata.mzn", maxpow, randomize, actual_minSol, actual_maxSol, wpob, wpts)
    optimizer.build_parameters()

    print("Ejecutando el optimizador...")
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
