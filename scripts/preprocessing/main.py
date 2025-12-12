##Análisis de Datos de Potencial de Generación de Energías Renovables en Estados Unidos (Casos de Estudio: Eólica y Solar):
import time
import pandas as pd
from pathlib import Path

# Iniciar medición de tiempo
start = time.perf_counter()

# --- Tu código aquí ---
# Ejemplo: verificación simple de existencia de archivo
data_path = Path("data/archivo.csv")
if data_path.exists():
    df = pd.read_csv(data_path)
    print(df.head())
else:
    print("El archivo no existe:", data_path)

# Finalizar medición
end = time.perf_counter()

print(f"Tiempo total de ejecución: {end - start:.4f} segundos")

#import time
from pathlib import Path
import os
import dask.dataframe as dd

# Iniciar medición de tiempo
start = time.perf_counter()

# Ruta al directorio con los archivos Parquet (ajusta si es Kaggle o local)
# Intenta leer la ruta desde la variable de entorno PUDL_DATASET_PATH; si no está definida, usa una ruta por defecto local.
pudl_path_str = os.environ.get("PUDL_DATASET_PATH", "data/catalystcooperative_pudl_project")
pudl_path = Path(pudl_path_str)
pq_path = pudl_path / "pudl_parquet"

# Verificación de existencia del directorio parquet
if not pq_path.exists():
    raise FileNotFoundError(
        f"No se encontró el directorio: {pq_path}. "
        "Define la variable de entorno PUDL_DATASET_PATH o verifica la ruta local."
    )

# Cargar el archivo parquet usando Dask
usa_rare = dd.read_parquet(
    pq_path / "out_vcerare__hourly_available_capacity_factor.parquet",
    engine="pyarrow"
)

# Mostrar las primeras filas (esto ejecuta una pequeña parte del dataframe)
print(usa_rare.head(10))

# Finalizar medición de tiempo
end = time.perf_counter()

print(f"Tiempo total de ejecución: {end - start:.4f} segundos")

import time
import os
import dask.dataframe as dd

# Iniciar medición de tiempo
start = time.perf_counter()

# Tamaño total del archivo/directory parquet
file_size_bytes = os.path.getsize(pq_path)
file_size_mb = file_size_bytes / (1024 * 1024)
print(f"Tamaño del archivo: {file_size_mb:.2f} MB")

# Cargar parquet con Dask
df_dd = dd.read_parquet(pq_path)

# Obtener número de filas y columnas
n_rows = df_dd.shape[0].compute()   # Ejecuta el cómputo de filas
n_cols = df_dd.shape[1]             # Columnas disponibles sin computar

print(f"Número de filas: {n_rows}")
print(f"Número de columnas: {n_cols}")

# Finalizar medición
end = time.perf_counter()
print(f"Tiempo total de ejecución: {end - start:.4f} segundos")

import time

# Iniciar medición de tiempo
start = time.perf_counter()

# Tamaño y estructura del DataFrame Pandas intermediario
usa_rare.info()

# Finalizar medición de tiempo
end = time.perf_counter()
print(f"Tiempo total de ejecución: {end - start:.4f} segundos")

import time
import geopandas as gpd
import sqlalchemy as sa
import matplotlib
import pandas as pd

# Se asume que plants_ferc1 YA está cargado.
# Si deseas cargarlo aquí nuevamente, puedo entregarte la versión integrada.

# ============================
# MEDIR TIEMPO DE EJECUCIÓN
# ============================

start_time = time.time()

# ============================
# Filtrado y preparación de datos para la planta Comanche
# ============================

