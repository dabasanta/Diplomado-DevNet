import requests
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import geopandas as gpd
import folium
from folium.plugins import HeatMap

# URL donde se encuentran los datos
url = "http://34.71.210.97:5000/logs"

# Realizamos la petición para obtener los datos
response = requests.get(url)

# Comprobamos que la petición se ha realizado correctamente
if response.status_code == 200:
    data = response.json()

    # Creamos un DataFrame con los datos
    df = pd.DataFrame(data)

    # Convertimos las columnas necesarias a los tipos correspondientes
    df['velocidad'] = df['velocidad'].astype(float)
    df['latitud'] = df['latitud'].astype(float)
    df['longitud'] = df['longitud'].astype(float)

    # Creamos un gráfico de dispersión con la velocidad y la fecha, con diferentes colores para las diferentes alertas
    plt.figure(figsize=(10, 6))
    sns.scatterplot(data=df, x='fecha', y='velocidad', hue='alerta')
    plt.title('Velocidad de los incidentes en función del tiempo')
    plt.xlabel('Fecha')
    plt.ylabel('Velocidad')
    plt.show()

    # Creamos un mapa de calor con los datos de latitud y longitud
    # Primero creamos un GeoDataFrame
    gdf = gpd.GeoDataFrame(df, geometry=gpd.points_from_xy(df.longitud, df.latitud))

    # Creamos el mapa base
    m = folium.Map([df['latitud'].mean(), df['longitud'].mean()], zoom_start=10)

    # Añadimos el mapa de calor
    HeatMap(data=gdf[['latitud', 'longitud']].groupby(['latitud', 'longitud']).sum().reset_index().values.tolist(), radius=8, max_zoom=13).add_to(m)

    # Mostramos el mapa
    m

else:
    print("Error en la petición, código de estado: ", response.status_code)
