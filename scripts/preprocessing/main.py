##ANÁLISIS DESCRIPTIVO DE LOS DATOS DE LA BASE DE DATOS DE PUDL##
# connect_pudl.py

import os
import sqlalchemy as sa
import pandas as pd


def load_pudl_path():
    """
    Lee la ruta local generada por setup_pudl_local.py
    """
    ruta_txt = os.path.join(os.path.dirname(__file__), "pudl_path.txt")

    if not os.path.exists(ruta_txt):
        raise FileNotFoundError(
            "No se encontró 'pudl_path.txt'. Ejecuta primero setup_pudl_local.py"
        )

    with open(ruta_txt, "r", encoding="utf-8") as f:
        dataset_path = f.read().strip()

    return dataset_path


def connect_pudl():
    """
    Crea y devuelve una conexión SQLAlchemy al archivo pudl.sqlite
    """
    dataset_path = load_pudl_path()
    sqlite_path = os.path.join(dataset_path, "pudl.sqlite")

    if not os.path.exists(sqlite_path):
        raise FileNotFoundError(
            f"No se encontró la base de datos pudl.sqlite en:\n{sqlite_path}"
        )

    engine = sa.create_engine(f"sqlite:///{sqlite_path}")
    print("Conexión a PUDL creada correctamente.")
    return engine


if __name__ == "__main__":
    engine = connect_pudl()

    # Ejemplo de prueba: listar tablas
    with engine.connect() as conn:
        result = conn.execute(sa.text(
            "SELECT name FROM sqlite_master WHERE type='table';"
        ))

        print("\nTablas encontradas en pudl.sqlite:\n")
        for row in result:
            print(row[0])
import time
import pandas as pd
from connect_pudl import connect_pudl  # Importa la conexión creada antes

# Crear engine
pudl_engine = connect_pudl()

# ============================
# MEDIR TIEMPO DE EJECUCIÓN
# ============================

start_time = time.time()

# Cargar tabla usando pandas + SQLAlchemy
plants_eia = pd.read_sql(
    "SELECT * FROM out_eia__yearly_plants",
    pudl_engine
).convert_dtypes(convert_floating=False)

# ============================
# FILTRAR PLANTAS "COMANCHE"
# ============================

resultado = plants_eia.loc[
    plants_eia.plant_name_eia.str.contains("comanche", case=False),
    [
        "plant_id_eia",
        "plant_id_pudl",
        "plant_name_eia",
        "utility_name_eia",
        "city",
        "state",
        "latitude",
        "longitude",
    ]
].drop_duplicates()

end_time = time.time()

print(f"\nTiempo de ejecución: {end_time - start_time:.2f} segundos\n")

print("Resultados encontrados:\n")
print(resultado)

import time
import pandas as pd
from connect_pudl import connect_pudl   # Importa la función que crea el engine

# Crear engine
pudl_engine = connect_pudl()

# ============================
# MEDIR TIEMPO DE EJECUCIÓN
# ============================

start_time = time.time()

# Cargar tabla desde SQLite usando SQL estándar
plants_ferc1 = pd.read_sql(
    "SELECT * FROM out_ferc1__yearly_steam_plants_sched402",
    pudl_engine
).convert_dtypes(convert_floating=False)

end_time = time.time()

# Mostrar información de la tabla
print("\nInformación de la tabla plants_ferc1:\n")
plants_ferc1.info()

print(f"\nTiempo de ejecución: {end_time - start_time:.2f} segundos\n")

import time
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

end_time = time.time()

# ============================
# RESULTADO
# ============================

print(f"\nTiempo de ejecución: {end_time - start_time:.2f} segundos\n")

print("Datos filtrados para la planta Comanche (plant_id_pudl = 126):\n")
print(comanche_ferc1)

#Aumento de Costos y Tiempo de Inactividad#

import matplotlib.pyplot as plt

# Suponiendo que comanche_ferc1 ya está definido como un DataFrame
axes = (
    comanche_ferc1
    .set_index("report_year")[["capacity_factor"]]
    .plot(kind="bar", width=0.75)
)

axes.axvline(x=15.5, color="red", linestyle="--", linewidth=3)
axes.set_xlabel("Año Reportado")
axes.set_ylabel("Factor de Capacidad")
axes.set_title("Factor de Capacidad Anual Planta Comanche (Todas las Unidades)")
axes.set_ylim(0, 1)

plt.show()

