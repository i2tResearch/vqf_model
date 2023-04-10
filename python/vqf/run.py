import click
from celgis import Celgis


@click.command()
@click.option("--api_url", default="http://172.28.16.1:8080/api", help="Celgis Url")
@click.option("--username", help="Celgis username")
@click.option("--password", help="Celgis password")
def run_vqf(api_url, username, password):
    print("Using API endpoint", api_url)
    celgis = Celgis(api_url, username, password)
    if (not celgis.is_active()):
        print("Could not activate celgis connector")
        return
    print("Celgis connector is active")


if __name__ == '__main__':
    run_vqf()
