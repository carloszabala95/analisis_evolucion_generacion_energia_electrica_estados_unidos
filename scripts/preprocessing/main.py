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