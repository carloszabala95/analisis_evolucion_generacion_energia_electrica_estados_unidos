import os
import time
from pathlib import Path
import pandas as pd
import dask.dataframe as dd
import geopandas as gpd
import sqlalchemy as sa
import matplotlib.pyplot as plt

# Consolidated, import fixes, and robust runtime behavior


def _load_pudl_project_path():
    """Buscar ruta PUDL: 1) PUDL_PROJECT_PATH env, 2) scripts/preprocessing/pudl_path.txt"""
    env = os.environ.get("PUDL_PROJECT_PATH")
    if env:
        return Path(env)
    repo_root = Path(__file__).resolve().parents[2]
    candidate = repo_root / "scripts" / "preprocessing" / "pudl_path.txt"
    if candidate.exists():
        text = candidate.read_text(encoding="utf-8").strip()
        if text:
            return Path(text)
    return None


def _maybe_start_dask_client():
    """Opcional: iniciar cliente Dask si USE_DASK_CLIENT=1"""
    if os.environ.get("USE_DASK_CLIENT", "0") == "1":
        try:
            from dask.distributed import Client, LocalCluster
            n_workers = int(os.environ.get("DASK_WORKERS", 2))
            cluster = LocalCluster(n_workers=n_workers)
            client = Client(cluster)
            print("Dask client iniciado:", client)
            return client
        except Exception as e:
            print("No se pudo iniciar Dask client:", e)
    return None


def _safe_df_diagnostics(ddf, sample_rows=5):
    """Imprimir diagnósticos ligeros sin computar todo el DataFrame."""
    print("Dask npartitions:", ddf.npartitions)
    print("Columnas:", list(ddf.columns))
    print("Dtypes:")
    print(ddf.dtypes)
    try:
        print("\nMuestra (head):")
        print(ddf.head(sample_rows))
    except Exception as e:
        print("No se pudo obtener head():", e)


def main():
    start = time.perf_counter()

    client = _maybe_start_dask_client()

    pudl_path = _load_pudl_project_path()
    if pudl_path is None:
        raise FileNotFoundError(
            "No se encontró la ruta al proyecto PUDL.\n"
            "Establece PUDL_PROJECT_PATH o crea scripts/preprocessing/pudl_path.txt (data_acquisition/main.py)."
        )

    pq_path = pudl_path / "pudl_parquet"
    if not pq_path.exists():
        raise FileNotFoundError(f"Directorio no existe: {pq_path}")

    parquet_file = pq_path / "out_vcerare__hourly_available_capacity_factor.parquet"
    if not parquet_file.exists():
        raise FileNotFoundError(f"Archivo parquet no encontrado: {parquet_file}")

    # Permitir proyección de columnas para reducir memoria: PUDL_COLUMNS="col1,col2"
    cols_env = os.environ.get("PUDL_COLUMNS")
    columns = [c.strip() for c in cols_env.split(",")] if cols_env else None
    read_kwargs = {"engine": "pyarrow"}
    if columns:
        read_kwargs["columns"] = columns

    ddf = dd.read_parquet(parquet_file, **read_kwargs)

    print("\nPrimeras filas (head):")
    try:
        print(ddf.head(10))
    except Exception as e:
        print("Error al mostrar head():", e)

    _safe_df_diagnostics(ddf, sample_rows=5)

    # Tamaño del archivo (informativo)
    try:
        size_mb = parquet_file.stat().st_size / (1024 * 1024)
        print(f"\nTamaño del archivo: {size_mb:.2f} MB")
    except Exception:
        pass

    # Evitar .compute() completo que consume memoria; calcular filas solo si necesario
    try:
        n_rows = ddf.shape[0].compute()
        print(f"Número de filas (estimado): {n_rows}")
    except Exception:
        print("Cálculo del número total de filas omitido (costoso).")

    print(f"Número de columnas: {ddf.shape[1]}")

    # Leer geometrías de condados desde SQLite (censusdp1tract.sqlite debe existir en pudl_path)
    census_sqlite = pudl_path / "censusdp1tract.sqlite"
    if not census_sqlite.exists():
        print(f"Advertencia: census SQLite no encontrado en {census_sqlite}. Se omite el mapa.")
    else:
        dp1_engine = sa.create_engine(f"sqlite:///{census_sqlite}")
        try:
            county_gdf = (
                gpd.read_postgis("county_2010census_dp1", con=dp1_engine, geom_col="shape")
                .rename(columns={"geoid10": "county_id_fips", "shape": "geometry"})
                .set_geometry("geometry")
                .set_crs("EPSG:4326")
                .loc[:, ["county_id_fips", "geometry"]]
                .assign(county_id_fips=lambda x: x["county_id_fips"].astype("string"))
            )

            conus_counties = county_gdf[
                ~county_gdf["county_id_fips"].str.startswith(("02", "15", "60", "66", "69", "72", "78"))
            ]

            fig, ax = plt.subplots(1, 1, figsize=(12, 8))
            conus_counties.plot(ax=ax)
            ax.set_xlim(-125, -66.5)
            ax.set_ylim(24, 50)
            ax.set_title("Condados EEUU Continental")
            ax.set_xlabel("Longitud")
            ax.set_ylabel("Latitud")
            plt.show()
        except Exception as e:
            print("Error al leer/plotear geometrías:", e)

    # Cargar usa_rare y filtrar condados de Colorado
    usa_rare_file = pq_path / "usa_rare.parquet"
    if usa_rare_file.exists():
        print("\nCargando usa_rare...")
        usa_rare = dd.read_parquet(usa_rare_file, engine="pyarrow")

        # Filtrar "CO" y county_id_fips no nulo (versión para Dask)
        colorado_rare = usa_rare[
            (usa_rare["state"] == "CO") &
            (~usa_rare["county_id_fips"].isna())
        ]

        # Mostrar primeras filas sin cargar todo
        print("\nPrimeras filas de colorado_rare:")
        try:
            print(colorado_rare.head(10))
        except Exception as e:
            print("Error al mostrar head() de colorado_rare:", e)

        # Merge geoespacial: Colorado
        t_merge_start = time.perf_counter()
        print("\n=== Merge geoespacial: Colorado ===")

        # Paso 1: Convertir subset Dask → Pandas (solo si es pequeño)
        try:
            est_rows = colorado_rare.shape[0].compute()
            print(f"Registros estimados en colorado_rare: {est_rows}")

            if est_rows > 500_000:
                print("Advertencia: El subconjunto es grande y podría exceder memoria al convertir a Pandas.")

            colorado_rare_df = colorado_rare.compute()
            print("Dask → Pandas: Conversión exitosa.")

        except Exception as e:
            print("Error al convertir colorado_rare a Pandas:", e)
            return

        # Paso 2: Merge geoespacial (merge regular de Pandas + GeoDataFrame)
        try:
            colorado_gdf = (
                county_gdf.merge(colorado_rare_df, on="county_id_fips", how="inner")
                .assign(county_id_fips=lambda x: x["county_id_fips"].astype("string"))
            )
            print("Merge geoespacial completado.")
        except Exception as e:
            print("Error durante el merge geoespacial:", e)
            return

        # Paso 3: Mostrar muestra
        try:
            print("\nMuestra de colorado_gdf:")
            print(colorado_gdf.head(10))
        except Exception as e:
            print("No se pudo mostrar la muestra:", e)

        t_merge_end = time.perf_counter()
        print(f"Tiempo de merge geoespacial: {t_merge_end - t_merge_start:.4f} segundos")

    else:
        print(f"Advertencia: no existe el archivo {usa_rare_file}. Se omite usa_rare.")

