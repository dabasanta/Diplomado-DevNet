# API REST

## Instalación de Python3 y Flask

Este procedimiento detalla la instalación de Flask en un sistema Linux Debian:

```bash
sudo apt install python3
sudo apt install python3-pip
pip3 install flask
```

![Instalación de Flask con pip](API%20REST%20385e4e8871594e8b9b39dd47f27eb40e/Untitled.png)

Instalación de Flask con pip

## Configuración de la base de datos

Para la conexión a la base de datos se ha usado la librería `flask_mysqldb`

```python
# Importación de las librerías necesarias
from flask import Flask
from flask_mysqldb import MySQL

# Creación de la aplicación Flask
app = Flask(__name__)

# Configuración de los parámetros de conexión a la base de datos MySQL
app.config['MYSQL_HOST'] = '34.71.210.97'  # Dirección IP o nombre del host del servidor MySQL
app.config['MYSQL_USER'] = 'operator'  # Usuario para acceder a la base de datos
app.config['MYSQL_PASSWORD'] = '*************'  # Contraseña del usuario para acceder a la base de datos
app.config['MYSQL_DB'] = 'SACL'  # Nombre de la base de datos a la que se conectará la aplicación
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'  # Tipo de cursor a utilizar para obtener resultados como diccionarios

mysql = MySQL(app)
```

En este código, se configura una conexión a una base de datos MySQL utilizando Flask-MySQLDB. A continuación, se detallan las anotaciones:

1. **`from flask import Flask`**: Importamos la clase Flask desde la librería Flask, necesaria para crear una aplicación Flask.
2. **`from flask_mysqldb import MySQL`**: Importamos la clase MySQL desde la extensión Flask-MySQLDB, que nos permite interactuar con una base de datos MySQL desde nuestra aplicación Flask.
3. **`app = Flask(__name__)`**: Creamos una instancia de la clase Flask, que representa nuestra aplicación Flask.
4. **`app.config['MYSQL_HOST'] = '34.71.210.97'`**: Configuramos el parámetro 'MYSQL_HOST' para especificar la dirección IP o nombre del host del servidor MySQL al que nos conectaremos.
5. **`app.config['MYSQL_USER'] = 'operator'`**: Configuramos el parámetro 'MYSQL_USER' para especificar el nombre del usuario que utilizará la aplicación para acceder a la base de datos.
6. **`app.config['MYSQL_PASSWORD'] = '*************'`**: Configuramos el parámetro 'MYSQL_PASSWORD' para especificar la contraseña del usuario que utilizará la aplicación para acceder a la base de datos. NOTA: En una implementación real, esta contraseña debería mantenerse segura y no revelarse en el código fuente.
7. **`app.config['MYSQL_DB'] = 'SACL'`**: Configuramos el parámetro 'MYSQL_DB' para especificar el nombre de la base de datos a la que se conectará la aplicación.
8. **`app.config['MYSQL_CURSORCLASS'] = 'DictCursor'`**: Configuramos el parámetro 'MYSQL_CURSORCLASS' para utilizar un cursor de tipo 'DictCursor'. Esto permite obtener los resultados de las consultas en forma de diccionarios, lo que facilita el acceso a los datos.
9. **`mysql = MySQL(app)`**: Creamos una instancia de la clase MySQL pasándole como parámetro la aplicación Flask previamente configurada. Esta instancia representará la conexión a la base de datos MySQL y nos permitirá interactuar con ella en nuestra aplicación.

## Token de acceso

Se ha usado la librería `flask_jwt_extended` para la generación de tokens JWT, los cuales se consideran seguros en la actualidad.

