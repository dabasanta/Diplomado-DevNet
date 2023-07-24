from datetime import datetime
from flask import Flask, jsonify, request
from flask_mysqldb import MySQL
from flask_jwt_extended import JWTManager, jwt_required, create_access_token
from flask_cors import CORS
from telegram_bot import TelegramBot

app = Flask(__name__)
CORS(app)

app.config['MYSQL_HOST'] = '34.71.210.97'
app.config['MYSQL_USER'] = 'operator'
app.config['MYSQL_PASSWORD'] = 'SuperSecretPassword$'
app.config['MYSQL_DB'] = 'SACL'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

app.config['JWT_SECRET_KEY'] = 'SuperSecretKeyAccessGalactikMachine(*^#'
jwt = JWTManager(app)

mysql = MySQL(app)

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

@app.route('/login', methods=['POST'])
def login():
    try:
        username = request.json.get('username')
        password = request.json.get('password')

        if username == 'admin' and password == 'BestSecurePassword':
            access_token = create_access_token(identity=username)
            return jsonify({'access_token': access_token}), 200
        else:
            return jsonify({'message': 'Credenciales inválidas'}), 401
    except Exception as e:
        return jsonify({'error': str(e)}), 500

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
        
        if velocidad > 20.00:
            bot = TelegramBot("6399352423:AAG6qacChJxhhR1jvdaVtRJb8YItMz7QJBM", db_config)
            chat_id = '486241032'
            bot.send_message(chat_id='486241032', text=f"*Alerta de alta velocidad:* {velocidad} KM/h")
            bot.send_location(chat_id='486241032', latitude=latitud, longitude=longitud)

        return jsonify({'message': 'Datos guardados correctamente'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