comanche_ferc1 = (
    plants_ferc1.loc[
        plants_ferc1["plant_id_pudl"] == 126,
        [
            "report_year",
            "plant_id_ferc1",
            "plant_name_ferc1",
            "plant_id_pudl",
            "capacity_mw",
            "net_generation_mwh",
            "capacity_factor",
            "capex_annual_addition",
            "capex_annual_per_mw",
            "capex_annual_per_mwh",
            "opex_total_nonfuel",
            "opex_per_mwh",
            "opex_nonfuel_per_mwh",
            "opex_fuel_per_mwh",
        ]
    ]
    .assign(report_date=lambda x: pd.to_datetime(x["report_year"].astype("string")))
)

# Guardar CSV de muestra
output_dir = Path("data")
output_dir.mkdir(exist_ok=True)
comanche_ferc1.to_csv(output_dir / "pudl_sample.csv", index=False)

end_time = time.time()

# ============================
# RESULTADO
# ============================

print(f"\nTiempo de ejecución: {end_time - start_time:.2f} segundos\n")

print("Datos filtrados para la planta Comanche (plant_id_pudl = 126):\n")
print(comanche_ferc1)

#Aumento de Costos y Tiempo de Inactividad#

import matplotlib.pyplot as plt

# Iniciar medición de tiempo
start = time.perf_counter()

# --- Aquí iría tu código que usa estas librerías ---

# Finalizar medición de tiempo
end = time.perf_counter()
print(f"Tiempo total de ejecución: {end - start:.4f} segundos")

import time
import geopandas as gpd
import sqlalchemy as sa
import matplotlib.pyplot as plt

# Iniciar medición de tiempo
start = time.perf_counter()

# Create the SQLAlchemy engine connecting to census spatial data
dp1_engine = sa.create_engine(
    "sqlite:///" + str((pudl_path / "censusdp1tract.sqlite").absolute())
)

# Read the county geometries from the database
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

# Filter out Alaska, Hawaii, and other territories
conus_counties = county_gdf[
    ~county_gdf["county_id_fips"].str.startswith(("02", "15", "60", "66", "69", "72", "78"))
]

# Plot the continental US with a larger figure size
fig, ax = plt.subplots(1, 1, figsize=(12, 8))
conus_counties.plot(ax=ax)

# Set axis limits to focus on the continental US
ax.set_xlim(-125, -66.5)
ax.set_ylim(24, 50)

# Add title and labels
ax.set_title('Condados EEUU Continental')
ax.set_xlabel('Longitud')
ax.set_ylabel('Latitud')

# Show the plot
plt.show()

# Finalizar medición de tiempo
end = time.perf_counter()
print(f"Tiempo total de ejecución: {end - start:.4f} segundos")

import time

# Iniciar medición de tiempo
start = time.perf_counter()

# Filtrar filas donde el estado es "CO" y eliminar valores nulos en county_id_fips
colorado_rare = usa_rare[
    (usa_rare.state == "CO") &
    (~usa_rare.county_id_fips.isna())
]

# Mostrar muestra sin cargar todo el dataset
print(colorado_rare.head(10))

# Finalizar medición de tiempo
end = time.perf_counter()
print(f"Tiempo total de ejecución: {end - start:.4f} segundos")

import time
import geopandas as gpd

# Iniciar medición de tiempo
start = time.perf_counter()

# Paso 1: Computar el subconjunto Dask → pandas (solo si es razonablemente pequeño)
colorado_rare_df = colorado_rare.compute()

# Paso 2: Realizar el merge geoespacial con pandas
colorado_gdf = (
    county_gdf.merge(colorado_rare_df, on="county_id_fips")
    .assign(county_id_fips=lambda x: x["county_id_fips"].astype("string"))
)

# Paso 3: Ver una muestra
print(colorado_gdf.head(10))

# Finalizar medición
end = time.perf_counter()
print(f"Tiempo total de ejecución: {end - start:.4f} segundos")

import time
import pandas as pd
import matplotlib.pyplot as plt

# Iniciar medición de tiempo
start = time.perf_counter()

# Timestamp objetivo
ts = pd.to_datetime("2020-06-21 18:00:00")

# Filtrar datos para la hora específica
one_hour = colorado_gdf[colorado_gdf.datetime_utc == ts]

