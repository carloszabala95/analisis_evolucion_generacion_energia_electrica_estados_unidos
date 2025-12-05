import time
import pandas as pd
from pathlib import Path

# Iniciar medición de tiempo
start = time.perf_counter()

# --- Tu código aquí ---
# Ejemplo:
data_path = Path("data/archivo.csv")
if data_path.exists():
    df = pd.read_csv(data_path)
    print(df.head())
else:
    print("El archivo no existe:", data_path)

# Finalizar medición
end = time.perf_counter()

print(f"Tiempo de ejecución: {end - start:.4f} segundos")

import time
from pathlib import Path
import dask.dataframe as dd

def main():
    # Ruta al directorio con los archivos Parquet (ajusta según sea local o Kaggle)
    # Obtiene la ruta del proyecto PUDL desde una variable de entorno o usa un valor por defecto
    catalystcooperative_pudl_project_path = os.environ.get(
        "PUDL_PROJECT_PATH",
        "data/catalystcooperative_pudl_project"
    )
    pudl_path = Path(catalystcooperative_pudl_project_path)
    pq_path = pudl_path / "pudl_parquet"

    # Verificar que el directorio existe
    if not pq_path.exists():
        raise FileNotFoundError(f"El directorio no existe: {pq_path}")

    # Cargar archivo Parquet usando Dask
    usa_rare = dd.read_parquet(
        pq_path / "out_vcerare__hourly_available_capacity_factor.parquet",
        engine="pyarrow"
    )

    # Mostrar primeras filas
    print(usa_rare.head(10))


if __name__ == "__main__":
    start = time.perf_counter()
    main()
    end = time.perf_counter()
    print(f"Tiempo de ejecución: {end - start:.4f} segundos")

import time
import os
import dask.dataframe as dd

def main():
    # Asegúrate de que pq_path ya está definido previamente en tu script principal
    # Ejemplo:
    # from pathlib import Path
    # pq_path = Path(...)

    # Verificar existencia del archivo
    if not os.path.exists(pq_path):
        raise FileNotFoundError(f"El archivo o directorio no existe: {pq_path}")

    # Tamaño del archivo
    file_size_bytes = os.path.getsize(pq_path)
    file_size_mb = file_size_bytes / (1024 * 1024)
    print(f"Tamaño del archivo: {file_size_mb:.2f} MB")

    # Cargar usando Dask
    df_dd = dd.read_parquet(pq_path)

    # Número de filas y columnas
    n_rows = df_dd.shape[0].compute()
    n_cols = df_dd.shape[1]

    print(f"Número de filas: {n_rows}")
    print(f"Número de columnas: {n_cols}")


if __name__ == "__main__":
    start = time.perf_counter()
    main()
    end = time.perf_counter()
    print(f"Tiempo de ejecución: {end - start:.4f} segundos")

    import time

def main():
    # Se asume que usa_rare ya fue cargado previamente como DataFrame de pandas.
    # Ejemplo:
    # usa_rare = df_dd.compute()

    # Mostrar información del DataFrame
    usa_rare.info()


if __name__ == "__main__":
    start = time.perf_counter()
    main()
    end = time.perf_counter()
    print(f"Tiempo de ejecución: {end - start:.4f} segundos")

    import time
import geopandas as gpd
import sqlalchemy as sa
import matplotlib
import matplotlib.pyplot as plt

def main():
    # Aquí irán las operaciones que realices con GeoPandas, SQLAlchemy y Matplotlib.
    # Ejemplo:
    # gdf = gpd.read_file("archivo.shp")
    # gdf.plot()
    # plt.show()
    pass


if __name__ == "__main__":
    start = time.perf_counter()
    main()
    end = time.perf_counter()
    print(f"Tiempo de ejecución: {end - start:.4f} segundos")

    import time
import geopandas as gpd
import sqlalchemy as sa
import matplotlib.pyplot as plt

def main():
    # Crear el engine de SQLAlchemy para los datos espaciales del censo
    dp1_engine = sa.create_engine(
        "sqlite:///" + str((pudl_path / "censusdp1tract.sqlite").absolute())
    )

    # Leer geometrías de condados desde la base de datos SQLite
    county_gdf = (
        gpd.read_postgis(
            "county_2010census_dp1",
            con=dp1_engine,
            geom_col="shape"
        )
        .rename(columns={"geoid10": "county_id_fips", "shape": "geometry"})
        .set_geometry("geometry")
        .set_crs("EPSG:4326")
        .loc[:, ["county_id_fips", "geometry"]]
        .assign(county_id_fips=lambda x: x["county_id_fips"].astype("string"))
    )

    # Filtrar Alaska, Hawaii y territorios
    conus_counties = county_gdf[
        ~county_gdf["county_id_fips"].str.startswith(
            ("02", "15", "60", "66", "69", "72", "78")
        )
    ]

    # Graficar mapa continental de EE.UU.
    fig, ax = plt.subplots(1, 1, figsize=(12, 8))
    conus_counties.plot(ax=ax)

    # Limitar la vista al territorio continental
    ax.set_xlim(-125, -66.5)
    ax.set_ylim(24, 50)

    # Agregar títulos y etiquetas
    ax.set_title('Condados EEUU Continental')
    ax.set_xlabel('Longitud')
    ax.set_ylabel('Latitud')

    # Mostrar gráfica
    plt.show()


if __name__ == "__main__":
    start = time.perf_counter()
    main()
    end = time.perf_counter()
    print(f"Tiempo de ejecución: {end - start:.4f} segundos")
