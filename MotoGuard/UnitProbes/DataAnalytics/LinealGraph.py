import requests
import pandas as pd
import matplotlib.pyplot as plt

# URL donde se encuentran los datos
url = "http://34.71.210.97:5000/logs"

# Realizamos la petición para obtener los datos
response = requests.get(url)

# Comprobamos que la petición se ha realizado correctamente
if response.status_code == 200:
    data = response.json()

    # Creamos un DataFrame con los datos
    df = pd.DataFrame(data)

    # Convertimos la columna de velocidad a float
    df['velocidad'] = df['velocidad'].astype(float)

    # Calculamos la media móvil de la velocidad
    df['media_movil'] = df['velocidad'].rolling(window=5).mean()

    # Hacemos un gráfico de la media móvil de las velocidades
    plt.figure(figsize=(10, 6))
    plt.plot(df['media_movil'])
    plt.title('Media móvil de velocidades')
    plt.xlabel('Registro')
    plt.ylabel('Velocidad media')
    plt.show()

else:
    print("Error en la petición, código de estado: ", response.status_code)