# Crear figuras para solar y eólica
fig, (solar_ax, wind_ax) = plt.subplots(1, 2, figsize=(18, 6))

plt.tight_layout()

# Configuración común para los mapas
kwargs = {
    "legend": True,
    "vmin": 0,
    "vmax": 1,
}

# --- Mapa solar ---
one_hour.plot(
    column="capacity_factor_solar_pv",
    ax=solar_ax,
    cmap="plasma",
    **kwargs,
)

solar_ax.set_title(f"Factor de Capacidad Energía Solar CO (Colorado)\n{ts} UTC")
solar_ax.set_xlabel("Longitud")
solar_ax.set_ylabel("Latitud")

# --- Mapa eólico ---
one_hour.plot(
    column="capacity_factor_onshore_wind",
    ax=wind_ax,
    cmap="viridis",
    **kwargs,
)

wind_ax.set_title(f"Factor de Capacidad Energía Eólica CO (Colorado)\n{ts} UTC")
wind_ax.set_xlabel("Longitud")
wind_ax.set_ylabel("Latitud")

# Mostrar figuras
plt.show()

# Finalizar medición
end = time.perf_counter()
print(f"Tiempo total de ejecución: {end - start:.4f} segundos")

import time
import matplotlib.animation as animation
from tqdm import tqdm
# IPython.display may not be available in non-notebook environments; import is handled later with a fallback.
import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt

# Iniciar medición de tiempo
start = time.perf_counter()

# --- Función Corregida (no necesita cambios) ---
def animate_capacity_factor_fixed(
    geodata: gpd.GeoDataFrame,
    column: str,
    prefix: str,
    colormap: str = 'viridis',
    frame_duration_ms: int = 500
) -> animation.FuncAnimation:
    """
    Crea una gráfica animada de una columna de factor de capacidad.
    Esta versión devuelve el objeto de animación.
    """
    # Crear la figura y el eje para la gráfica
    fig, ax = plt.subplots(1, 1, figsize=(8, 6))
    ax.axis('off')
    plt.tight_layout()

    sm = plt.cm.ScalarMappable(cmap=colormap, norm=plt.Normalize(vmin=0, vmax=1))
    sm._A = []  # Hack para que funcione sin datos
    cbar = fig.colorbar(sm, ax=ax, orientation='horizontal', fraction=0.036, pad=0.04)
    cbar.set_label("Factor de Capacidad Eólico")

    # Barra de progreso
    unique_times = sorted(geodata.datetime_utc.unique())
    num_frames = len(unique_times)

    # Función para actualizar la gráfica en cada fotograma
    def update(frame):
        ax.clear()
        ax.axis('off')
        current_time = unique_times[frame]
        current_data = geodata[geodata.datetime_utc == current_time]

        current_data.plot(
            column=column,
            cmap=colormap,
            linewidth=0.1,
            ax=ax,
            edgecolor='0.1',
            vmin=0,
            vmax=1,
            legend=False
        )
        ax.set_title(
            f'{column.replace("_", " ").title()} '
            f'{pd.to_datetime(current_time).strftime("%Y-%m-%d %H:%M")} UTC',
            fontdict={'fontsize': 15}
        )

    # Crear la animación
    anim = animation.FuncAnimation(fig, update, frames=num_frames, repeat=False)

    # Guardar el video con barra de progreso
    with tqdm(total=num_frames, desc="Guardando Video") as pbar:
        def progress_callback(current_frame, total_frames):
            pbar.update(1)

        writer = animation.FFMpegWriter(fps=1000 / frame_duration_ms)
        anim.save(f"{prefix}{column}.mp4", writer=writer, progress_callback=progress_callback)

    plt.close(fig)  # Evitar mostrar la imagen estática en VS Code

    return anim  # ¡Importante! devolvemos la animación.


