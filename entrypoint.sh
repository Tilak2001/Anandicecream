#!/bin/sh
set -e

echo "Waiting for PostgreSQL..."
until python -c "
import os, psycopg2
psycopg2.connect(
    dbname=os.getenv('DB_NAME','anand_ice_cream'),
    user=os.getenv('DB_USER','postgres'),
    password=os.getenv('DB_PASSWORD',''),
    host=os.getenv('DB_HOST','db'),
    port=os.getenv('DB_PORT','5432')
)
" 2>/dev/null; do
  echo "  postgres not ready, retrying in 2s..."
  sleep 2
done
echo "PostgreSQL is up!"

echo "Running migrations..."
python manage.py migrate --noinput

echo "Starting Gunicorn on 0.0.0.0:8050..."
exec gunicorn anand_ice_cream.wsgi:application \
    --bind 0.0.0.0:8050 \
    --workers 3 \
    --timeout 120
