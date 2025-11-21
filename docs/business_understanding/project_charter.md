# Project Charter - Entendimiento del Negocio

## Nombre del Proyecto

Análisis de la evolución de Generación de Energía Eléctrica en Estados Unidos

## Objetivo del Proyecto

Estudiar las tendencias en el uso de tecnologías de generación de energía eléctrica, contrastando la evolución de las fuentes renovables con las convencionales, para determinar el potencial de las tecnologías libres de carbono para reemplazar a las que tienen una mayor huella de carbono. Esto busca ofrecer una visión clara de los factores que impulsan o limitan la adopción de energías limpias..

## Alcance del Proyecto

- Se desean tomar datos de diversas fuentes relacionadas con el mercado de la generación y comercialización de la energía eléctrica tales como la Agencia Internacional de Energía (IEA), la UPME, XM, entre otros; con el fin de realizar un analisis contratastado de la evolución en la generación de energía electrica mediante Tecnologías Alternativas libres de emisiones de CO2 con respecto a fuentes convencionales que utilizan combustibles fósiles como fuente de energía.
- Se analizarán los datos de generación y consumo de energía eléctrica de los últimos 20 años a nivel global, regional y nacional. No se incluiran aspecto del mercado de energía eléctrica tales como la transmisión y la comercialización para el presente proyecto de análisis de datos.
- Con el presente proyecto, se espera poder presentar a la partes interesadas un análisis detallado de la implementación de fuentes renovables libres de emisiones de CO2 y su evolución en la participación en la matriz de generación de electricidad contrastando los comportamientos observados con las tecnologías tradicionales de generación que emplean combustibles fósiles. Esto con la finalidad de sacar conclusiones de la factibilidad a futuro que tienen estas tecnologías para reemplazar las tecnologías convencionales que dejan una gran huella de carbono en el medio ambiente.

### Incluye:

El proyecto se apoya en una base de datos integral sobre el sector energético de Estados Unidos, principalmente el dataset PUDL Project de Catalyst Cooperative, almacenado en formato SQLite. Esta base de datos compila un vasto volumen de información recolectada de diversas agencias nacionales e internacionales como la EIA (Energy Information Administration) y la FERC (Federal Energy Regulatory Commission).

Los datos incluyen:

- Información de Plantas de Generación (EIA y FERC): Detalle de plantas, su capacidad instalada (MW), generación neta (MWh), factor de capacidad, costos de capital (CAPEX) y costos operativos (OPEX) por MWh, incluyendo costos de combustible y no combustible. Se dispone de datos anuales.
- Datos de Generadores (EIA MCOE): Estadísticas precalculadas de generadores a nivel mensual y anual, incluyendo generación neta, costos de combustible por MWh, tasas de calor y factor de capacidad por unidad generadora (ej. Comanche Units 1, 2, 3).
- Emisiones Horarias (EPA CEMS): Serie temporal completa de emisiones por hora de miles de centrales eléctricas estadounidenses, abarcando el período 1995-2022. Esta información incluye operating_datetime_utc, plant_id_eia, plant_id_epa, emissions_unit_id_epa, operating_time_hours, gross_load_mw, heat_content_mmbtu y co2_mass_tons. Estos datos se almacenan en un único archivo Apache Parquet, optimizado para el manejo de grandes volúmenes de datos.
- Potencial de Generación Renovable (VCE RARE): Datos horarios del factor de capacidad de energía solar fotovoltaica, eólica terrestre y eólica marina por condado en el Estados Unidos continental. Estos datos están disponibles en formato Parquet e incluyen state, place_name, datetime_utc, report_year, hour_of_year, county_id_fips, latitude, longitude, capacity_factor_solar_pv, capacity_factor_onshore_wind y capacity_factor_offshore_wind.
- Datos Geoespaciales (Censo DP1): Información geográfica a nivel de condado, incluyendo códigos FIPS y geometrías, para la creación de mapas y visualizaciones espaciales.
La manipulación y exploración de estos datasets se realiza principalmente con Dask y Pandas, aprovechando la eficiencia de Dask para volúmenes de datos que exceden la memoria RAM disponible.

Se espera que el proyecto brinde los siguientes resultados clave para las partes interesadas (UPME, XM SA ESP, Empresas Generadoras y Distribuidoras de Energía en Colombia):