# Finalizar medición de tiempo
end = time.perf_counter()
print(f"Tiempo total de ejecución: {end - start:.4f} segundos")

import time

# Iniciar medición de tiempo
start = time.perf_counter()

# Filtrar filas donde el estado es Texas ("TX")
texas_rare = usa_rare.loc[usa_rare.state == "TX"]

# Finalizar medición
end = time.perf_counter()
print(f"Tiempo total de ejecución: {end - start:.4f} segundos")

import time
import pandas as pd

# Iniciar medición de tiempo
start = time.perf_counter()

# --- Celda para llamar a la animación y mostrarla (CORREGIDA) ---

# 1. Rango de tiempo para la animación (puedes ajustarlo)
start_time = "2020-06-21 00:00:00"
end_time = "2020-06-22 00:00:00"  # Animación de 1 día

# 2. Filtrar los datos de Texas para el rango de tiempo
texas_rare_subset_dd = usa_rare[
    (usa_rare.state == "TX") &
    (~usa_rare.county_id_fips.isna()) &
    (usa_rare.datetime_utc.between(start_time, end_time))
]

# 3. Convertir el subconjunto de Dask a un DataFrame de pandas
texas_rare_subset_df = texas_rare_subset_dd.compute()

# 4. Asegurar que los tipos de datos coincidan para la unión
texas_rare_subset_df["county_id_fips"] = texas_rare_subset_df["county_id_fips"].astype("string")
county_gdf["county_id_fips"] = county_gdf["county_id_fips"].astype("string")

# 5. Unir los datos de energía con las geometrías de los condados
texas_gdf_subset = county_gdf.merge(texas_rare_subset_df, on="county_id_fips")

# 6. Llamar a la función CORREGIDA de animación
anim = animate_capacity_factor_fixed(
    geodata=texas_gdf_subset,
    column="capacity_factor_onshore_wind",
    prefix="texas_",
    colormap="viridis",
    frame_duration_ms=500  # 500 ms por fotograma
)

# 7. Mostrar el video (solo funciona dentro de notebooks)
# from IPython.display import HTML
# HTML(anim.to_html5_video())

print("Animación generada exitosamente: archivo MP4 guardado.")

# Finalizar medición
end = time.perf_counter()
print(f'Tiempo total de ejecución: {end - start:.4f} segundos')

import pandas as pd
import importlib.util

# Dynamically check for IPython.display to avoid static import errors in non-notebook environments
HTML = None
try:
    if importlib.util.find_spec("IPython.display") is not None:
        from IPython.display import HTML  # type: ignore
    else:
        raise ImportError("IPython.display not available")
except Exception:
    # Fallback stub for environments without IPython (e.g., plain python execution)
    class _HTMLStub:
        def __init__(self, content):
            self.content = content
        def _repr_html_(self):
            return self.content
        def to_html5_video(self):
            return self.content
        def __str__(self):
            return self.content
    def HTML(content):
        return _HTMLStub(content)

# Llamar a la función CORREGIDA (sin start y end)
anim = animate_capacity_factor_fixed(
    geodata=texas_gdf_subset,
    column="capacity_factor_solar_pv",
    prefix="texas_",
    colormap="plasma",
    frame_duration_ms=500  # 500ms por fotograma (2 FPS)
)

# Mostrar el video (solo funciona dentro de ambientes tipo Jupyter)
html_video = anim.to_html5_video()
print("Animación generada. Si estás en Jupyter, mostrará el video.")

# Si estás en VS Code-Jupyter, se mostrará:
HTML(html_video)

# Si estás en un archivo .py tradicional y quieres guardarlo como HTML:
with open("animacion_texas_solar.html", "w") as f:
    f.write(html_video)

print("Archivo generado: animacion_texas_solar.html")

import time

# Iniciar medición del tiempo (equivalente a %%time)
start = time.perf_counter()

