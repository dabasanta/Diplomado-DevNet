# Bot Telegram

El Bot de Telegram tiene capacidades sofisticadas para interactuar con los usuarios, recopilar y analizar datos en tiempo real y en histórico, y proporcionar información y alertas útiles en función de las condiciones y los patrones observados.

## Comandos predefinidos

El Bot de Telegram responde a comandos específicos, los cuales serán dispuestos al usuario por medio de un teclado interactivo. El método que se encarga de manejar estos comandos es el siguiente:

```python
def handle_updates(self, updates):
    # La función handle_updates recibe un objeto "updates" que contiene información sobre las actualizaciones recibidas del chat de Telegram.
    for update in updates["result"]:
        # Se itera sobre cada actualización contenida en el objeto "updates".
        self.update_id = update["update_id"]
        # Se actualiza el ID de la última actualización procesada para evitar el procesamiento repetido de la misma.

        if "message" in update:
            # Se verifica si la actualización contiene un mensaje.

            message = update["message"]
            # Se obtiene el contenido del mensaje.

            text = message.get("text")
            # Se intenta obtener el texto del mensaje, si existe. De lo contrario, text será None.

            chat_id = message["chat"]["id"]
            # Se obtiene el ID del chat donde se envió el mensaje.

            if text == "/start":
                # Si el texto del mensaje es "/start":

                keyboard = [
                    [{"text": "Salir a rodar"}, {"text": "Ver estadísticas recientes"}, {"text": "Ver histórico de alertas"}],
                    [{"text": "Ver histórico completo"}]
                ]
                # Se crea un teclado personalizado con diferentes opciones.

                reply_markup = {"keyboard": keyboard, "one_time_keyboard": True}
                # Se define el markup del teclado para mostrar las opciones al usuario.

                self.reset_state()
                # Se llama a una función interna "reset_state" que reinicia el estado interno del bot.

                self.send_message(chat_id, "¡Hola! Soy MotoGuard, tu seguro al volante \U0001F3CD ¿Qué quieres hacer hoy? \U0001F600", reply_markup)
                # Se envía un mensaje de bienvenida al chat con el teclado personalizado.

            elif text.lower() == "salir a rodar":
                self.start_ride(chat_id)
                # Si el texto del mensaje coincide con "salir a rodar", se llama a la función interna "start_ride".

            elif text.lower() == "terminar rodada":
                self.end_ride(chat_id)
                # Si el texto del mensaje coincide con "terminar rodada", se llama a la función interna "end_ride".

            elif text.lower() == "ver estadísticas recientes":
                self.send_recent_stats(chat_id)
                # Si el texto del mensaje coincide con "ver estadísticas recientes", se llama a la función interna "send_recent_stats".

            elif text.lower() == "ver histórico completo":
                self.send_all_stats(chat_id)
                # Si el texto del mensaje coincide con "ver histórico completo", se llama a la función interna "send_all_stats".

            elif text.lower() == "ver histórico de alertas":
                self.send_alerts_barchart(chat_id)
                # Si el texto del mensaje coincide con "ver histórico de alertas", se llama a la función interna "send_alerts_barchart".
```

Este código es una implementación de cómo el Bot "`MotoGuard`" maneja las actualizaciones de mensajes recibidos en Telegram y cómo responde a comandos específicos enviados por los usuarios. Cada comando específico desencadena una acción particular dentro del Bot, lo que permite que los usuarios interactúen con él y realicen diversas acciones relacionadas con las actividades de conducción.

## Capacidades del Bot de Telegram

## Envío de estadísticas

### Estadísticas recientes

![Untitled](Bot%20Telegram%20539489482da44c7db91a0b8b0d6914c0/Untitled.png)