- Análisis Comparativo Detallado: Un contraste claro y exhaustivo entre la evolución en la generación de energía eléctrica mediante Tecnologías Alternativas (libres de emisiones de CO2) y las fuentes convencionales que utilizan combustibles fósiles en Estados Unidos.
- Identificación de Tendencias y Patrones: Descubrimiento de patrones significativos en el uso, costos (CAPEX y OPEX), factor de capacidad y emisiones de CO2 para cada tipo de tecnología de generación a lo largo de las últimas dos décadas.
- Evaluación de la Viabilidad de Tecnologías Limpias: Determinación del potencial de las tecnologías renovables y nucleares para reemplazar completamente a las tecnologías tradicionales de alta huella de carbono, basándose en datos históricos de rendimiento y costos.
- Información para la Toma de Decisiones: Proporcionar al lector y a las partes interesadas una visión más clara acerca de los principales factores (tecnológicos, económicos, operativos) que pueden limitar o impulsar la adopción de energías limpias frente a energías no renovables en los próximos años.
- Visualizaciones Claras y Animadas: Mapas interactivos y animados de los factores de capacidad eólica y solar a nivel de condado en Estados Unidos, mostrando la variabilidad y el potencial de estas fuentes renovables en diferentes ubicaciones y momentos.
- Perfiles de Generación Específicos: Análisis de casos de estudio detallados (como la planta Comanche), ofreciendo insights sobre el comportamiento de unidades generadoras individuales en términos de potencia de salida, consumo de combustible, tasas de calor e intensidad de emisiones de CO2.

El éxito de este proyecto se medirá por la capacidad de:

- Integración y Procesamiento de Datos: Demostrar una integración y procesamiento efectivo de grandes volúmenes de datos de diversas fuentes (SQLite, Parquet, datos geoespaciales) utilizando herramientas como Dask y Pandas, manejando las limitaciones de recursos de manera eficiente.
- Claridad del Análisis Comparativo: Presentar un análisis que permita comprender claramente las diferencias y similitudes en el rendimiento (generación, factor de capacidad), costos (CAPEX, OPEX) y impacto ambiental (emisiones de CO2) entre las tecnologías de generación limpia y fósil.
- Relevancia de las Conclusiones: Extraer conclusiones significativas sobre la factibilidad a futuro de las tecnologías renovables para reemplazar las fuentes convencionales, las cuales sean de utilidad para la planificación energética y la formulación de políticas.
- Calidad de las Visualizaciones: Generar gráficos y mapas (incluyendo animaciones) que sean informativos, fáciles de interpretar y que ayuden a comunicar los patrones y tendencias clave de manera efectiva a una audiencia diversa.
- Utilidad para las Partes Interesadas: Que el análisis y las conclusiones sirvan como una base sólida para que las empresas y entidades del sector energético en Colombia (UPME, XM, etc.) puedan tomar decisiones informadas respecto a la transición energética y la inversión en energías limpias.
- Reproducibilidad y Escalabilidad: Asegurar que el código y la metodología sean reproducibles y, en la medida de lo posible, escalables para futuras expansiones o aplicaciones a otros contextos geográficos o temporales.

### Excluye:

- La base de datos seleccionada aún sigue en construcción, recibiendo actualizaciones diarias en horas de la noche, por ello solo se analizará la información del sector energético en Estados Unidos.
- Transmisión de energía eléctrica: No se abordarán los procesos ni la infraestructura relacionada con el transporte de la energía desde las plantas generadoras hasta los puntos de consumo.
- Comercialización de energía eléctrica: No se cubrirán los aspectos de compra, venta o distribución minorista de la energía eléctrica en el mercado.

## Metodología

Se utilizará una extensa base de datos SQLite del proyecto PUDL de Catalyst Cooperative, que integra información detallada del sector energético de EE. UU. Para el procesamiento y análisis de grandes volúmenes de datos (especialmente archivos Parquet), se empleará el entorno Dask, valorado por su eficiencia en la manipulación de datos y su compatibilidad con el ecosistema de ciencia de datos de Python, con la ventaja de requerir menos memoria RAM que otras soluciones como Apache Spark.

## Cronograma

| Etapa | Duración Estimada | Fechas |
|------|---------|-------|
| Entendimiento del negocio y carga de datos | 1 semanas | del 5 de noviembre al 12 de noviembre |
| Preprocesamiento, análisis exploratorio | 1 semanas | del 12 de noviembre al 19 de noviembre |
| Modelamiento y extracción de características | 1 semanas | del 19 de noviembre al 26 de noviembre |
| Despliegue | 1 semanas | del 26 de noviembre al 4 de diciembre |
| Evaluación y entrega final | 1 semanas | del 4 de diciembre al 19 de diciembre |


## Equipo del Proyecto

- Yefferson Stid Ruiz Cardona (ysruizc@unal.edu.co)
- Carlos Andrés Zabala Baquero (cazabalab@unal.edu.co)

## Presupuesto - Por Definir

[Descripción del presupuesto asignado al proyecto]

## Stakeholders - Por Definir

- [Nombre y cargo de los stakeholders del proyecto]
- [Descripción de la relación con los stakeholders]
- [Expectativas de los stakeholders]

## Aprobaciones - Por Definir

- [Nombre y cargo del aprobador del proyecto]
- [Firma del aprobador]
- [Fecha de aprobación]