# Select a county by 5-digit county FIPS ID
hist_county_id_fips = "08075"  # Logan County, CO. You can replace it with any 5-digit FIPS code
hist_gen_type = "onshore_wind"  # Options: solar_pv, onshore_wind, offshore_wind

# Fin de la medición
end = time.perf_counter()
print(f"Tiempo de ejecución: {end - start:.4f} segundos")

import time

# Iniciar temporizador (equivalente a %%time)
start = time.perf_counter()

# Filtrar el DataFrame por county_id_fips
plot_df = usa_rare.loc[usa_rare["county_id_fips"] == hist_county_id_fips]

# Finalizar temporizador
end = time.perf_counter()
print(f"Tiempo de ejecución: {end - start:.4f} segundos")

import numpy as np
import matplotlib.pyplot as plt

# 1. Crear el histograma
fig, ax = plt.subplots(1, 1, figsize=(12, 6))
plt.hist(plot_df[f"capacity_factor_{hist_gen_type}"], bins=100, range=(0, 1))

# 2. Obtener información del condado
county_info = plot_df[plot_df["county_id_fips"] == hist_county_id_fips]
county_name = county_info.place_name.unique()[0]
state_name = county_info.state.unique()[0]

# 3. Obtener el máximo valor y convertirlo a float de forma segura
max_cf_raw = plot_df[f"capacity_factor_{hist_gen_type}"].max()

# Manejo robusto del tipo
try:
    max_cf = round(float(max_cf_raw), 2)
except (TypeError, ValueError):
    max_cf = "N/A"

# 4. Título y etiquetas
plt.xlabel("Capacity Factor")
plt.ylabel("Hours")
plt.grid()
plt.show()


import time

# Iniciar medición de tiempo (equivalente a %%time)
start = time.perf_counter()

state = "TX"  # Ingresa el estado deseado
annual_year = 2023  # Ingresa el año deseado

# Finalizar medición de tiempo
end = time.perf_counter()
print(f"Tiempo de ejecución: {end - start:.6f} segundos")


import time
import dask.dataframe as dd

# -------------------------------------------------------------------
# (Opcional) Medición de tiempo equivalente a %%time
start = time.perf_counter()
# -------------------------------------------------------------------

# 1. Definir las columnas relevantes
cap_fac_cols = ['solar_pv', 'onshore_wind', 'offshore_wind']

# 2. Crear una copia segura del DataFrame
rare_df_copy = usa_rare.copy()

# 3. Renombrar las columnas para eliminar el prefijo 'capacity_factor_'
new_columns = {
    col: col.replace('capacity_factor_', '')
    for col in rare_df_copy.columns if col.startswith('capacity_factor_')
}
rare_df_copy = rare_df_copy.rename(columns=new_columns)

# 4. Filtrar por año y estado (usa variables: annual_year, state)
rare_year_state_subset = rare_df_copy[
    (rare_df_copy["report_year"] == annual_year) &
    (rare_df_copy["state"] == state)
]

# 5. Agrupar por las columnas deseadas y calcular media y varianza
grouped = rare_year_state_subset.groupby(
    ["report_year", "state", "place_name", "county_id_fips"]
)

# 6. Calcular estadísticas para cada columna de capacidad
means = grouped[cap_fac_cols].mean().rename(
    columns={col: f"{col}_mean" for col in cap_fac_cols}
)

vars_ = grouped[cap_fac_cols].var().rename(
    columns={col: f"{col}_var" for col in cap_fac_cols}
)

# 7. Combinar los resultados
stats_combined = dd.concat([means, vars_], axis=1)

# 8. Convertir a pandas si el resultado es pequeño o se va a visualizar
stats_combined_df = stats_combined.compute()

# 9. Reorganizar a formato largo (opcional)
stats_long = stats_combined_df.reset_index().melt(
    id_vars=["report_year", "state", "place_name", "county_id_fips"],
    var_name="stat_type",
    value_name="value"
)

