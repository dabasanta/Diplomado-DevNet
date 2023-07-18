import requests

#
# Sencilla implementacion del bot de telegram que sera llamado desde la API cuando las condiciones se cumplan, inicialmente para laspruebas se usara la condicion de que la velocidad sea mayor a 5 KM/h para que se sea ejecutado el bot y se envie un mensaje al usuario.
#

class TelegramBot:
    def __init__(self, token, chat_id):
        self.token = token
        self.chat_id = chat_id
        self.base_url = f"https://api.telegram.org/bot{self.token}/"

    def send_message(self, message):
        url = self.base_url + f"sendMessage?chat_id={self.chat_id}&text={message}"
        response = requests.get(url)
        return response.json()