```python
def send_recent_stats(self, chat_id):
    # Esta función se encarga de enviar estadísticas recientes de velocidad al chat de Telegram con el ID especificado.

    if self.connection is None or not self.connection.is_connected():
        self.connection = mysql.connector.connect(**self.db_config)
    # Se verifica si hay una conexión activa a la base de datos. Si no hay una conexión, se establece una nueva utilizando los parámetros de configuración.

    cursor = self.connection.cursor(dictionary=True)
    # Se crea un cursor para ejecutar consultas a la base de datos con resultados en formato de diccionario.

    cursor.execute("SELECT velocidad FROM road_logs ORDER BY fecha DESC LIMIT 100")
    # Se realiza una consulta SQL para obtener las últimas 100 velocidades registradas, ordenadas por fecha.

    data = cursor.fetchall()
    # Se recuperan los resultados de la consulta.

    speeds = [record['velocidad'] for record in data]
    # Se crea una lista con las velocidades extraídas de los registros.

    avg_speed = sum(speeds) / len(speeds)
    # Se calcula el promedio de velocidad.

    df = pd.DataFrame(speeds, columns=['Speed'])
    # Se crea un DataFrame de pandas con las velocidades para generar la gráfica.

    plt.figure(figsize=(10, 5))
    # Se define el tamaño de la figura de la gráfica.

    df['Speed'].plot(kind='line', grid=True)
    # Se genera una gráfica de líneas utilizando las velocidades.

    plt.title(f'Promedio de velocidad en los últimos 100 incidentes: {avg_speed:.2f} km/h')
    plt.xlabel('Registro')
    plt.ylabel('Velocidad (km/h)')
    # Se agregan etiquetas y título a la gráfica.

    image_path = '/tmp/recent_speeds.png'
    # Se define la ruta donde se guardará la imagen de la gráfica.

    plt.savefig(image_path)
    # Se guarda la gráfica como una imagen en la ruta especificada.

    if os.path.exists(image_path):
        self.send_photo(chat_id, image_path)
        # Si la imagen existe, se envía al chat de Telegram utilizando la función interna "send_photo".
```

### Historico de alertas

![Untitled](Bot%20Telegram%20539489482da44c7db91a0b8b0d6914c0/Untitled%201.png)

```python
def send_all_stats(self, chat_id):
    # Esta función se encarga de enviar todas las estadísticas de velocidad y alertas a lo largo del tiempo al chat de Telegram con el ID especificado.

    if self.connection is None or not self.connection.is_connected():
        self.connection = mysql.connector.connect(**self.db_config)
    # Se verifica si hay una conexión activa a la base de datos. Si no hay una conexión, se establece una nueva utilizando los parámetros de configuración.

    cursor = self.connection.cursor(dictionary=True)
    # Se crea un cursor para ejecutar consultas a la base de datos con resultados en formato de diccionario.

    cursor.execute("SELECT fecha, velocidad, alerta FROM road_logs ORDER BY fecha")
    # Se realiza una consulta SQL para obtener todas las fechas, velocidades y alertas registradas, ordenadas por fecha.

    data = cursor.fetchall()
    # Se recuperan los resultados de la consulta.

    df = pd.DataFrame(data)
    # Se crea un DataFrame de pandas con los datos para generar las gráficas.

    alerts = df.groupby(df['fecha'].dt.date)['alerta'].count()
    speeds = df.groupby(df['fecha'].dt.date)['velocidad'].mean()
    # Se agrupan los datos por fecha para obtener la cantidad de alertas y el promedio de velocidad en cada fecha.

    fig, ax1 = plt.subplots(figsize=(10, 5))
    # Se crea una figura y dos ejes para mostrar las dos gráficas.

    color = 'tab:red'
    ax1.set_xlabel('Fecha')
    ax1.set_ylabel('Velocidad (km/h)', color=color)
    ax1.plot(speeds.index, speeds, color=color)
    ax1.tick_params(axis='y', labelcolor=color)
    # Se configura el primer eje y se muestra la gráfica de velocidad.

    ax2 = ax1.twinx()
    color = 'tab:blue'
    ax2.set_ylabel('Cantidad de alertas', color=color)
    ax2.plot(alerts.index, alerts, color=color)
    ax2.tick_params(axis='y', labelcolor=color)
    # Se crea el segundo eje y se muestra la gráfica de alertas.

    fig.tight_layout()
    # Se ajusta la disposición de las gráficas para evitar superposiciones.

    plt.title('Velocidad y alertas a lo largo del tiempo')
    plt.subplots_adjust(top=0.9)
    # Se agrega un título general a las gráficas y se ajusta la posición del título.

    image_path = '/tmp/all_stats.png'
    # Se define la ruta donde se guardará la imagen de las gráficas.

    plt.savefig(image_path)
    # Se guarda la figura como una imagen en la ruta especificada.

    if os.path.exists(image_path):
        self.send_photo(chat_id, image_path)
        # Si la imagen existe, se envía al chat de Telegram utilizando la función interna "send_photo".
```