#Estadísticas de generadores precalculadas según la EIA#

import pandas as pd

# Ejecutar consulta SQL
comanche_mcoe = (
    pd.read_sql(
        "SELECT * FROM out_eia__monthly_generators WHERE plant_id_eia=470",
        pudl_engine  # Debe estar inicializado previamente
    )
    .convert_dtypes(convert_floating=False)
    .sort_values(["report_date", "plant_id_eia", "generator_id"])
)

# Mostrar información básica del DataFrame
print(comanche_mcoe.info())

# Mostrar una muestra aleatoria de 10 filas
print(comanche_mcoe.sample(10))

#Generación neta mensual#

import matplotlib.pyplot as plt
import pandas as pd

gen_ids = ["1", "2", "3"]

# Crear figura y ejes
fig, axs = plt.subplots(
    nrows=len(gen_ids),
    ncols=1,
    sharex=True,
    figsize=(20, 15)
)

# Graficar por cada generador
for n, gen_id in enumerate(gen_ids):
    mask = comanche_mcoe.generator_id == gen_id

    axs[n].plot(
        pd.to_datetime(comanche_mcoe.loc[mask, "report_date"]),
        comanche_mcoe.loc[mask, "net_generation_mwh"] / 1000.0
    )

    axs[n].set_ylim(-10, 600)
    axs[n].set_title(f"Unidad de la Planta de Comanche {gen_id}")
    axs[n].set_ylabel("Generación neta [GWh]")

plt.show()

import plotly.graph_objs as go
import pandas as pd

# Asegúrate de que estas variables estén definidas antes:
# gen_ids = ["1", "2", "3"]
# comanche_mcoe = tu DataFrame ya cargado

fig = go.Figure()

for gen_id in gen_ids:
    datos = comanche_mcoe[comanche_mcoe.generator_id == gen_id]

    fig.add_trace(
        go.Scatter(
            x=pd.to_datetime(datos["report_date"]),
            y=datos["net_generation_mwh"] / 1000.0,
            mode='lines',
            name=f"Unidad {gen_id}",
        )
    )

fig.update_layout(
    title="Comparativo de Generación Neta - Plantas de Comanche",
    xaxis_title="Fecha",
    yaxis_title="Generación neta [GWh]",
    height=600,
    width=1000,
    legend_title="Unidades",
    hovermode="x unified",
)

fig.update_yaxes(range=[-10, 600])

fig.show()

#Costos mensuales de combustible por MWh#

import matplotlib.pyplot as plt
import pandas as pd

gen_ids = ["1", "2", "3"]

# Crear figura y ejes
fig, axs = plt.subplots(
    nrows=len(gen_ids),
    ncols=1,
    sharex=True,
    figsize=(20, 15)
)

# Graficar cada generador
for n, gen_id in enumerate(gen_ids):
    mask = comanche_mcoe.generator_id == gen_id

    axs[n].scatter(
        pd.to_datetime(comanche_mcoe.loc[mask, "report_date"]),
        comanche_mcoe.loc[mask, "fuel_cost_per_mwh"]
    )

    axs[n].set_ylim(-2, 60)
    axs[n].set_title(f"Unidad de la Planta Comanche {gen_id}")
    axs[n].set_ylabel("Costo de Combustible [US$/MWh]")

plt.show()


import plotly.graph_objs as go
import pandas as pd

# Asegúrate de definir estas variables antes de ejecutar:
# gen_ids = ["1", "2", "3"]
# comanche_mcoe = tu DataFrame ya cargado

fig = go.Figure()

for gen_id in gen_ids:
    datos = comanche_mcoe[comanche_mcoe.generator_id == gen_id]

    fig.add_trace(
        go.Scatter(
            x=pd.to_datetime(datos["report_date"]),
            y=datos["fuel_cost_per_mwh"],
            mode='markers',
            name=f"Unidad {gen_id}",
        )
    )

fig.update_layout(
    title="Comparativo de Costo de Combustible - Plantas Comanche",
    xaxis_title="Fecha",
    yaxis_title="Costo de Combustible [US$/MWh]",
    height=600,
    width=1000,
    legend_title="Unidades",
    hovermode="x unified",
)

fig.update_yaxes(range=[-2, 60])

fig.show()

# Tasas de calor promedio mensuales#

import matplotlib.pyplot as plt
import pandas as pd

gen_ids = ["1", "2", "3"]