```python
# Importación de las librerías necesarias
from flask_jwt_extended import JWTManager, jwt_required, create_access_token
from flask import Flask, request, jsonify

# Creación de la aplicación Flask
app = Flask(__name__)

# Configuración de la clave secreta para el manejo de JWT
app.config['JWT_SECRET_KEY'] = '******************Machine(*^#'  # NOTA: En una implementación real, esta clave debería mantenerse segura y no revelarse en el código fuente.
jwt = JWTManager(app)

# Ruta para el inicio de sesión, se espera una solicitud POST con los datos de usuario y contraseña.
@app.route('/login', methods=['POST'])
def login():
    try:
        # Obtener el nombre de usuario y contraseña de la solicitud JSON
        username = request.json.get('username')
        password = request.json.get('password')

        # NOTA: En una implementación real, el inicio de sesión debería verificarse contra una base de datos con los datos del usuario.
        # Sin embargo, en este prototipo, se utiliza una comparación simple mediante if/else con credenciales predefinidas para demostración.

        # Comprobar si el nombre de usuario y contraseña coinciden con las credenciales predefinidas.
        if username == 'SACL' and password == '****************':
            # Si las credenciales son válidas, se crea un token de acceso JWT para el usuario.
            access_token = create_access_token(identity=username)
            return jsonify({'access_token': access_token}), 200
        else:
            # Si las credenciales son inválidas, se devuelve un mensaje de error y un código de estado 401 (No autorizado).
            return jsonify({'message': 'Credenciales inválidas'}), 401
    except Exception as e:
        # En caso de cualquier error durante el proceso de inicio de sesión, se devuelve un mensaje de error y un código de estado 500 (Error interno del servidor).
        return jsonify({'error': str(e)}), 500
```

Este código implementa un punto de acceso "/login" en una aplicación Flask para autenticar usuarios mediante JWT. Es importante tener en cuenta que esta implementación es solo un prototipo y no se recomienda para un entorno de producción, ya que el proceso de autenticación debe realizarse de manera más segura, conectándose a una base de datos y almacenando las contraseñas de manera segura mediante técnicas de hash y salting.

### Probando autorizador

Para esto, se debe consumir la API `/login` para enviar los datos de usuario y contraseña, si la autenticación es exitosa el token de autorización será retornado en la respuesta.

```bash
#!/bin/bash

# Asignación de nombre de usuario y contraseña
username="admin"
password="********"

# URL del endpoint de login
url="http://34.71.210.97:5000/login"

# Datos de la solicitud en formato JSON
data="{\"username\":\"$username\",\"password\":\"$password\"}"

# Realizar la solicitud POST utilizando curl
response=$(curl -s -X POST -H "Content-Type: application/json" -d "$data" "$url")

# Imprimir la respuesta
echo "$response"
```

Ejemplo de la respuesta:

```bash
curl -X GET -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTY4Nzk2OTA0NCwianRpIjoiY2I3MDA0ZDMtNGY2NS00YzU0LTgwNjQtZTYyZjIzODZjMDJjIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6ImFkbWluIiwibmJmIjoxNjg3OTY5MDQ0LCJleHAiOjE2ODc5Njk5NDR9.j9tyxsQTCKFjhFuk_WbP-7sqYlXEa4b-hXupO87052g" "http://34.71.210.97:5000/profile"
{"apellido":"Doe","contacto_emergencia":"300********","fecha_nacimiento":"1190-04-25","nombre":"John","numero_telefono":"300********"}
```

# Métodos de la API

## Profile

La ruta de acceso al perfil es "`/profile`" y la función se protege con el decorador "`@jwt_required`" de Flask-JWT-Extended, lo que significa que solo los usuarios autenticados con un token válido pueden acceder a esta ruta.

```python
# Importación del decorador jwt_required y la función jsonify de Flask
from flask_jwt_extended import jwt_required
from flask import jsonify

# Definición de la ruta "/profile" para obtener el perfil del usuario
@jwt_required
@app.route('/profile', methods=['GET'])
def get_profile():
    try:
        # Establecer una conexión con la base de datos MySQL
        cursor = mysql.connection.cursor()

        # Ejecutar una consulta SQL para obtener los datos del usuario
        cursor.execute("SELECT nombre, apellido, fecha_nacimiento, numero_telefono, contacto_emergencia FROM userdata")

        # Obtener la primera fila de los resultados de la consulta
        data = cursor.fetchone()

        # Cerrar el cursor para liberar recursos de la conexión
        cursor.close()

        # Crear un diccionario con los datos del perfil del usuario
        profile = {
            'nombre': data['nombre'],
            'apellido': data['apellido'],
            'fecha_nacimiento': str(data['fecha_nacimiento']),
            'numero_telefono': data['numero_telefono'],
            'contacto_emergencia': data['contacto_emergencia']
        }

        # Devolver los datos del perfil en formato JSON con un código de estado 200 (OK)
        return jsonify(profile), 200
    except Exception as e:
        # En caso de cualquier error durante el proceso, devolver un mensaje de error en formato JSON con un código de estado 500 (Error interno del servidor).
        return jsonify({'error': str(e)}), 500
```

