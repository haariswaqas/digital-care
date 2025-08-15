#!/bin/sh

# Exit on error
set -e

# Wait for PostgreSQL to be ready
echo "Waiting for DigitalCare PostgreSQL..."
while ! nc -z $POSTGRES_HOST $POSTGRES_PORT; do
  sleep 1
done
echo "DigitalCare PostgreSQL is up!"

# Apply migrations and collect static files
python manage.py migrate
python manage.py collectstatic --noinput

exec "$@"