### Historial completo

![Untitled](Bot%20Telegram%20539489482da44c7db91a0b8b0d6914c0/Untitled%202.png)

```python
def send_alerts_barchart(self, chat_id):
    # Esta función se encarga de enviar un gráfico de barras con el número de alertas registradas en los últimos 7 días al chat de Telegram con el ID especificado.

    if self.connection is None or not self.connection.is_connected():
        self.connection = mysql.connector.connect(**self.db_config)
    # Se verifica si hay una conexión activa a la base de datos. Si no hay una conexión, se establece una nueva utilizando los parámetros de configuración.

    cursor = self.connection.cursor(dictionary=True)
    # Se crea un cursor para ejecutar consultas a la base de datos con resultados en formato de diccionario.

    cursor.execute("SELECT fecha FROM road_logs ORDER BY fecha DESC LIMIT 1")
    # Se realiza una consulta SQL para obtener la fecha más reciente registrada en los logs.

    last_date = cursor.fetchone()['fecha']
    # Se recupera la fecha más reciente.

    start_date = last_date - pd.Timedelta(days=7)
    # Se calcula la fecha de inicio para los últimos 7 días.

    query = """
    SELECT fecha, alerta
    FROM road_logs
    WHERE fecha BETWEEN %s AND %s AND alerta IS NOT NULL
    ORDER BY fecha
    """
    # Se define una consulta SQL para obtener las fechas y alertas de los registros en el rango de los últimos 7 días.

    cursor.execute(query, (start_date, last_date))
    # Se ejecuta la consulta con las fechas de inicio y fin como parámetros.

    data = cursor.fetchall()
    # Se recuperan los resultados de la consulta.

    df = pd.DataFrame(data)
    # Se crea un DataFrame de pandas con los datos para generar el gráfico de barras.

    df['day'] = df['fecha'].dt.day_name()
    # Se agrega una columna con el nombre del día de la semana correspondiente a cada fecha.

    barchart_data = df.groupby('day').size().reset_index(name='count')
    # Se agrupan los datos por día de la semana y se cuenta la cantidad de alertas en cada día.

    days_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    barchart_data['day'] = pd.Categorical(barchart_data['day'], categories=days_order, ordered=True)
    barchart_data = barchart_data.sort_values('day')
    # Se ordenan los datos por día de la semana en orden cronológico.

    plt.figure(figsize=(10, 5))
    # Se define el tamaño de la figura del gráfico de barras.

    ax = barchart_data.plot(kind='bar', x='day', y='count', legend=False, color='skyblue')
    # Se genera un gráfico de barras utilizando los datos.

    plt.title('No. de alertas en los últimos 7 días')
    plt.xlabel('Día de la semana')
    plt.ylabel('Cuenta de incidentes')
    plt.xticks(rotation=90)
    # Se agregan etiquetas y título a la gráfica.

    for p in ax.patches:
        ax.annotate(str(p.get_height()), (p.get_x() * 1.005, p.get_height() * 1.005))
    # Se agregan etiquetas en las barras para mostrar el valor numérico correspondiente.

    image_path = '/tmp/alerts_barchart.png'
    # Se define la ruta donde se guardará la imagen del gráfico de barras.

    plt.savefig(image_path)
    # Se guarda el gráfico como una imagen en la ruta especificada.

    if os.path.exists(image_path):
        self.send_photo(chat_id, image_path)
        # Si la imagen existe, se envía al chat de Telegram utilizando la función interna "send_photo".
  
```