# Crear la figura y los subplots
fig, axs = plt.subplots(
    nrows=len(gen_ids),
    ncols=1,
    sharex=True,
    figsize=(20, 15)
)

# Graficar cada unidad
for n, gen_id in enumerate(gen_ids):
    mask = comanche_mcoe.generator_id == gen_id

    axs[n].scatter(
        pd.to_datetime(comanche_mcoe.loc[mask, "report_date"]),
        comanche_mcoe.loc[mask, "unit_heat_rate_mmbtu_per_mwh"]
    )

    axs[n].set_ylim(-1, 20)
    axs[n].set_title(f"Unidad de Planta Comanche {gen_id}")
    axs[n].set_ylabel("Tasa de Calor [mmBTU/MWh]")

plt.show()

import plotly.graph_objs as go
import pandas as pd

# Asegúrate de definir estas variables antes de ejecutar:
# gen_ids = ["1", "2", "3"]
# comanche_mcoe = tu DataFrame ya cargado

fig = go.Figure()

for gen_id in gen_ids:
    datos = comanche_mcoe[comanche_mcoe.generator_id == gen_id]

    fig.add_trace(
        go.Scatter(
            x=pd.to_datetime(datos["report_date"]),
            y=datos["unit_heat_rate_mmbtu_per_mwh"],
            mode='markers',
            name=f"Unidad {gen_id}",
        )
    )

fig.update_layout(
    title="Comparativo de Tasa de Calor - Plantas Comanche",
    xaxis_title="Fecha",
    yaxis_title="Tasa de Calor [mmBTU/MWh]",
    height=600,
    width=1000,
    legend_title="Unidades",
    hovermode="x unified",
)

fig.update_yaxes(range=[-1, 20])

fig.show()

#Factor de Capacidad Mensual planta Comanche#

import matplotlib.pyplot as plt
import pandas as pd

gen_ids = ["1", "2", "3"]

# Crear figura y subplots
fig, axs = plt.subplots(
    nrows=len(gen_ids),
    ncols=1,
    sharex=True,
    figsize=(20, 15)
)

# Graficar cada unidad
for n, gen_id in enumerate(gen_ids):
    mask = comanche_mcoe.generator_id == gen_id

    axs[n].scatter(
        pd.to_datetime(comanche_mcoe.loc[mask, "report_date"]),
        comanche_mcoe.loc[mask, "capacity_factor"]
    )

    axs[n].set_ylim(-0.1, 1.1)
    axs[n].set_title(f"Unidad de Planta Comanche {gen_id}")
    axs[n].set_ylabel("Factor de Capacidad")

plt.show()

import plotly.graph_objs as go
import pandas as pd

# Asegúrate de definir estas variables antes de ejecutar:
# gen_ids = ["1", "2", "3"]
# comanche_mcoe = tu DataFrame ya cargado

fig = go.Figure()

for gen_id in gen_ids:
    datos = comanche_mcoe[comanche_mcoe.generator_id == gen_id]

    fig.add_trace(
        go.Scatter(
            x=pd.to_datetime(datos["report_date"]),
            y=datos["capacity_factor"],
            mode='markers',
            name=f"Unidad {gen_id}",
        )
    )

fig.update_layout(
    title="Comparativo de Factor de Capacidad - Plantas Comanche",
    xaxis_title="Fecha",
    yaxis_title="Factor de Capacidad",
    height=600,
    width=1000,
    legend_title="Unidades",
    hovermode="x unified",
)

fig.update_yaxes(range=[-0.1, 1.1])

fig.show()

#Lectura de los datos de generación y emisiones por hora desde Apache Parquet#

from dask import dataframe as dd
import pandas as pd

# Asegúrate de definir esta ruta antes:
# catalystcooperative_pudl_project_path = "RUTA/A/TU/PROYECTO"

unit_ids = ["1", "2", "3"]

cems_cols = [
    "operating_datetime_utc",
    "plant_id_eia",
    "plant_id_epa",
    "emissions_unit_id_epa",
    "operating_time_hours",
    "gross_load_mw",
    "heat_content_mmbtu",
    "co2_mass_tons",
]

# Cargar dataset CEMS con Dask
comanche_cems_dd = dd.read_parquet(
    f"{catalystcooperative_pudl_project_path}/pudl_parquet/core_epacems__hourly_emissions.parquet",
    engine="pyarrow",
    filters=[
        ("state", "=", "CO"),
        ("plant_id_eia", "=", 470),
    ],
    columns=cems_cols,
    index=False,
)

