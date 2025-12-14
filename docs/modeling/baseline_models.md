# Reporte del Modelo Baseline

## Descripción del modelo
- Se implementa un modelo base de regresión lineal que utiliza únicamente el año del reporte (report_year) como variable explicativa para pronosticar una variable objetivo numérica (por ejemplo, generación o capacidad).

- El modelo se entrena y evalúa usando datos anuales de una planta específica, tomados del archivo CSV por defecto
docs/data/comanche_ferc1_annual.csv o de un CSV cargado por el usuario mediante Streamlit.

- Este enfoque se utiliza como línea base de referencia, permitiendo comparar el desempeño de modelos más complejos como Random Forest, Gradient Boosting y Regresión Polinómica, y así evaluar si el aumento en complejidad realmente aporta mejoras significativas en la predicción.

## Variables de entrada
- `report_year` (feature temporal obligatoria).
- Otras columnas numéricas disponibles en el CSV se usan solo como objetivo, no como features en el baseline.

## Variable objetivo
- Seleccionable según el CSV (ejemplos en el CSV por defecto: `net_generation_mwh`, `capacity_factor`, `capacity_mw`, `capex_annual_addition`, `opex_total_nonfuel`).
- Para otros CSV, cualquier columna numérica distinta de `report_year` puede ser objetivo.

## Evaluación del modelo

### Métricas de evaluación
- MAE (Mean Absolute Error)
- RMSE (Root Mean Squared Error)
- R² (coeficiente de determinación)

### Resultados de evaluación (ejemplo con CSV por defecto)
- Entrenamiento/test: hold-out cronológico (configurable; por defecto 3 años para test).

- MAE (Mean Absolute Error) El error absoluto medio.
- RMSE (Root Mean Squared Error) La raíz del error cuadrático medio.

- El modelo de regresion Lineal evaluado no es adecuado para pronósticos a 3 años en su configuración actual. Las métricas obtenidas, especialmente el R² negativo, evidencian una falta de capacidad 
predictiva y de generalización temporal, lo que justifica la necesidad de ajustar el enfoque metodológico antes de su uso en producción.


- El RandomForestRegressor representa una mejora clara en términos de error frente al modelo previo, pero no alcanza un desempeño adecuado para pronósticos a 3 años. El R² aún 
negativo indica que, si bien el modelo aprende relaciones más complejas, no logra capturar completamente la dinámica temporal necesaria para una predicción confiable a largo plazo.


- El GradientBoostingRegressor es el modelo con mejor desempeño relativo para el pronóstico energético en este estudio. Aunque el R² aún negativo indica que el problema sigue 
siendo desafiante en horizontes largos, el modelo reduce significativamente el error, muestra mayor estabilidad temporal y representa el mejor compromiso entre precisión y 
eficiencia computacional.   

## Análisis de los resultados
- Fortalezas: modelo rápido, interpretable, línea base inmediata para comparar mejoras.
- Debilidades: solo usa tendencia temporal lineal; no captura no linealidades, estacionalidad ni interacciones.
- Riesgo de sobreestimar capacidad si la serie presenta cambios estructurales; evaluar residuales para decidir modelos más ricos.

## Conclusiones
- El baseline lineal es suficiente para una primera aproximación y para validar el pipeline de datos.
- Se recomienda comparar con modelos no lineales (RandomForestRegressor, GradientBoostingRegressor, PolynomialRegression) ya incluidos en la app Streamlit, usando las mismas métricas y partición cronológica.

## Referencias
- CSV de referencia: `docs/data/comanche_ferc1_annual.csv` (o CSV cargado por el usuario en la app).
