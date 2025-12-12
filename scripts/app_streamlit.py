from pathlib import Path
import os

import numpy as np
import pandas as pd
import streamlit as st
from sklearn.linear_model import LinearRegression

# Ruta base del CSV; permite override vía PUDL_PATH
BASE = Path(os.getenv("PUDL_PATH", "docs/data"))
CSV = BASE / "comanche_ferc1_annual.csv"


@st.cache_data
def load_data(csv_path: Path) -> pd.DataFrame:
    if not csv_path.exists():
        raise FileNotFoundError(f"No existe el archivo: {csv_path}")
    return pd.read_csv(csv_path)


@st.cache_data
def train_forecast(df: pd.DataFrame, target: str, years_ahead: int) -> pd.DataFrame:
    df = df.dropna(subset=["report_year", target])
    X = df[["report_year"]].values
    y = df[target].values

    model = LinearRegression()
    model.fit(X, y)

    last_year = int(df["report_year"].max())
    future_years = np.arange(last_year + 1, last_year + years_ahead + 1).reshape(-1, 1)
    preds = model.predict(future_years)

    forecast_df = pd.DataFrame(
        {"year": future_years.flatten().astype(int), "prediction": preds.astype(float)}
    )
    return forecast_df


def main():
    st.title("Comanche (PUDL) - Forecast rápido")
    st.write(f"Fuente de datos: `{CSV}`")

    try:
        df = load_data(CSV)
    except FileNotFoundError as exc:
        st.error(str(exc))
        st.stop()

    # Opciones de targets numéricos
    numeric_cols = [
        "net_generation_mwh",
        "capacity_factor",
        "capacity_mw",
        "capex_annual_addition",
        "opex_total_nonfuel",
    ]
    available_targets = [c for c in numeric_cols if c in df.columns]

    col1, col2 = st.columns(2)
    with col1:
        target = st.selectbox("Columna objetivo", options=available_targets, index=0)
    with col2:
        years_ahead = st.slider("Años a predecir", min_value=1, max_value=5, value=3)

    st.subheader("Datos históricos (últimas filas)")
    st.dataframe(df.tail(10))

    # Forecast
    forecast_df = train_forecast(df, target, years_ahead)

    st.subheader(f"Pronóstico: {target}")
    st.dataframe(forecast_df)

    st.line_chart(
        data=pd.concat(
            [
                df[["report_year", target]].rename(columns={"report_year": "year", target: "value"}),
                forecast_df.rename(columns={"prediction": "value"}),
            ],
            ignore_index=True,
        ).set_index("year")
    )


if __name__ == "__main__":
    main()