Este código es una función de un servidor web implementado con Flask, que responde a solicitudes GET en la ruta "`/profile`" para obtener el perfil de un usuario desde la base de datos MySQL. El decorador "`@jwt_required`" asegura que solo los usuarios autenticados con un token JWT válido pueden acceder a esta ruta, lo que proporciona una capa adicional de seguridad.

En la función "`get_profile()`", se realiza una consulta SQL a la tabla "`userdata`" para obtener los datos del usuario. Luego, estos datos se procesan y se almacenan en un diccionario llamado "`profile`". Finalmente, se devuelve este diccionario en formato JSON con un código de estado `HTTP 200` (OK) en caso de éxito, o un mensaje de error en formato JSON con un código de estado `HTTP 500` (Error interno del servidor) si se produce algún error durante el proceso.

Cabe mencionar que, en el código proporcionado, no se muestra la conexión a la base de datos, lo que significa que debe existir una configuración adecuada de la base de datos y una conexión establecida antes de que esta función pueda funcionar correctamente. Además, se asume que la base de datos contiene una tabla llamada "`userdata`" con los campos "`nombre`", "`apellido`", "`fecha_nacimiento`", "`numero_telefono`" y "`contacto_emergencia`".

## Logs

Este método corresponde a una solicitud `GET` para obtener registros de eventos de la base de datos. La ruta de acceso a los registros es "`/logs`" y al igual que el código anterior, esta función también está protegida con el decorador "`@jwt_required`" de *Flask-JWT-Extended*, lo que implica que solo los usuarios autenticados con un token válido pueden acceder a esta ruta.

```python
# Importación del decorador jwt_required y la función jsonify de Flask
from flask_jwt_extended import jwt_required
from flask import jsonify

# Definición de la ruta "/logs" para obtener los registros de eventos
@jwt_required
@app.route('/logs', methods=['GET'])
def get_logs():
    try:
        # Establecer una conexión con la base de datos MySQL
        cursor = mysql.connection.cursor()

        # Ejecutar una consulta SQL para obtener los registros de eventos
        cursor.execute("SELECT latitud, longitud, fecha, velocidad, alerta FROM road_logs")

        # Obtener todos los resultados de la consulta
        data = cursor.fetchall()

        # Cerrar el cursor para liberar recursos de la conexión
        cursor.close()

        # Crear una lista vacía para almacenar los registros de eventos
        logs = []

        # Procesar cada registro de evento y agregarlo a la lista de logs
        for log in data:
            log_entry = {
                'latitud': log['latitud'],
                'longitud': log['longitud'],
                'fecha': str(log['fecha']),
                'velocidad': log['velocidad'],
                'alerta': log['alerta']
            }
            logs.append(log_entry)

        # Devolver la lista de registros de eventos en formato JSON con un código de estado 200 (OK)
        return jsonify(logs), 200
    except Exception as e:
        # En caso de cualquier error durante el proceso, devolver un mensaje de error en formato JSON con un código de estado 500 (Error interno del servidor).
        return jsonify({'error': str(e)}), 500
```

Este código es una función similar a la anterior, pero en este caso, responde a solicitudes GET en la ruta "`/logs`" para obtener registros de eventos almacenados en una tabla de la base de datos llamada "`road_logs`". Al igual que antes, el decorador "`@jwt_required`" asegura que solo los usuarios autenticados con un token JWT válido pueden acceder a esta ruta.

En la función "`get_logs()`", se realiza una consulta SQL a la tabla "`road_logs`" para obtener los registros de eventos. Luego, se procesan estos datos y se almacenan en una lista de diccionarios llamada "`logs`". Cada diccionario representa un registro de evento y contiene información como la latitud, longitud, fecha, velocidad y alerta asociadas a cada evento.

Finalmente, la lista de registros de eventos "*`logs`*" se devuelve en formato *JSON* con un código de estado `HTTP 200` (*OK*) en caso de éxito, o un mensaje de error en formato *JSON* con un código de estado `HTTP 500` (*Error interno del servidor*) si se produce algún error durante el proceso.

