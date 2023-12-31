import urequests
import network
from machine import Pin, time_pulse_us, UART
import ujson
import time

# Credenciales de WiFi
ssid = 'SuperSecureNetwork'
password = '*******'

# Conectarse a WiFi
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
if not wlan.isconnected():
    print('Connecting to network...')
    wlan.connect(ssid, password)
    while not wlan.isconnected():
        pass
print('Network connected:', wlan.ifconfig())

# Autenticar con la API y obtener el token de acceso
auth_url = 'http://34.71.210.97:5000/login'
auth_data = {
    "username": "admin",
    "password": "**********"
}
response = urequests.post(auth_url, headers = {'Content-Type': 'application/json'}, data = ujson.dumps(auth_data))
access_token = response.json().get('access_token')
response.close()

# Define los pines para los sensores
TRIG_IZQUIERDO = 21
ECHO_IZQUIERDO = 22
TRIG_DERECHO = 2
ECHO_DERECHO = 4
pin_led1 = Pin(13, Pin.OUT)
pin_led2 = Pin(14, Pin.OUT)

# Configura UART para el GPS
uart = UART(2, baudrate=9600, tx=17, rx=16)

# Crea los objetos de pin
trig_izquierdo = Pin(TRIG_IZQUIERDO, Pin.OUT)
echo_izquierdo = Pin(ECHO_IZQUIERDO, Pin.IN)
trig_derecho = Pin(TRIG_DERECHO, Pin.OUT)
echo_derecho = Pin(ECHO_DERECHO, Pin.IN)

# Crear las variables globales para la velocidad y los datos del GPS
velocidad = None
lat = None
lon = None

# Function to calculate distance
def get_distance(trig, echo):
    trig.value(1)
    time.sleep_us(10)
    trig.value(0)
    duration = time_pulse_us(echo, 1)
    distance = duration * 340.0 / 2.0 / 10000.0
    return distance

def get_formatted_time():
    now = time.localtime()
    return '{:04d}-{:02d}-{:02d} {:02d}:{:02d}:{:02d}'.format(now[0], now[1], now[2], now[3], now[4], now[5])

def main():
    global lat, lon, velocidad

    while True:
        # Get speed data
        if uart.any():
            try:
                gps_data = uart.readline()
                parts = gps_data.decode('ascii').split(',')
                if parts[0] == '$GPVTG':
                    try:
                        velocidad = float(parts[7])
                    except ValueError:
                        print('Datos de velocidad no recibidos')
            except UnicodeError:
                print('Error Unicode en get_speed')

        # Get GPS data
        if uart.any():
            try:
                gps_data = uart.readline()
                parts = gps_data.decode('ascii').split(',')
                if parts[0] == '$GPGGA':
                    try:
                        lat = float(parts[2][:2]) + float(parts[2][2:]) / 60
                        if parts[3] == 'S':
                            lat *= -1
                        lon = float(parts[4][:3]) + float(parts[4][3:]) / 60
                        if parts[5] == 'W':
                            lon *= -1
                    except ValueError:
                        print('Datos de geolocalizacion no recibidos')
            except UnicodeError:
                print('Error Unicode en get_gps')

        # Main function logic
        dist_izquierdo = get_distance(trig_izquierdo, echo_izquierdo)
        dist_derecho = get_distance(trig_derecho, echo_derecho)

        if dist_izquierdo < 10 or dist_derecho < 10:
            print('Distancia menor a 100 CM en el sensor izquierdo' if dist_izquierdo < 100 else 'Distancia menor a 100 CM en el sensor derecho')
            pin_led2.on() if dist_izquierdo < 10 else pin_led1.on()
            time_start = time.time()
            while lat is None or lon is None or velocidad is None:
                print('Buscando GPS')
                time.sleep(0.5)
                if time.time() - time_start > 60:
                    print("Fallo en recopilar los datos del GPS.")
                    break
            if lat is not None and lon is not None and velocidad is not None:
                timestamp = get_formatted_time()
                incident = {
                    "alerta": "incidente",
                    "fecha": timestamp,
                    "latitud": lat,
                    "longitud": lon,
                    "velocidad": velocidad
                }
                print(ujson.dumps(incident))

                # URL de la API a la que enviarás la solicitud POST
                url = 'http://34.71.210.97:5000/save_log'

                # Enviar solicitud PUT
                response = urequests.post(url, headers = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + access_token}, data = ujson.dumps(incident))

                # Comprueba el código de estado de la respuesta
                if response.status_code < 400:
                    print('Incidente enviado con éxito.')
                else:
                    print('Error al enviar el incidente: {}'.format(response.status_code))
                response.close()
                pin_led2.off() if dist_izquierdo < 10 else pin_led1.off()

        time.sleep(0.5)

# Start the main function
main()
