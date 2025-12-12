from pathlib import Path
import os
import pandas as pd
from fastapi import FastAPI
from sklearn.linear_model import LinearRegression
import numpy as np

app = FastAPI()
BASE = Path(os.getenv("PUDL_PATH", "docs/data"))
CSV = BASE / "comanche_ferc1_annual.csv"


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/sample")
def sample(n: int = 5):
    if not CSV.exists():
        return {"error": f"No existe {CSV}"}
    df = pd.read_csv(CSV)
    # Reemplazar NaN por None para que sea JSON-serializable
    return df.head(n).replace({np.nan: None}).to_dict(orient="records")


@app.get("/forecast")
def forecast(years_ahead: int = 3, target: str = "net_generation_mwh"):
    if not CSV.exists():
        return {"error": f"No existe {CSV}"}
    df = pd.read_csv(CSV)
    if target not in df.columns:
        return {"error": f"Columna objetivo no encontrada: {target}"}

    df = df.dropna(subset=["report_year", target])
    X = df[["report_year"]].values  # feature
    y = df[target].values           # objetivo

    model = LinearRegression()
    model.fit(X, y)

    last_year = int(df["report_year"].max())
    future_years = np.arange(last_year + 1, last_year + years_ahead + 1).reshape(-1, 1)
    preds = model.predict(future_years)

    return {
        "target": target,
        "train_years": df["report_year"].tolist(),
        "train_values": y.tolist(),
        "forecast": [
            {"year": int(year), "prediction": float(pred)}
            for year, pred in zip(future_years.flatten(), preds)
        ],
    }