# 10. Separar 'stat_type' en 'gen_type' y 'metric' (mean o var)
stats_long[['gen_type', 'metric']] = stats_long["stat_type"].str.extract(
    r'(\w+)_(mean|var)'
)

stats_long = stats_long.drop(columns="stat_type")

# 11. Pivotear para obtener columnas más limpias
rare_year_state_subset_final = stats_long.pivot_table(
    index=["report_year", "state", "place_name", "county_id_fips", "gen_type"],
    columns="metric",
    values="value"
).reset_index()

# 12. Renombrar columnas finales
rare_year_state_subset_final = rare_year_state_subset_final.rename(columns={
    "mean": "average_capacity_factor",
    "var": "average_variance"
})

# -------------------------------------------------------------------
# Finalizar temporizador
end = time.perf_counter()
print(f"Tiempo de ejecución: {end - start:.4f} segundos")
# -------------------------------------------------------------------

import time
import altair as alt

# ---------------------------------------------------------------
# (Opcional) Medición equivalente a %%time
start = time.perf_counter()
# ---------------------------------------------------------------

# Define the data source for the chart
source = rare_year_state_subset_final

# Set the color scheme for the chart
color = alt.Color('gen_type:N').scale(
    domain=['solar_pv', 'onshore_wind', 'offshore_wind'],
    range=['#e7ba52', '#69b373', '#aec7e8']
)

# Create selections:
# - brush for the top panel
# - click selection for the bottom panel
brush = alt.selection_interval(encodings=['x'])
click = alt.selection_point(encodings=['color'])

# Top panel: scatter plot variance vs capacity factor
points = (
    alt.Chart()
    .mark_point()
    .encode(
        alt.X('average_variance:Q', title='Varianza Anual'),
        alt.Y('average_capacity_factor:Q', title='Factor de Capacidad Promedio Anual')
            .scale(domain=[0, 1]),
        color=alt.condition(brush, color, alt.value('lightgray')),
        tooltip=[
            alt.Tooltip('county_or_lake_name:N', title='Nombre del Condado'),
            alt.Tooltip('county_id_fips:N', title='FIPS ID'),
            alt.Tooltip(
                'average_capacity_factor:Q',
                title='Factor de Capacidad Promedio Anual',
                format='.2f'
            ),
            alt.Tooltip(
                'average_variance:Q',
                title='Varianza Promedio Anual',
                format='.2f'
            ),
        ]
    )
    .properties(
        width=1000,
        height=550
    )
    .add_params(brush)
    .transform_filter(click)
)

# Bottom panel: bar chart of average capacity factor by generation type
bars = (
    alt.Chart()
    .mark_bar()
    .encode(
        x=alt.X(
            'average(average_capacity_factor):Q',
            title='Factor de capacidad promedio (excluyendo valores atípicos)'
        ),
        y=alt.Y('gen_type:N', title='Tipo de Generación'),
        color=alt.condition(click, color, alt.value('lightgray')),
        tooltip=[
            alt.Tooltip('gen_type:N', title='Tipo de Generación'),
            alt.Tooltip(
                'average(average_capacity_factor):Q',
                title='Factor de Capacidad Promedio',
                format='.2f'
            )
        ]
    )
    .transform_filter(
        (alt.datum.average_capacity_factor > 0) & brush
    )
    .properties(width=1000)
    .add_params(click)
)

chart = alt.vconcat(
    points,
    bars,
    data=source,
    title=f"Factor de Capacidad Promedio vs. Varianza por Condados en {state} en {annual_year}"
).configure_title(
    fontSize=24,
    anchor="middle",
    dy=-10,
).configure_axis(
    titleFontSize=16,
    titleFontWeight='bold',
    titleColor='black',
    labelFontSize=12,
    labelColor='gray',
    titlePadding=10,
)

# Si estás en VS Code, debes guardar o mostrar el gráfico
chart.save("capacity_factor_variance_chart.html")
print("Gráfico guardado como: capacity_factor_variance_chart.html")

