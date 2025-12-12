# Definición de los datos

## Origen de los datos

- La base de datos utilizada para este proyecto es una compilación exhaustiva sobre el sector energético de Estados Unidos, alojada en SQLite. Esta información, recolectada de agencias nacionales e internacionales como la EIA y la FERC, es el resultado del esfuerzo de la organización Catalyst Cooperative para centralizar datos. La estructura de la base de datos en SQLite permite el almacenamiento y manejo de archivos en formatos CSV y Parquet de Apache, facilitando su análisis.

## Especificación de los scripts para la carga de datos

- ### Análisis Descriptivo de los Datos : 

    Inicialmente, se llevara a cabo la carga de la base de datos y las librerías que no serán más útiles para su manipulación y posterior análisis mediante estadísitica descriptiva e inferencial.

    Para realizar una primera exploración de la base de datos, realizaremos la búsqueda y análisis de datos de producción, consumo, costos, entre otros de la operación de Planta de Generación de Energía Eléctrica "Comanche" ubicada, ubicada en el Estado de Colorado, la cual genera energía mediante vapor calentado mediante que de Carbón (Termoeléctrica) y más recientemente Energía Solar Fotovoltaica; teniendo una capacidad neta instalada de 1252 Megavatios (MW).

    En los siguientes fragmentos de código se realiza la conexión de la copia de la base de datos previamente creada con las librerías de SQL Alchemy, con la finalidad de realizar la búsqueda y filtración de los datasets que contienen la información deseada sobre la planta de Comanche.

      #### Aumento de costos y tiempo de inactividad:
      
      Algunos datos disponibles de la FERC se superponen con los de la EIA y la EPA. Esto nos permite comparar las distintas fuentes de datos. Tanto la FERC como la EIA recopilan datos sobre costos de combustible y generación, aunque con diferentes resoluciones. El Formulario 1 de la FERC se informa anualmente y, por lo general, no con el mayor detalle de cada generador. Sin embargo, la FERC es única en informar categorías detalladas de costos de operación y mantenimiento (O&M) no relacionados con el combustible y las adiciones de capital a la planta, necesarias para obtener una visión global de los costos de producción de la planta.

      En los gráficos a continuación, analizamos el factor de capacidad general de la planta de Comanche, los costos de operación y mantenimiento (O&M) relacionados con el combustible y no relacionados con el combustible, y el historial de adiciones de capital.

      La línea discontinua roja indica la fecha de entrada en funcionamiento de la Unidad 3 de la planta Comanche. El factor de capacidad es la relación entre su generación real y la generación máxima posible si funcionara al 100 % de su capacidad de forma continua. El factor de capacidad general de la planta se redujo drásticamente con la incorporación de la nueva unidad, pasando de un nivel histórico de aproximadamente el 70 % a un 50 % incluso menor en los últimos años.

      Al mismo tiempo, los costos de operación y mantenimiento (O&M) por MWh generado, tanto de combustible como no combustible, aumentaron significativamente. Los precios del combustible escapan en gran medida al control de la empresa de servicios públicos y constituyen un costo puramente variable. Los costos del combustible en 2016 fueron anormalmente bajos. ¿Es esto real o un error en los informes? La EIA proporciona informes de costos de combustible mucho más detallados.
      
      Los costos de operación y mantenimiento no combustibles son una combinación de costos fijos y variables. Cuando los costos fijos se distribuyen entre una cantidad menor de MWh, el costo por MWh aumenta. Las adiciones de capital graficadas anteriormente se dividen en dos categorías distintas.
      
      Existe un flujo continuo de fondos hacia la planta, necesario para mantener todo en funcionamiento; parte del cual se clasifica como O&M, y parte como inversión de capital, que potencialmente se suma a la base tarifaria sobre la que la empresa de servicios públicos obtiene una rentabilidad. Antes de 2008, podíamos observar una tasa de inversión de capital continua de aproximadamente un dólar por MWh de generación. En 2008 y 2010, las adiciones de capital fueron considerablemente mayores.
      
      En 2008, esto se debió a los controles de emisiones que se añadieron a las antiguas Unidades 1 y 2. Luego, en 2010, el pico se debió a la inversión de más de mil millones de dólares en Comanche 3, que finalmente se materializó. Estas grandes adiciones de capital, aunque poco frecuentes, se amortizarán a lo largo de varias décadas, por lo que no son fáciles de comparar con los costos de operación y mantenimiento (O&M), tanto de combustible como de otros tipos. Sin embargo, el flujo continuo de adiciones de capital se asemeja más a un costo de mantenimiento continuo y es relativamente comparable a los demás costos de operación y mantenimiento mostrados.

      #### Estadísticas de generadores precalculadas según la EIA:

      Hemos precalculado una serie de estadísticas útiles de generadores basadas en los datos EIA 860 y 923 de las Tablas de generadores MCOE. A primera vista, podría pensarse que son fáciles de calcular, pero debido a los diferentes requisitos de informes que se aplican a los distintos tamaños y tipos de centrales eléctricas, lamentablemente esto no es así. Estas estadísticas están disponibles mensual y anualmente.

      #### Generación neta mensual:

      Muchos generadores reportan datos a nivel de generador. Sin embargo, cuando la generación se reporta a nivel de generador principal y combustible de la planta, asignamos la generación neta a los generadores que comparten el mismo generador principal y combustibles.

      #### Costos mensuales de combustible por MWh:

      Se reportan los costos de combustible para cada tipo de combustible de una planta. Asignamos los costos a nivel de generador con base en la generación neta. Para ello, asumimos que cada generador utiliza la misma combinación de combustibles.
      
      En general, los precios del carbón se han mantenido bastante estables. La Unidad 1 parece tener costos de combustible por MWh ligeramente más altos. Los aumentos repentinos en los costos de combustible por MWh se deben a que los costos mensuales de combustible se basan en las entregas de combustible, que pueden ocurrir incluso si la planta no está operando. Cabe destacar que los costos de combustible anormalmente bajos para 2016, que se presentaron en los datos del Formulario 1 de la FERC mencionados anteriormente, no aparecen en los datos de la EIA.

      #### Tasas de calor promedio mensuales:

      Se calculan a nivel de unidad utilizando la generación neta y el consumo de combustible a nivel de unidad. La mayor tasa de calor estimada para la Unidad 1 probablemente sea la causa de las mayores estimaciones de costos de combustible mencionadas anteriormente.

      #### Lectura de los datos de generación y emisiones por hora desde Apache Parquet:
      
      La serie temporal completa de emisiones por hora de miles de centrales eléctricas estadounidenses, que abarca el período 1995-2022, contiene casi mil millones de registros. Los datos se almacenan en un único archivo Apache Parquet con grupos de filas definidos por año y estado. Este formato comprimido en columnas permite consultas muy eficientes con las herramientas adecuadas, como Dask y PyArrow. Leer todo el conjunto de datos en memoria de una sola vez probablemente superará la RAM disponible. Otras herramientas como DuckDB (API de Python) también ofrecen una buena compatibilidad con Parquet.

      #### Potencia de Salida:

      Los diagramas de dispersión a continuación contienen más de medio millón de puntos. Muestran los patrones operativos de las tres unidades Comanche con una resolución horaria. Se observan claramente los límites superior e inferior de la potencia operativa de la planta, con la Unidad 3 operando típicamente entre 510 y 800 MW.
      
      Cabe destacar que, aunque las Unidades 1 y 2 tienen aproximadamente 50 años (entraron en funcionamiento en 1973 y 1975, respectivamente), parecen estar en funcionamiento con mayor frecuencia que la nueva Unidad 3.
      
      En particular, la Unidad 3 pasó la mayor parte de 2020 fuera de servicio y, desde entonces, ha experimentado varios meses de inactividad. Dado que la Unidad 3 representa más del 50% de la capacidad de generación total de la planta, estas interrupciones han tenido un gran impacto en el factor de capacidad general, como se vio anteriormente en los datos del factor de capacidad del Formulario 1 de la FERC.


