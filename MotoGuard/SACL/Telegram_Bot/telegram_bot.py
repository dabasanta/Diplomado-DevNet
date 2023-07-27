# Importamos las librerías necesarias
import requests
import json
import time
import mysql.connector
import pandas as pd
import matplotlib.pyplot as plt
import os
from datetime import datetime

# Definimos la clase del bot de Telegram
class TelegramBot:
    def __init__(self, token, db_config):
        self.token = token
        self.base_url = f"https://api.telegram.org/bot{self.token}/"
        self.update_id = 0
        self.db_config = db_config
        self.connection = None

    # Método para obtener actualizaciones del bot
    def get_updates(self):
        url = self.base_url + f"getUpdates?offset={self.update_id + 1}"
        response = requests.get(url)
        return response.json()

    # Método para enviar un mensaje
    def send_message(self, chat_id, text, reply_markup=None):
        url = self.base_url + f"sendMessage?chat_id={chat_id}&text={text}&parse_mode=Markdown"
        if reply_markup:
            url += f"&reply_markup={json.dumps(reply_markup)}"
        response = requests.get(url)
        return response.json()

    # Método para enviar una ubicación
    def send_location(self, chat_id, latitude, longitude):
        url = self.base_url + f"sendLocation?chat_id={chat_id}&latitude={latitude}&longitude={longitude}"
        response = requests.get(url)
        return response.json()

    # Método para enviar una foto
    def send_photo(self, chat_id, photo_path):
        url = self.base_url + f"sendPhoto"
        with open(photo_path, 'rb') as photo:
            files = {'photo': photo}
            data = {'chat_id': chat_id}
            response = requests.post(url, files=files, data=data)
        return response.json()
    
    # Método para resetear el estado del viaje
    def reset_state(self):
        self.ride_start_time = None

    # Método para manejar las actualizaciones recibidas
    def handle_updates(self, updates):
        for update in updates["result"]:
            self.update_id = update["update_id"]
            if "message" in update:
                message = update["message"]
                text = message.get("text")
                chat_id = message["chat"]["id"]
                if text == "/start":
                    keyboard = [[{"text": "Salir a rodar"}, {"text": "Ver estadísticas recientes"}, {"text": "Ver histórico de alertas"}], [{"text": "Ver histórico completo"}]]
                    reply_markup = {"keyboard": keyboard, "one_time_keyboard": True}
                    self.reset_state()
                    self.send_message(chat_id, "¡Hola! Soy MotoGuard, tu seguro al bolante \U0001F3CD ¿Qué quieres hacer hoy? \U0001F600", reply_markup)
                elif text.lower() == "salir a rodar":
                    self.start_ride(chat_id)
                elif text.lower() == "terminar rodada":
                    self.end_ride(chat_id)
                elif text.lower() == "ver estadísticas recientes":
                    self.send_recent_stats(chat_id)
                elif text.lower() == "ver histórico completo":
                    self.send_all_stats(chat_id)
                elif text.lower() == "ver histórico de alertas":
                    self.send_alerts_barchart(chat_id)

    # Método para iniciar un viaje
    def start_ride(self, chat_id):
        keyboard = [[{"text": "Terminar rodada"}]]
        reply_markup = {"keyboard": keyboard, "one_time_keyboard": True}
        
        # Obtener datos climatológicos
        hora_actual = datetime.now().time()
        hora_amanecer = datetime.strptime("06:00:00", "%H:%M:%S").time()
        hora_anochecer = datetime.strptime("18:00:00", "%H:%M:%S").time()
        ciudad = "Barranquilla"
        api_key = "****************" 
        url = f"http://api.openweathermap.org/data/2.5/weather?q={ciudad}&appid={api_key}&units=metric"
        respuesta = requests.get(url)
        datos_clima = respuesta.json()

        if datos_clima["cod"] == 200:
            clima_actual = datos_clima["weather"][0]["description"]
            temperatura_actual = datos_clima["main"]["temp"]
            
            if "rain" in clima_actual.lower():
                self.send_message(chat_id, f"\U0001F6AB ¡Ten cuidado, esta lloviendo en {ciudad} \U0001F327 No olvides llevar impermeable y botas. Recuerda no exceder los limites de velocidad, las llantas pueden resbalar facilmente \U0001F6FC - Temperatura actual: {temperatura_actual} °C", reply_markup)
            elif "clear" in clima_actual.lower():
                self.send_message(chat_id, f"\U0001F324 ¡El clima esta despejado en {ciudad} y hay buena visibilidad \U0001F440 - Temperatura actual: {temperatura_actual} °C", reply_markup)
            elif "sun" in clima_actual.lower() or "sunny" in clima_actual.lower():
                self.send_message(chat_id, f"\U0001F31E ¡El dia esta soleado en {ciudad} \U0001FAE0 y hay buena visibilidad! \U0001F440 - Temperatura actual: {temperatura_actual} °C", reply_markup)

            if hora_amanecer < hora_actual < hora_anochecer:
                self.send_message(chat_id, f"\U0001F6B8 Las calles suelen estar mas congestionadas durante el dia.", reply_markup)
            else:
                self.send_message(chat_id, f"\U0001F31A ¡Nunca olvides encender las luces de tu vehiculo durante la noche! \U0001F4A1", reply_markup)
       
        self.send_message(chat_id, f"\U0001F525 ¡La rodada ha iniciado! Presiona en Terminar Rodada cuando hayas terminado. Estare monitoreando el trafico durante tu recorrido \U0001F441 por lo que no podre entregarte estadisticas durante tu rodada.", reply_markup)
        self.ride_start_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Método para finalizar un viaje
    def end_ride(self, chat_id):
        try:
            if self.ride_start_time:
                ride_end_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                ride_duration = self.calculate_ride_duration(self.ride_start_time, ride_end_time)
                self.connection = mysql.connector.connect(**self.db_config)
                cursor = self.connection.cursor(dictionary=True)

                query = f"""
                SELECT velocidad, alerta
                FROM road_logs
                WHERE fecha BETWEEN '{self.ride_start_time}' AND '{ride_end_time}'
                """
                cursor.execute(query)
                data = cursor.fetchall()

                if not data:
                    retry_query = f"""
                    SELECT velocidad, alerta
                    FROM road_logs
                    WHERE fecha >= '{self.ride_start_time}' AND fecha <= (SELECT MAX(fecha) FROM road_logs)
                    """
                    cursor.execute(retry_query)
                    data = cursor.fetchall()

                    if not data:
                        self.send_message(chat_id, "\U0001F4A4 No hay datos en el período de tiempo de la rodada \U0001F635 Por favor, revise si el sistema está funcionando correctamente. \U0001F9D0 \U0001F50D")
                        return

                speeds = [log['velocidad'] for log in data]
                alerts = [log['alerta'] for log in data]

                incidents_count = alerts.count('incidente')
                max_speed = max(speeds)
                avg_speed = sum(speeds) / len(speeds)

                self.send_message(chat_id, f"¡La rodada ha terminado! Duración: {ride_duration}. \U0001F550")
                self.send_message(chat_id, f"Incidentes generados: {incidents_count} \U0001F4A2")
                self.send_message(chat_id, f"Velocidad máxima: {max_speed} \U0001F5F2")
                self.send_message(chat_id, f"Velocidad promedio: {avg_speed} \U0001F4C9")

                self.ride_start_time = None
            else:
                self.send_message(chat_id, "\U0001F534 No hay una rodada en curso.")
        except AttributeError:
            self.send_message(chat_id, "\U0001F534 No hay una rodada en curso.")
        finally:
            self.ride_start_time = None
        
    # Método para calcular la duración del viaje
    def calculate_ride_duration(self, start_time, end_time):
        start_time = datetime.strptime(start_time, "%Y-%m-%d %H:%M:%S")
        end_time = datetime.strptime(end_time, "%Y-%m-%d %H:%M:%S")
        duration = end_time - start_time
        return str(duration)
    
    # Método para enviar las estadísticas recientes
    def send_recent_stats(self, chat_id):
        if self.connection is None or not self.connection.is_connected():
            self.connection = mysql.connector.connect(**self.db_config)
        cursor = self.connection.cursor(dictionary=True)
        cursor.execute("SELECT velocidad FROM road_logs ORDER BY fecha DESC LIMIT 100")
        data = cursor.fetchall()
        speeds = [record['velocidad'] for record in data]
        avg_speed = sum(speeds) / len(speeds)
        df = pd.DataFrame(speeds, columns=['Speed'])
        plt.figure(figsize=(10, 5))
        df['Speed'].plot(kind='line', grid=True)
        plt.title(f'Promedio de velocidad en los ultimos 100 incidentes: {avg_speed:.2f} km/h')
        plt.xlabel('Registro')
        plt.ylabel('Velocidad (km/h)')
        image_path = '/tmp/recent_speeds.png'
        plt.savefig(image_path)
        if os.path.exists(image_path):
            self.send_photo(chat_id, image_path)

    # Método para enviar todas las estadísticas
    def send_all_stats(self, chat_id):
        if self.connection is None or not self.connection.is_connected():
            self.connection = mysql.connector.connect(**self.db_config)
        cursor = self.connection.cursor(dictionary=True)
        cursor.execute("SELECT fecha, velocidad, alerta FROM road_logs ORDER BY fecha")
        data = cursor.fetchall()
        df = pd.DataFrame(data)
        alerts = df.groupby(df['fecha'].dt.date)['alerta'].count()
        speeds = df.groupby(df['fecha'].dt.date)['velocidad'].mean()
        fig, ax1 = plt.subplots(figsize=(10, 5))
        color = 'tab:red'
        ax1.set_xlabel('Fecha')
        ax1.set_ylabel('Velocidad (km/h)', color=color)
        ax1.plot(speeds.index, speeds, color=color)
        ax1.tick_params(axis='y', labelcolor=color)
        ax2 = ax1.twinx()
        color = 'tab:blue'
        ax2.set_ylabel('Cantidad de alertas', color=color)
        ax2.plot(alerts.index, alerts, color=color)
        ax2.tick_params(axis='y', labelcolor=color)
        fig.tight_layout()
        plt.title('Velocidad y alertas a lo largo del tiempo')
        plt.subplots_adjust(top=0.9)
        image_path = '/tmp/all_stats.png'
        plt.savefig(image_path)
        if os.path.exists(image_path):
            self.send_photo(chat_id, image_path)
    
    # Método para enviar un gráfico de barras de las alertas
    def send_alerts_barchart(self, chat_id):
        if self.connection is None or not self.connection.is_connected():
            self.connection = mysql.connector.connect(**self.db_config)
        cursor = self.connection.cursor(dictionary=True)
        cursor.execute("SELECT fecha FROM road_logs ORDER BY fecha DESC LIMIT 1")
        last_date = cursor.fetchone()['fecha']
        start_date = last_date - pd.Timedelta(days=7)
        query = """
        SELECT fecha, alerta
        FROM road_logs
        WHERE fecha BETWEEN %s AND %s AND alerta IS NOT NULL
        ORDER BY fecha
        """
        cursor.execute(query, (start_date, last_date))
        data = cursor.fetchall()
        df = pd.DataFrame(data)
        df['day'] = df['fecha'].dt.day_name()
        barchart_data = df.groupby('day').size().reset_index(name='count')
        days_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        barchart_data['day'] = pd.Categorical(barchart_data['day'], categories=days_order, ordered=True)
        barchart_data = barchart_data.sort_values('day')
        plt.figure(figsize=(10, 5))
        ax = barchart_data.plot(kind='bar', x='day', y='count', legend=False, color='skyblue')
        plt.title('No. de alertas en los ultimos 7 dias')
        plt.xlabel('Dia de la semana')
        plt.ylabel('Cuenta de incidentes')
        plt.xticks(rotation=90)
        for p in ax.patches:
            ax.annotate(str(p.get_height()), (p.get_x() * 1.005, p.get_height() * 1.005))
        image_path = '/tmp/alerts_barchart.png'
        plt.savefig(image_path)
        if os.path.exists(image_path):
            self.send_photo(chat_id, image_path)

# Método principal
def main():
    db_config = {
        'host': '34.71.210.97',
        'user': 'operator',
        'password': '***************',
        'database': 'SACL'
    }
    bot = TelegramBot("*********:****************", db_config)
    while True:
        updates = bot.get_updates()
        if updates["ok"]:
            bot.handle_updates(updates)
        time.sleep(0.1)

if __name__ == '__main__':
    main()
