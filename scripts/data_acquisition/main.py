# setup_pudl_local.py
import time
import os
import sys

start_time = time.time()

# ============================
# CARGA DE LIBRERÍAS
# ============================

# Intenta importar kagglehub (útil si quieres descargar directamente desde Kaggle)
try:
    import kagglehub
    HAS_KAGGLEHUB = True
except ImportError:
    HAS_KAGGLEHUB = False
    print("Aviso: 'kagglehub' no está instalado. "
          "Puedes instalarlo con: pip install kagglehub")
    print("O bien, descarga el dataset manualmente y ajusta la ruta local.\n")

import seaborn as sns
import matplotlib
import matplotlib.pyplot as plt
import numpy as np      # Álgebra lineal
import pandas as pd     # Procesamiento de datos
import sqlalchemy as sa # Conexión a bases de datos SQL


def main():
    print(f"Python version: {sys.version}")
    print(f"{np.__version__=}")
    print(f"{pd.__version__=}")
    print(f"{sa.__version__=}")

    # ============================
    # DESCARGA / RUTA DEL DATASET
    # ============================

    # Opción 1: descargar con kagglehub si está disponible
    if HAS_KAGGLEHUB:
        print("Descargando dataset 'catalystcooperative/pudl-project' desde Kaggle...")
        catalystcooperative_pudl_project_path = kagglehub.dataset_download(
            'catalystcooperative/pudl-project'
        )
    else:
        # Opción 2: usar una ruta local donde ya tengas el dataset
        # 👉 AJUSTA ESTA RUTA A DONDE LO TENGAS EN TU PC
        catalystcooperative_pudl_project_path = os.path.join(
            os.path.dirname(__file__),
            "pudl-project"  # por ejemplo: carpeta local con el dataset
        )
        print(f"Usando ruta local (ajústala si es necesario): {catalystcooperative_pudl_project_path}")

    print('Data source import complete.')

    # ============================
    # LISTAR ARCHIVOS DEL DATASET
    # ============================

    if os.path.exists(catalystcooperative_pudl_project_path):
        print("\nArchivos encontrados en el dataset:\n")
        for dirname, _, filenames in os.walk(catalystcooperative_pudl_project_path):
            for filename in sorted(filenames):
                print(os.path.join(dirname, filename))
    else:
        print(f"\n⚠️ Directorio no encontrado: {catalystcooperative_pudl_project_path}")
        print("Verifica que la ruta sea correcta o que el dataset se haya descargado.\n")

    # ============================
    # CONFIGURACIÓN DE VISUALIZACIÓN
    # ============================

    sns.set()

    matplotlib.rcParams["figure.figsize"] = (16, 10)
    matplotlib.rcParams["figure.dpi"] = 150
    pd.set_option("display.max_columns", 200)
    pd.set_option("display.max_rows", 100)
    pd.set_option("display.max_colwidth", 1000)

    # (Ejemplo: crear un gráfico vacío solo para probar que funciona)
    # plt.plot([1, 2, 3], [1, 4, 9])
    # plt.title("Prueba de gráfico")
    # plt.show()

    end_time = time.time()
    print(f"\nTiempo de ejecución: {end_time - start_time:.2f} segundos")


if __name__ == "__main__":
    main()