## Referencias a rutas o bases de datos origen y destino

- Se emplearan una base de datos muy completa sobre el sector energético de Estados Unidos soportada en SQLite que compile un gran volumen de información recolectado de distintas agencias Nacionales e Internacionales de Energía (EIA, FERC, entre otros).Fuente: https://catalyst.coop/pudl/
- 
- Se manejaran principalmente datos númericos tipo float de consumo de energía eléctrica dado en Vatios-Hora (Wh) a lo largo de las últimas 2 decadas, la medida de tiempo se hace en años, que corresponde a valores enteros. También se estudian valores de tipo categorico para las ciudades, los estados y los tipos de tecnologías de generación eléctica a estudiar. *La base de datos seleccionada para la realización del presente proyecto es el resultado de un esfuerzo muy grande que está realizando la organización Catalyst Cooperative actualmente para la compilación de información muy completa del funcionamiento del Sector Energético no solo en Estados Unidos sino a Nivel Mundial mediante la centralización de los datos provenientes de diferentes Agencias Nacionales e Internacionales en una sola base de datos utlizando actualmente la plataforma SQLite.


### Rutas de origen de datos

- Origen Base de Datos Actualizada: (https://www.kaggle.com/datasets/catalystcooperative/pudl-project/data)
- Se utilizará una base de datos muy grande que contiene datos técnicos y finanancieros del sector energético Estadounidense que incluye generación y consumo de energía eléctrica, gas y combustibles fósiles. Esta base de datos esta estructurada en SQLite, la cual almacena los archivos en formato CSV, XML y Parquet de Apache.
- Para la exploración y el análisis de los datos se usará el entorno de Dask, teniendo en cuenta la gran compatibilidad para el manejo de archivos tipo Parquet, una gran velocidad de procesamiento de la información y una gran versatilidad en la manipulación de la información considerando que parte de los datos con esta tecnología se almacenan y manipulan en la memoria RAM mientras que el resto son almacenados en la memoria ROM (Disco Duro o SSD) antes de ser analizados, requiriendo así equipos con una memoria RAM más reducida que en el caso de otras tecnologías como Apache Spark, reduciendo considerablemente los costos. Dask es un entorno veloz para la manipulación de grandes volúmenes de datos, también cuenta con herramientas muy poderosas para llevar a cabo análisis estadístico de un volumen muy grande de datos e incluso llevar a cabo proyectos de Machine Learning con dichos datos gracias a su gran compatibilidad con el entorno de ciencia de datos de Python. La principal desventaja de utilizar Dask radica en que si se maneja volumenes demasiado grandes de datos, se requieren tiempos de procesamiento considerablemente mayores que otras tecnologías como Apache Spark debido a usa menores cantidades de Memoria RAM más veloz para la manipulación de datos, prolongando así los tiempos de procesamiento.

### Base de datos de destino

- [ ] Especificar la base de datos de destino para los datos.
- [ ] Especificar la estructura de la base de datos de destino.
- [ ] Describir los procedimientos de carga y transformación de los datos en la base de datos de destino.
