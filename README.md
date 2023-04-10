# Proyecto VQF

Modelo en MiniZinc para el proyecto VQF.

## Notas del desarrollador

* Este repositorio se manejan en español porque así fue diseñado el modelo.
* Los nombres de las variables están como aparecen en el documento de definición del modelo.
* El desarrollo en Python sigue las mejores prácticas: pep8, variables en inglés, etc.

## Documentación y recursos

* El modelo está en el archivo [Formula Orquestadorv2_junio_2022.docx](./docs/Formula%20Orquestadorv2_junio_2022.docx)
* [MiniZinc Handbook](https://www.minizinc.org/doc-2.6.4/en/index.html)

## Minizinc + Python

* Instale Minizinc `sudo apt-get install minizinc`.
* Cree un entorno virtual de python `python3 -m venv env`.
* Active el entorno `source env/bin/activate`.
* Instale el paquete de python `pip install minizinc`.

## Python modules
* requests: HTTP client
* click: CLI properties manager