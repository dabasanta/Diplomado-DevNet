#!/bin/bash

# Variables de autenticación
username="admin"
password="BestSecurePassword"
data="{\"username\":\"$username\",\"password\":\"$password\"}"

# Obtener el token de autorización
token=$(curl -s -X POST -H "Content-Type: application/json" -d "$data" http://34.71.210.97:5000/login | awk -F'"' '{print $4}')

# Datos a enviar
datos='{"alerta":"incidente","fecha":"2023-06-24 00:00:00","latitud":"10.986700","longitud":"-74.805000","velocidad":80.6}'

# Enviar la solicitud POST a la API
curl -s -X POST -H "Content-Type: application/json" -H "Authorization: Bearer $token" -d "$datos" http://34.71.210.97:5000/save_log | jq
