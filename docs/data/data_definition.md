# Definición de los datos

## Origen de los datos

- La base de datos utilizada para este proyecto es una compilación exhaustiva sobre el sector energético de Estados Unidos, alojada en SQLite. Esta información, recolectada de agencias nacionales e internacionales como la EIA y la FERC, es el resultado del esfuerzo de la organización Catalyst Cooperative para centralizar datos. La estructura de la base de datos en SQLite permite el almacenamiento y manejo de archivos en formatos CSV y Parquet de Apache, facilitando su análisis.

## Especificación de los scripts para la carga de datos

- ### Análisis Descriptivo de los Datos : 

    Inicialmente, se llevara a cabo la carga de la base de datos y las librerías que no serán más útiles para su manipulación y posterior análisis mediante estadísitica descriptiva e inferencial.

    Para realizar una primera exploración de la base de datos, realizaremos la búsqueda y análisis de datos de producción, consumo, costos, entre otros de la operación de Planta de Generación de Energía Eléctrica "Comanche" ubicada, ubicada en el Estado de Colorado, la cual genera energía mediante vapor calentado mediante que de Carbón (Termoeléctrica) y más recientemente Energía Solar Fotovoltaica; teniendo una capacidad neta instalada de 1252 Megavatios (MW).

    En los siguientes fragmentos de código se realiza la conexión de la copia de la base de datos previamente creada con las librerías de SQL Alchemy, con la finalidad de realizar la búsqueda y filtración de los datasets que contienen la información deseada sobre la planta de Comanche.

## Referencias a rutas o bases de datos origen y destino

- [ ] Especificar las rutas o bases de datos de origen y destino para los datos.

### Rutas de origen de datos

- [ ] Especificar la ubicación de los archivos de origen de los datos.
- [ ] Especificar la estructura de los archivos de origen de los datos.
- [ ] Describir los procedimientos de transformación y limpieza de los datos.

### Base de datos de destino

- [ ] Especificar la base de datos de destino para los datos.
- [ ] Especificar la estructura de la base de datos de destino.
- [ ] Describir los procedimientos de carga y transformación de los datos en la base de datos de destino.