Al igual que en el código anterior, se asume que la conexión a la base de datos ya ha sido configurada adecuadamente y establecida antes de que esta función pueda funcionar correctamente. Además, se asume que la tabla "`road_logs`" contiene los campos "`latitud`", "`longitud`", "`fecha`", "`velocidad`" y "`alerta`" para almacenar los registros de eventos.

## Save_log

Este método responde a una solicitud POST para guardar registros de eventos de SACL (ESP32) en la base de datos. La ruta de acceso para guardar los registros es "`/save_log`" y, al igual que en los códigos anteriores, esta función también está protegida con el decorador "`@jwt_required`" de *Flask-JWT-Extended*, lo que significa que solo los usuarios autenticados con un token válido pueden acceder a esta ruta.

```python
# Importación del decorador jwt_required y la función jsonify de Flask
from flask_jwt_extended import jwt_required
from flask import request, jsonify

# Definición de la ruta "/save_log" para guardar registros de eventos
@jwt_required
@app.route('/save_log', methods=['POST'])
def save_log():
    try:
        # Obtener los datos de la solicitud en formato JSON
        data = request.get_json()

        # Obtener los valores de longitud, latitud, fecha, velocidad y alerta del diccionario 'data'
        longitud = data['longitud']
        latitud = data['latitud']
        fecha = data['fecha']
        velocidad = data['velocidad']
        alerta = data['alerta']

        # Establecer una conexión con la base de datos MySQL
        cursor = mysql.connection.cursor()

        # Crear la consulta SQL para insertar los datos en la tabla 'road_logs'
        query = """
        INSERT INTO road_logs (latitud, longitud, fecha, velocidad, alerta)
        VALUES (%s, %s, %s, %s, %s)
        """

        # Ejecutar la consulta SQL con los valores proporcionados
        cursor.execute(query, (latitud, longitud, fecha, velocidad, alerta))

        # Realizar la confirmación de la transacción en la base de datos
        mysql.connection.commit()

        # Cerrar el cursor para liberar recursos de la conexión
        cursor.close()

        # Configuración de la base de datos y envío de alerta si la velocidad es mayor a 20.00 KM/h
        db_config = {
            'host': '34.71.210.97',
            'user': 'operator',
            'password': '**********',
            'database': 'SACL'
        }

        if velocidad > 20.00:
            # Crear una instancia de la clase TelegramBot y enviar un mensaje y ubicación a través de Telegram
            bot = TelegramBot("63*******************BM", db_config)
            chat_id = 'xxxxxxx'
            bot.send_message(chat_id=chat_id, text=f"*Alerta de alta velocidad:* {velocidad} KM/h")
            bot.send_location(chat_id=chat_id, latitude=latitud, longitude=longitud)

        # Devolver un mensaje de éxito en formato JSON con un código de estado 200 (OK)
        return jsonify({'message': 'Datos guardados correctamente'}), 200
    except Exception as e:
        # En caso de cualquier error durante el proceso, devolver un mensaje de error en formato JSON con un código de estado 500 (Error interno del servidor).
        return jsonify({'error': str(e)}), 500
```

En este código, la función "`save_log()`" responde a solicitudes POST en la ruta "`/save_log`" para guardar registros de eventos en una tabla de la base de datos llamada "`road_logs`". Al igual que en los ejemplos anteriores, el decorador `"@jwt_required`" asegura que solo los usuarios autenticados con un token JWT válido puedan acceder a esta ruta.

Dentro de la función, se obtienen los datos de la solicitud en formato JSON y luego se extraen los valores de longitud, latitud, fecha, velocidad y alerta de ese diccionario.

Luego, se establece una conexión con la base de datos MySQL y se crea una consulta SQL para insertar los datos en la tabla "`road_logs`". La consulta se ejecuta con los valores proporcionados y luego se realiza una confirmación de la transacción en la base de datos utilizando **`mysql.connection.commit()`**.

Además, se verifica si la velocidad es mayor a 80.00 KM/h. Si es así, se envía una alerta a través de Telegram utilizando una instancia de la clase "`TelegramBot`" y se envía un mensaje de texto junto con la ubicación (`latitud` y `longitud`) del evento registrado.

Finalmente, se devuelve un mensaje de éxito en formato JSON con un código de estado `HTTP 200` (OK) si todo el proceso se realiza correctamente. En caso de algún error durante el proceso, se devuelve un mensaje de error en formato JSON con un código de estado `HTTP 500` (Error interno del servidor).
