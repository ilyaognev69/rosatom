#!/bin/sh

# entrypoint.sh

echo "Waiting for PostgreSQL to be ready..."
while ! nc -z db 5432; do
  sleep 0.1
done

echo "PostgreSQL is ready"

# Применяем миграции и запускаем сервер
python manage.py migrate
python manage.py collectstatic --no-input --clear
exec "$@"