import click
import tifffile
from celgis import Celgis
from models import Project, OptimizationProperties


@click.command()
@click.option("--api_url", default="http://172.28.16.1:8080/api", help="Celgis Url")
@click.option("--username", help="Celgis username")
@click.option("--password", help="Celgis password")
def run_vqf(api_url, username, password):
    if username is None or password is None:
        username = click.prompt("Enter the username", type=str)
        password = click.prompt("Enter the password", type=str)

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
    project_id = projects[index].id
    print("Selected project:", projects[index].id)

    json_project = celgis.get_project(project_id)
    project = Project.from_api_dict_detailed(json_project)

    print("=================================================")
    print("Project", project)
    for s in project.sites:
        print("\t", "Site", s)
        for t in s.transmitters:
            print("\t", "\t", "Transmitter", t)

    print("=================================================")
    lat = 3.4228480292106775
    lon = -76.52822476196289
    json_signal_level = celgis.get_project_signal_level(project_id, lat, lon)
    print(f"Signal level at LAT {lat} and LON {lon}:", json_signal_level)

    print("=================================================")
    print("Retrieving the TIFF that contains the signal levels")
    tiff_bin = celgis.get_project_tiff(project_id)
    open("./tmp/tmp.tiff", "wb").write(tiff_bin)
    signal_levels_matrix = tifffile.imread("./tmp/tmp.tiff")
    optimization_properties = OptimizationProperties(signal_levels_matrix)

    print(
        f"Points with coverage (THR {project.threshold}):",
        optimization_properties.count_points_over_threshold(project.threshold),
        "of", optimization_properties.count_points())


if __name__ == '__main__':
    run_vqf()
