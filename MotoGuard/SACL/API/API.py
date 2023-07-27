# Importación de los módulos necesarios
from datetime import datetime
from flask import Flask, jsonify, request
from flask_mysqldb import MySQL
from flask_jwt_extended import JWTManager, jwt_required, create_access_token
from flask_cors import CORS
from telegram_bot import TelegramBot

# Creación de una instancia de la aplicación Flask
app = Flask(__name__)

# Habilitar el soporte para solicitudes de Cross-Origin Resource Sharing (CORS)
CORS(app)

# Configuración de la base de datos MySQL
app.config['MYSQL_HOST'] = '34.71.210.97'
app.config['MYSQL_USER'] = 'operator'
app.config['MYSQL_PASSWORD'] = '********************'
app.config['MYSQL_DB'] = 'SACL'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

# Configuración para el manejo de JWT
app.config['JWT_SECRET_KEY'] = '*************(*^#'
jwt = JWTManager(app)

# Creación de una instancia de MySQL para la conexión con la base de datos
mysql = MySQL(app)

# Definición de la ruta "/profile" para obtener el perfil del usuario
@jwt_required
@app.route('/profile', methods=['GET'])
def get_profile():
    try:
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT nombre, apellido, fecha_nacimiento, numero_telefono, contacto_emergencia FROM userdata")
        data = cursor.fetchone()
        cursor.close()

        profile = {
            'nombre': data['nombre'],
            'apellido': data['apellido'],
            'fecha_nacimiento': str(data['fecha_nacimiento']),
            'numero_telefono': data['numero_telefono'],
            'contacto_emergencia': data['contacto_emergencia']
        }

        return jsonify(profile), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Definición de la ruta "/logs" para obtener los registros de eventos
@jwt_required
@app.route('/logs', methods=['GET'])
def get_logs():
    try:
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT latitud, longitud, fecha, velocidad, alerta FROM road_logs")
        data = cursor.fetchall()
        cursor.close()

        logs = []
        for log in data:
            log_entry = {
                'latitud': log['latitud'],
                'longitud': log['longitud'],
                'fecha': str(log['fecha']),
                'velocidad': log['velocidad'],
                'alerta': log['alerta']
            }
            logs.append(log_entry)

        return jsonify(logs), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Definición de la ruta "/login" para realizar el inicio de sesión
@app.route('/login', methods=['POST'])
def login():
    try:
        username = request.json.get('username')
        password = request.json.get('password')

        if username == 'operator' and password == '****************':
            access_token = create_access_token(identity=username)
            return jsonify({'access_token': access_token}), 200
        else:
            return jsonify({'message': 'Credenciales inválidas'}), 401
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Definición de la ruta "/save_log" para guardar los registros de eventos
@jwt_required
@app.route('/save_log', methods=['POST'])
def save_log():
    try:
        data = request.get_json()

        longitud = data['longitud']
        latitud = data['latitud']
        fecha = data['fecha']
        velocidad = data['velocidad']
        alerta = data['alerta']

        cursor = mysql.connection.cursor()
        query = """
        INSERT INTO road_logs (latitud, longitud, fecha, velocidad, alerta)
        VALUES (%s, %s, %s, %s, %s)
        """
        cursor.execute(query, (latitud, longitud, fecha, velocidad, alerta))
        mysql.connection.commit()
        cursor.close()
        
        db_config = {
        'host': '34.71.210.97',
        'user': 'operator',
        'password': 'SuperSecretPassword$',
        'database': 'SACL'
    }
        
        if velocidad > 80.00:
            bot = TelegramBot("63***************************M", db_config)
            chat_id = '********'
            bot.send_message(chat_id='xxxxxx', text=f"*Alerta de alta velocidad:* {velocidad} KM/h")
            bot.send_location(chat_id='xxxxxxx', latitude=latitud, longitude=longitud)

        return jsonify({'message': 'Datos guardados correctamente'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Iniciar el servidor de desarrollo si este archivo es el punto de entrada principal
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
