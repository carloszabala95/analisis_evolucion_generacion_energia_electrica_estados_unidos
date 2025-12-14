from pathlib import Path
import os

import numpy as np
import pandas as pd
import streamlit as st
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.preprocessing import PolynomialFeatures
from sklearn.pipeline import Pipeline

# Rutas base; puedes sobrescribir con variables de entorno
BASE = Path(os.getenv("PUDL_PATH", "docs/data"))
CSV = BASE / "comanche_ferc1_annual.csv"
IMG_DIR = Path(os.getenv("IMG_PATH", BASE))


@st.cache_data
def load_data(csv_path: Path) -> pd.DataFrame:
    if not csv_path.exists():
        raise FileNotFoundError(f"No existe el archivo: {csv_path}")
    return pd.read_csv(csv_path)


def make_model(name: str, poly_degree: int = 2):
    if name == "LinearRegression":
        return LinearRegression()
    if name == "RandomForestRegressor":
        return RandomForestRegressor(
            n_estimators=200, random_state=0, n_jobs=-1, max_depth=None
        )
    if name == "GradientBoostingRegressor":
        return GradientBoostingRegressor(random_state=0)
    if name == "PolynomialRegression":
        return Pipeline(
            steps=[
                ("poly", PolynomialFeatures(degree=poly_degree, include_bias=False)),
                ("lr", LinearRegression()),
            ]
        )
    raise ValueError(f"Modelo no soportado: {name}")


