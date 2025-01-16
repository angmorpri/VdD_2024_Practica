# Práctica de Visualización de Datos 2024/25
## Script de preparación del juego de datos
### Ángel Moreno Prieto

## Objetivo
Este repositorio contiene el script `build_dataset.py`, que prepara el juego de
datos usado en la práctica a partir de los dos originales (cuyas fuentes pueden
encontrarse en `data/sources.txt`). Se fusionan ambos juegos de datos, y se
realiza un preprocesado sencillo, lo suficiente para poder preparar el
ejercicio de visualización.

## Consideraciones
Este código ha sido desarrollado en Python 3.12, por lo que es compatible con
ésa y superiores versiones de Python. También se han usado Pandas y NumPy con
versión 2.2.

## Instalación
### Poetry
Este proyecto utiliza [`poetry`](https://python-poetry.org/) como gestor de dependencias, a través de los archivos `pyproject.toml` y `poetry.lock`.

Una vez clonado el repositorio, se recomienda abrir una terminal y ejecutar:
```
    pip install poetry
    poetry install --no-root --without dev
```
De esta forma, se instalará `poetry`, y `poetry` gestionará todas las dependencias y los entornos virtuales.

Para ejecutar el programa, bastará entonces con realizar:
```
    poetry run python build_dataset.py
```

### Pip
Si **no** se quiere o puede usar `poetry`, bastará con instalar las dependencias, una vez clonado el repositorio, mediante:
```
    pip install -r requirements.txt
```
Y ejecutar el programa de la forma usual:
```
    python build_dataset.py
```

## Scripts
El script principal para generar el dataset final es `build_dataset.py`.

Se proporciona también otro script, `build_charts.py`, que ha sido utilizado
para generar reducciones de este dataset final, para poder generar las gráficas
pertinentes en la visualización.