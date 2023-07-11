from telegram_bot import TelegramBot
from flask import Flask, jsonify, request
from flask_mysqldb import MySQL
from flask_jwt_extended import JWTManager, jwt_required, create_access_token
from flask_cors import CORS  # Importa la biblioteca CORS


app = Flask(__name__)
CORS(app)  # Aplica CORS para todos los recursos

# Configuración de la base de datos
app.config['MYSQL_HOST'] = '127.0.0.1'
app.config['MYSQL_USER'] = 'operator'
app.config['MYSQL_PASSWORD'] = 'SuperSecretPassword$'
app.config['MYSQL_DB'] = 'SACL'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

# Configuración de Flask-JWT-Extended
app.config['JWT_SECRET_KEY'] = 'SuperSecretKeyAccessGalactikMachine(*^#'  # Cambia esto por tu clave secreta real
jwt = JWTManager(app)

mysql = MySQL(app)

@jwt_required  # Protege el método con autenticación JWT
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


@jwt_required  # Protege el método con autenticación JWT
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

        # Verificar las credenciales del usuario (por ejemplo, en una base de datos)
        if username == 'admin' and password == 'BestSecurePassword':
            # Generar un token de acceso JWT válido
            access_token = create_access_token(identity=username)
            return jsonify({'access_token': access_token}), 200
        else:
            return jsonify({'message': 'Credenciales inválidas'}), 401
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@jwt_required
@app.route('/save', methods=['PUT'])
def save_log():
    try:
        data = request.get_json()  # Obtén los datos del cuerpo de la solicitud

        # Extrae los datos
        longitud = data['longitud']
        latitud = data['latitud']
        fecha = data['fecha']
        velocidad = data['velocidad']
        alerta = data['alerta']

        cursor = mysql.connection.cursor()

        # Prepara la sentencia SQL
        query = """
        INSERT INTO road_logs (latitud, longitud, fecha, velocidad, alerta)
        VALUES (%s, %s, %s, %s, %s)
        """
        if velocidad > 5.00:
            bot = TelegramBot('6399352423:AAG6qacChJxhhR1jvdaVtRJb8YItMz7QJBM', '486241032')
            bot.send_message(f'Alerta de velocidad alta: {velocidad}')

        # Ejecuta la sentencia SQL
        cursor.execute(query, (latitud, longitud, fecha, velocidad, alerta))
        mysql.connection.commit()  # Confirma la transacción
        cursor.close()

        return jsonify({'message': 'Datos guardados correctamente'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
    