# ---------------------------------------------------------------
end = time.perf_counter()
print(f"Tiempo de ejecución: {end - start:.4f} segundos")
# ---------------------------------------------------------------

import time

# ---------------------------------------------------------------
# Inicio del temporizador (equivalente a %%time)
start = time.perf_counter()
# ---------------------------------------------------------------

# --- 1. Rango de tiempo de interés ---
start_time = "2020-06-21 00:00:00"
end_time = "2020-06-22 00:00:00"

# --- 2. Filtrar datos válidos ---
usa_filtered_dd = usa_rare[
    (~usa_rare.county_id_fips.isna()) &
    (usa_rare.datetime_utc.between(start_time, end_time))
]

# --- 3. Convertir subconjunto de Dask a pandas ---
usa_filtered_df = usa_filtered_dd.compute()

# --- 4. Asegurar que los FIPS sean tipo string ---
usa_filtered_df["county_id_fips"] = usa_filtered_df["county_id_fips"].astype("string")
county_gdf["county_id_fips"] = county_gdf["county_id_fips"].astype("string")

# --- 5. Unión con geometrías ---
usa_gdf_subset = county_gdf.merge(usa_filtered_df, on="county_id_fips")

# --- 6. Ejecutar la animación ---
anim = animate_capacity_factor_fixed(
    geodata=usa_gdf_subset,
    column="capacity_factor_onshore_wind",  # cambiar si deseas solar/onshore/offshore
    prefix="usa_",
    colormap="viridis",
    frame_duration_ms=500
)

# --- 7. Guardar el video (VS Code no muestra HTML directamente) ---
output_video = "usa_capacity_factor_onshore_wind.mp4"
anim.save(output_video, writer="ffmpeg")
print(f"Animación guardada como: {output_video}")

# ---------------------------------------------------------------
end = time.perf_counter()
print(f"Tiempo de ejecución: {end - start:.4f} segundos")
# ---------------------------------------------------------------
anim.save(output_video, writer="ffmpeg")

import time

# ---------------------------------------------------------------
# Inicio del temporizador (equivalente a %%time)
start_time_exec = time.perf_counter()
# ---------------------------------------------------------------

# --- 1. Rango de tiempo de interés ---
start = "2020-06-21 00:00:00"
end = "2020-06-22 00:00:00"

# --- 2. Filtrar datos válidos (FIPS + rango de tiempo) ---
usa_filtered_dd = usa_rare[
    (~usa_rare.county_id_fips.isna()) &
    (usa_rare.datetime_utc.between(start, end))
]

# --- 3. Convertir subconjunto Dask → pandas ---
usa_filtered_df = usa_filtered_dd.compute()

# --- 4. Asegurar que los FIPS sean strings ---
usa_filtered_df["county_id_fips"] = usa_filtered_df["county_id_fips"].astype("string")
county_gdf["county_id_fips"] = county_gdf["county_id_fips"].astype("string")

# --- 5. Unir energía + geometrías ---
usa_gdf_subset = county_gdf.merge(usa_filtered_df, on="county_id_fips")

# --- 6. Ejecutar la animación ---
anim = animate_capacity_factor_fixed(
    geodata=usa_gdf_subset,
    column="capacity_factor_solar_pv",  # solar, onshore, offshore
    prefix="usa_",
    colormap="plasma",
    frame_duration_ms=500
)

# --- 7. Guardar el video (VS Code no muestra HTML directamente) ---
output_file = "usa_capacity_factor_solar_pv.mp4"
anim.save(output_file, writer="ffmpeg")
print(f"Animación guardada en: {output_file}")

# ---------------------------------------------------------------
end_time_exec = time.perf_counter()
print(f"Tiempo de ejecución: {end_time_exec - start_time_exec:.4f} segundos")
# ---------------------------------------------------------------
anim.save(output_file, writer="ffmpeg")