if __name__ == "__main__":
    main()

# Mover el bloque de generación de mapas dentro de main(), después de colorado_gdf
# Añade este bloque justo después de la creación de colorado_gdf en main()

# --- INICIO DEL BLOQUE PARA MAPA SOLAR/EÓLICO ---
# (Coloca este bloque después de colorado_gdf.head(10) y print(f"Tiempo de merge geoespacial: ..."))

            import time
            import pandas as pd
            import matplotlib.pyplot as plt

            t0 = time.perf_counter()

            print("\n=== Generación del mapa solar/eólico para Colorado ===")

            # -------------------------------------------------------------
            # Paso 1: Convertir timestamp y filtrar una hora específica
            # -------------------------------------------------------------
            try:
                ts = pd.to_datetime("2020-06-21 18:00:00")
                one_hour = colorado_gdf[colorado_gdf["datetime_utc"] == ts]
                print(f"Filas seleccionadas para {ts}: {len(one_hour)}")
            except Exception as e:
                print("Error filtrando el GeoDataFrame para la hora seleccionada:", e)
                raise

            # -------------------------------------------------------------
            # Paso 2: Crear figura con dos ejes
            # -------------------------------------------------------------
            fig, (solar_ax, wind_ax) = plt.subplots(1, 2, figsize=(18, 6))
            plt.tight_layout()

            # Valores compartidos para los mapas
            kwargs = {
                "legend": True,
                "vmin": 0,
                "vmax": 1,
            }

            # -------------------------------------------------------------
            # Paso 3: Mapa Solar (PV)
            # -------------------------------------------------------------
            try:
                one_hour.plot(
                    column="capacity_factor_solar_pv",
                    ax=solar_ax,
                    cmap="plasma",
                    **kwargs,
                )

                solar_ax.set_title(
                    f"Factor de Capacidad Energía Solar CO (Colorado)\n{ts} UTC"
                )
                solar_ax.set_xlabel("Longitud")
                solar_ax.set_ylabel("Latitud")

            except Exception as e:
                print("Error generando el mapa solar:", e)

            # -------------------------------------------------------------
            # Paso 4: Mapa Eólico (Onshore Wind)
            # -------------------------------------------------------------
            try:
                one_hour.plot(
                    column="capacity_factor_onshore_wind",
                    ax=wind_ax,
                    cmap="viridis",
                    **kwargs,
                )

                wind_ax.set_title(
                    f"Factor de Capacidad Energía Eólica CO (Colorado)\n{ts} UTC"
                )
                wind_ax.set_xlabel("Longitud")
                wind_ax.set_ylabel("Latitud")

            except Exception as e:
                print("Error generando el mapa eólico:", e)

            # -------------------------------------------------------------
            # Paso 5: Mostrar gráfico
            # -------------------------------------------------------------
            plt.show()

            t1 = time.perf_counter()
            print(f"Tiempo total del bloque: {t1 - t0:.4f} segundos")
# --- FIN DEL BLOQUE PARA MAPA SOLAR/EÓLICO ---