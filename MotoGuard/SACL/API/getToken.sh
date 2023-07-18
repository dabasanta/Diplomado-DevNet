#!/bin/bash

username="admin"
password="BestSecurePassword"

# URL del endpoint de login
url="http://34.71.210.97:5000/login"

# Datos de la solicitud en formato JSON
data="{\"username\":\"$username\",\"password\":\"$password\"}"

# Realizar la solicitud POST utilizando curl
response=$(curl -s -X POST -H "Content-Type: application/json" -d "$data" "$url")

# Imprimir la respuesta
echo "$response" | jq