# Convertir a pandas y crear nuevas columnas
comanche_cems = (
    comanche_cems_dd.compute()
    .assign(
        gross_generation_mwh=lambda x: x.operating_time_hours * x.gross_load_mw,
        heat_rate_mmbtu_per_mwh=lambda x: x.heat_content_mmbtu / x.gross_generation_mwh,
        gross_co2_intensity=lambda x: x.co2_mass_tons / x.gross_generation_mwh,
    )
)

# Mostrar información del DataFrame
print(comanche_cems.info())

#Potencia de Salida#

import matplotlib.pyplot as plt
import pandas as pd

# Asegúrate de que estas variables ya existan:
# unit_ids = ["1", "2", "3"]
# comanche_cems = tu DataFrame ya cargado

fig, axs = plt.subplots(
    nrows=len(unit_ids),
    ncols=1,
    sharex=True,
    figsize=(20, 15)
)

for n, unit_id in enumerate(unit_ids):
    mask = comanche_cems.emissions_unit_id_epa == unit_id

    axs[n].scatter(
        comanche_cems.loc[mask, "operating_datetime_utc"],
        comanche_cems.loc[mask, "gross_generation_mwh"],
        s=0.2,
        alpha=0.1,
    )

    axs[n].set_ylim(-10, 850)
    axs[n].set_title(f"Unidad de Planta Comanche {unit_id}")
    axs[n].set_ylabel("Potencia de Salida por hora [MW]")

plt.show()

import plotly.graph_objs as go
import pandas as pd

# unit_ids = [...]  # tu lista de IDs, igual que gen_ids
# comanche_cems = ...  # tu DataFrame filtrado

fig = go.Figure()

for unit_id in unit_ids:
    datos = comanche_cems[comanche_cems.emissions_unit_id_epa == unit_id]

    fig.add_trace(
        go.Scattergl(  # Usar Scattergl para muchos puntos (más rápido e interactivo)
            x=datos["operating_datetime_utc"],
            y=datos["gross_generation_mwh"],
            mode="markers",
            marker=dict(size=2, opacity=0.1),  # Equivalente a s=0.2, alpha=0.1 en matplotlib
            name=f"Unidad {unit_id}",
        )
    )

fig.update_layout(
    title="Potencia de Salida por hora - Unidades Planta Comanche",
    xaxis_title="Fecha y Hora",
    yaxis_title="Potencia de Salida por hora [MW]",
    height=600,
    width=1000,
    legend_title="Unidades",
    hovermode="x unified",
)

fig.update_yaxes(range=[-10, 850])

fig.show()

#Consumo de Combustible (Carbón)#

import matplotlib.pyplot as plt

fig, axs = plt.subplots(
    nrows=len(unit_ids),
    ncols=1,
    sharex=True,
    figsize=(20, 15)
)

for n, unit_id in enumerate(unit_ids):
    axs[n].scatter(
        comanche_cems.loc[
            comanche_cems.emissions_unit_id_epa == unit_id, 
            "operating_datetime_utc"
        ],
        comanche_cems.loc[
            comanche_cems.emissions_unit_id_epa == unit_id, 
            "heat_content_mmbtu"
        ],
        s=0.2,
        alpha=0.1,
    )
    
    axs[n].set_ylim(-100, 10_000)
    axs[n].set_title(f"Unidad de Planta Comanche {unit_id}")
    axs[n].set_ylabel("Combustible Consumido [mmBTU/hr]")

plt.show()

import plotly.graph_objs as go
import pandas as pd

# unit_ids = [...]  # lista de unidades
# comanche_cems = ...  # DataFrame con los datos

fig = go.Figure()

for unit_id in unit_ids:
    datos = comanche_cems[comanche_cems.emissions_unit_id_epa == unit_id]
    
    fig.add_trace(
        go.Scattergl(
            x=datos["operating_datetime_utc"],
            y=datos["heat_content_mmbtu"],
            mode="markers",
            marker=dict(size=2, opacity=0.1),
            name=f"Unidad {unit_id}",
        )
    )

fig.update_layout(
    title="Consumo de Combustible por hora - Unidades Planta Comanche",
    xaxis_title="Fecha y Hora",
    yaxis_title="Combustible Consumido [mmBTU/hr]",
    height=600,
    width=1000,
    legend_title="Unidades",
    hovermode="x unified",
)

