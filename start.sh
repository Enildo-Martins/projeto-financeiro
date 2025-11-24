#!/bin/bash

# Sai do script se qualquer comando der erro
set -e

echo "Rodando Migrations..."
python manage.py migrate

echo "Iniciando Gunicorn..."
# O Render injeta a variável PORT automaticamente
gunicorn core.wsgi:application --bind 0.0.0.0:$PORT