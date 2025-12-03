#!/bin/bash

set -e

echo "Rodando Migrations..."
python manage.py migrate

echo "Coletando arquivos estáticos..."
python manage.py collectstatic --noinput

echo "Iniciando Celery Worker..."
celery -A core worker --loglevel=info --concurrency=1 &

# Define a porta como 10000 se a variável $PORT não existir
PORT=${PORT:-10000}

echo "Iniciando Gunicorn na porta $PORT..."
gunicorn core.wsgi:application --bind 0.0.0.0:$PORT