fig.update_yaxes(range=[-100, 10000])

fig.show()

#Tasas de Calor#

import matplotlib.pyplot as plt
import pandas as pd

# unit_ids = [...]  # lista de unidades
# comanche_cems = ...  # DataFrame con los datos

fig, axs = plt.subplots(
    nrows=len(unit_ids),
    ncols=1,
    sharex=True,
    figsize=(20, 15)
)

for n, unit_id in enumerate(unit_ids):
    axs[n].scatter(
        comanche_cems.loc[comanche_cems.emissions_unit_id_epa == unit_id, "operating_datetime_utc"],
        comanche_cems.loc[comanche_cems.emissions_unit_id_epa == unit_id, "heat_rate_mmbtu_per_mwh"],
        s=0.2,
        alpha=0.1,
    )
    axs[n].set_ylim(-1, 20)
    axs[n].set_title(f"Unidad de la Planta Comanche {unit_id}")
    axs[n].set_ylabel("Tasa de Calor [mmBTU/MWh]")

plt.show()

import plotly.graph_objs as go
import pandas as pd

# unit_ids = [...]  # tu lista de unidades
# comanche_cems = ...  # tu DataFrame

fig = go.Figure()

for unit_id in unit_ids:
    datos = comanche_cems[comanche_cems.emissions_unit_id_epa == unit_id]
    fig.add_trace(
        go.Scattergl(
            x=datos["operating_datetime_utc"],
            y=datos["heat_rate_mmbtu_per_mwh"],
            mode='markers',
            marker=dict(size=2, opacity=0.1),
            name=f"Unidad {unit_id}",
        )
    )

fig.update_layout(
    title="Tasa de Calor por hora - Unidades Planta Comanche",
    xaxis_title="Fecha y Hora",
    yaxis_title="Tasa de Calor [mmBTU/MWh]",
    height=600,
    width=1000,
    legend_title="Unidades",
    hovermode="x unified",
)

fig.update_yaxes(range=[-1, 20])

fig.show()

#Intensidad de Emisiones de CO2#

import matplotlib.pyplot as plt

fig, axs = plt.subplots(
    nrows=len(unit_ids),
    ncols=1,
    sharex=True,
    figsize=(20, 15)
)

for n, unit_id in enumerate(unit_ids):
    axs[n].scatter(
        comanche_cems.loc[comanche_cems.emissions_unit_id_epa == unit_id, "operating_datetime_utc"],
        comanche_cems.loc[comanche_cems.emissions_unit_id_epa == unit_id, "gross_co2_intensity"],
        s=0.2,
        alpha=0.1,
    )
    axs[n].set_ylim(0.5, 1.5)
    axs[n].set_title(f"Unidad de la Planta Comanche {unit_id}")
    axs[n].set_ylabel("Intensidad bruta de emisiones de CO₂ [tons/MWh]")

plt.show()

import plotly.graph_objs as go
import pandas as pd

# Asegúrate de tener definidas estas variables antes de ejecutar:
# unit_ids = ["1", "2", "3"]
# comanche_cems = <tu DataFrame>

fig = go.Figure()

for unit_id in unit_ids:
    datos = comanche_cems[comanche_cems.emissions_unit_id_epa == unit_id]

    fig.add_trace(
        go.Scattergl(
            x=datos["operating_datetime_utc"],
            y=datos["gross_co2_intensity"],
            mode="markers",
            marker=dict(size=2, opacity=0.1),
            name=f"Unidad {unit_id}",
        )
    )

fig.update_layout(
    title="Intensidad Bruta de Emisiones de CO₂ por hora - Unidades Planta Comanche",
    xaxis_title="Fecha y Hora",
    yaxis_title="Intensidad bruta de emisiones de CO₂ [tons/MWh]",
    height=600,
    width=1000,
    legend_title="Unidades",
    hovermode="x unified",
)

fig.update_yaxes(range=[0.5, 1.5])

fig.show()

import pandas as pd

# Asegúrate de tener definido pudl_engine antes de esto:
# pudl_engine = create_engine("sqlite:///ruta_a_tu_bd.sqlite")  (ejemplo)

df = pd.read_sql("core_pudl__codes_datasources", pudl_engine)
print(df)

import time
start = time.time()

df = pd.read_sql("core_pudl__codes_datasources", pudl_engine)

end = time.time()
print(df)
print(f"Tiempo de ejecución: {end - start:.4f} segundos")