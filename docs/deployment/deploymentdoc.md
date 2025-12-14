# Despliegue de modelos

## Infraestructura
- Nombre del modelo:  Análisis Potencia de Generación de Energía Eléctrica en Estados Unidos
- Plataforma de despliegue: Railway (servicio web)
- Requisitos técnicos: Python >=3.9; deps: fastapi, uvicorn[standard], pandas, numpy, sqlalchemy, matplotlib, seaborn, scikit-learn, streamlit (kagglehub opcional)
- Requisitos de seguridad: sin autenticación; añadir auth/API key si se expone públicamente; evitar subir datos sensibles
- Diagrama de arquitectura: (no incluido; flujo simple cliente → Railway → FastAPI/Streamlit leyendo CSV)

## Código de despliegue
- Archivo principal: `scripts/app/main.py` (FastAPI) y `scripts/app_streamlit.py` (Streamlit, opcional)
- Rutas de acceso a los archivos: CSV por defecto `docs/data/comanche_ferc1_annual.csv`; imágenes en `docs/data` (o `IMG_PATH`); videos en `VIDEO_PATH` (por defecto la misma base)
- Variables de entorno:
  - `PORT` (inyectada por Railway)
  - `PUDL_PATH` (ruta del CSV; por defecto `docs/data`)
  - `IMG_PATH` (opcional, ruta de imágenes)
  - `VIDEO_PATH` (opcional, ruta de videos)

## Documentación del despliegue
- Instrucciones de instalación:
  - `pip install -r requirements.txt`
- Instrucciones de configuración:
  - Comando de arranque FastAPI: `uvicorn scripts.app.main:app --host 0.0.0.0 --port ${PORT}`
  - Comando de arranque Streamlit (servicio aparte): `streamlit run scripts/app_streamlit.py --server.port $PORT --server.address 0.0.0.0`
  - Definir variables de entorno según las rutas de datos deseadas
- Instrucciones de uso:
  - FastAPI: `/health`, `/sample`, `/forecast?years_ahead=3&target=<columna>`
  - Streamlit: usar sidebar para Pronóstico (CSV repo o subido), Subir CSV, Galería, Videos
- Instrucciones de mantenimiento:
  - Actualizar `docs/data/comanche_ferc1_annual.csv` si cambia el dataset
  - Revisar dependencias en `requirements.txt`/`pyproject.toml`
  - Redeploy en Railway tras cambios; verificar logs y endpoints