@st.cache_data
def train_and_forecast(
    df: pd.DataFrame,
    target: str,
    model_name: str,
    test_years: int,
    years_ahead: int,
    poly_degree: int = 2,
    log_target: bool = False,
):
    df = df.dropna(subset=["report_year", target]).sort_values("report_year")
    y_raw = df[target].values
    if log_target:
        if (y_raw <= 0).any():
            raise ValueError("No se puede usar log para valores <= 0 en la serie objetivo.")
        y = np.log1p(y_raw)
    else:
        y = y_raw

    # Split cronológico: últimos test_years como test
    if test_years >= len(df):
        test_years = max(1, len(df) // 5)
    X = df[["report_year"]].values

    split_idx = len(df) - test_years
    X_train, X_test = X[:split_idx], X[split_idx:]
    y_train, y_test = y[:split_idx], y[split_idx:]

    model = make_model(model_name, poly_degree=poly_degree)
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    pred_all = model.predict(X)

    if log_target:
        y_test_eval = y_raw[split_idx:]
        y_pred_eval = np.expm1(y_pred)
        pred_all_eval = np.expm1(pred_all)
    else:
        y_test_eval = y_test
        y_pred_eval = y_pred
        pred_all_eval = pred_all

    metrics = {
        "MAE": float(mean_absolute_error(y_test_eval, y_pred_eval)),
        "RMSE": float(mean_squared_error(y_test_eval, y_pred_eval, squared=False)),
        "R2": float(r2_score(y_test_eval, y_pred_eval)),
    }

    last_year = int(df["report_year"].max())
    future_years = np.arange(last_year + 1, last_year + years_ahead + 1).reshape(-1, 1)
    preds = model.predict(future_years)
    if log_target:
        preds = np.expm1(preds)
    forecast_df = pd.DataFrame(
        {"year": future_years.flatten().astype(int), "prediction": preds.astype(float)}
    )

    results = {
        "model": model_name,
        "train_years": df["report_year"].tolist(),
        "train_values": y.tolist(),
        "pred_all": pred_all_eval.tolist(),
        "test_years": df.iloc[split_idx:]["report_year"].tolist(),
        "test_values": y_test_eval.tolist(),
        "test_preds": y_pred_eval.tolist(),
        "metrics": metrics,
        "forecast_df": forecast_df,
    }
    return results


def main():
    st.title("Analisis de Generación Eléctrica - Resultados y Pronósticos")
    st.subheader("Se debe seleccionar una opción en la barra lateral.")

    section = st.sidebar.radio(
        "Sección",
        ["Pronóstico", "Galería"],
        index=0,
        help="Elige si ver el Pronóstico o la galería de imágenes.",
    )

    if section == "Pronóstico":
        st.write("Predicción Planta de energía (Se debe cargar el csv por analizar).")
        st.write(f"Fuente de datos: `{CSV}`")
        try:
            df = load_data(CSV)
        except FileNotFoundError as exc:
            st.error(str(exc))
            st.stop()

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

        col3, col4 = st.columns(2)
        with col3:
            model_name = st.selectbox(
                "Modelo",
                options=[
                    "LinearRegression",
                    "RandomForestRegressor",
                    "GradientBoostingRegressor",
                    "PolynomialRegression",
                ],
                index=0,
            )
        with col4:
            test_years = st.slider(
                "Años para test (hold-out crono)",
                min_value=1,
                max_value=min(10, max(2, len(df) - 2)),
                value=3,
            )

        poly_degree = 2
        if model_name == "PolynomialRegression":
            poly_degree = st.slider("Grado polinómico", min_value=2, max_value=5, value=2)

        log_target = False
        if df[target].min() > 0:
            log_target = st.checkbox(
                "Usar log1p(y) en el objetivo",
                value=False,
                help="Transforma y -> log(1+y) para ajustar con el modelo y luego revierte la predicción.",
            )
        else:
            st.info("Log1p desactivado: la serie contiene valores <= 0.")

        st.subheader("Datos históricos (últimas filas)")
        st.dataframe(df.tail(10))

        results = train_and_forecast(
            df,
            target,
            model_name,
            test_years,
            years_ahead,
            poly_degree,
            log_target,
        )

        st.subheader(f"Métricas (test cronológico, {test_years} años)")
        m = results["metrics"]
        c1, c2, c3 = st.columns(3)
        c1.metric("MAE", f"{m['MAE']:.2f}")
        c2.metric("RMSE", f"{m['RMSE']:.2f}")
        c3.metric("R²", f"{m['R2']:.3f}")

        st.subheader(f"Pronóstico: {target}")
        st.dataframe(results["forecast_df"])
        st.subheader(f"Gráfico del Pronóstico: {target}")

        historical = df[["report_year", target]].rename(
            columns={"report_year": "year", target: "actual"}
        )
        pred_hist = pd.DataFrame(
            {"year": results["train_years"], "predicted": results["pred_all"]}
        )
        pred_future = results["forecast_df"].rename(columns={"prediction": "predicted"})
        pred_line = pd.concat([pred_hist, pred_future], ignore_index=True)

        chart_df = (
            historical.merge(pred_line, on="year", how="outer")
            .sort_values("year")
            .set_index("year")
        )
        st.line_chart(data=chart_df)

    else:
        st.subheader("Galería de imágenes del estudio")
        image_summaries = {
            # "ejemplo.png": "Descripción breve de la imagen."
        }
        img_paths = sorted(
            [
                p
                for p in IMG_DIR.glob("**/*")
                if p.suffix.lower() in {".png", ".jpg", ".jpeg", ".svg"}
            ]
        )
        if not img_paths:
            st.info(f"No se encontraron imágenes en {IMG_DIR}.")
        else:
            def bucket_for(name: str) -> str:
                name_low = name.lower()
                if name_low.startswith("image-"):
                    return "image-*"
                if name_low.startswith("newplot"):
                    return "newplot-*"
                if name_low.startswith("combust"):
                    return "combustible-*"
                if name_low.startswith("consumo"):
                    return "consumo-*"
                return "otros"

            buckets = {}
            for p in img_paths:
                key = bucket_for(p.name)
                buckets.setdefault(key, []).append(p)

            for label, paths in buckets.items():
                st.markdown(f"**{label}**")
                for p in sorted(paths):
                    caption = p.name
                    summary = image_summaries.get(p.name)
                    st.image(str(p), caption=caption, use_container_width=True)
                    if summary:
                        st.caption(summary)


if __name__ == "__main__":
    main()
