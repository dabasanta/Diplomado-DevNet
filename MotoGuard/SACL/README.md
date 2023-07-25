# Componentes del Sistema de Alerta de Colision Lateral (SAC-L) | Documentación Técnica

## Backend del Sistema

El backend del sistema es una parte crucial de la solución, ya que se encarga de almacenar y gestionar los datos recopilados por el dispositivo. Está compuesto por los siguientes componentes:

### Base de datos MySQL

La base de datos MySQL contiene dos tablas principales: `userdata` y `road_logs`.

- **userdata**: Almacena la información personal del usuario, como nombre, apellido, fecha de nacimiento, número de teléfono, identificador del vehículo y contacto de emergencia. Esta información es esencial para asociar los datos de los sensores y del GPS con un usuario específico y su vehículo, y para proporcionar un punto de contacto en caso de emergencia.

- **road_logs**: Almacena los registros de las rutas tomadas por el usuario. Cada registro incluye la latitud y longitud de un punto específico del recorrido, la fecha y hora del dato, la velocidad del vehículo en ese momento y un campo de alerta que puede tener el valor de 'incidente' o 'accidente'. Estos datos son los que el dispositivo recopila y envía a través de la API.

### API programada en Flask

La API proporciona una interfaz de comunicación web que permite la autenticación de usuarios, la recuperación de datos del perfil y los registros de ruta, y la grabación de nuevos registros de ruta en la base de datos. Además, se integra con Telegram para enviar alertas en caso de alta velocidad.

Se definen cuatro rutas en la API:

1. `/profile`: Ruta GET protegida por JWT que devuelve la información del perfil del usuario de la base de datos.
2. `/logs`: Ruta GET protegida por JWT que devuelve todos los registros de ruta almacenados en la base de datos.
3. `/login`: Ruta POST que toma un nombre de usuario y una contraseña, y si las credenciales son correctas, devuelve un token de acceso JWT.
4. `/save_log`: Ruta POST protegida por JWT que toma un objeto JSON con datos de latitud, longitud, fecha, velocidad y alerta, y los guarda en la base de datos. Si la velocidad es mayor a 80 KM/h, se envía una alerta a un chat de Telegram con la velocidad y la ubicación.

## Bot de Telegram

El Bot de Telegram interactúa con los usuarios, recibe y envía mensajes, y genera y envía estadísticas y gráficos basados en los datos de la base de datos.

El Bot cuenta con varias funciones para manejar diferentes tipos de mensajes entrantes, incluyendo el inicio y el fin de una "rodada" o viaje, y la generación y envío de estadísticas sobre los viajes recientes y totales. También puede generar y enviar un gráfico de barras de las alertas de la última semana.

## ESP32 – SACL

El sistema de SACL está escrito en Micro Python diseñado para ser ejecutado en un dispositivo ESP32. Su principal objetivo es recoger y transmitir datos de sensores y GPS, y controlar dispositivos de salida como LEDs.

El script importa los módulos necesarios para su ejecución, establece una conexión a una red WiFi utilizando las credenciales proporcionadas y realiza una autenticación con una API externa para obtener un token de acceso.

Se definen dos funciones asíncronas, `get_speed` y `get_gps`, que se encargan de leer y procesar los datos del GPS. Estas funciones se ejecutan continuamente en el bucle de eventos, actualizando las variables globales de velocidad, latitud y longitud con los datos más recientes del GPS.

La función principal o "main" del script se ejecuta en un bucle infinito, leyendo constantemente los datos de los sensores de ultrasonido. Si se detecta un objeto a menos de 100 cm, se enciende el LED correspondiente y se recopilan los datos del GPS. Estos datos se envían a una API externa mediante una solicitud POST. Si la solicitud es exitosa, se imprime un mensaje de éxito y se apaga el LED correspondiente.

## Aplicación web Incidents-Map

"Incidents-Map" es una aplicación web interactiva desarrollada para ser parte del frontend del sistema SACL. Proporciona una visualización gráfica y detallada de los incidentes en un mapa de la ciudad, utilizando para ello datos de incidentes obtenidos de una API Flask.

La aplicación web "Incidents-Map" es una herramienta interactiva de visualización de datos que tiene como objetivo proporcionar una representación gráfica de los incidentes en un mapa de la ciudad. Esta aplicación, escrita en Node.js y haciendo uso de los frameworks Vue y Nuxt, conecta con una API Flask para obtener los datos de los incidentes. La funcionalidad principal de la aplicación es recopilar y presentar los últimos 100 incidentes registrados. Al hacerlo, se conecta a la API Flask, obtiene los datos de los incidentes y luego los utiliza para generar marcadores en un mapa. Cada marcador representa un incidente individual y se coloca en el mapa según las coordenadas de latitud y longitud asociadas al incidente.

Al interactuar con la aplicación, los usuarios pueden hacer clic en un marcador individual para ver más detalles sobre el incidente correspondiente. Al seleccionar un marcador, se muestra un cuadro de información que proporciona detalles adicionales del incidente.
