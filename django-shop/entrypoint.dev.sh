#!/bin/sh

# if [ "$DATABASE" = "postgres" ]
# then
#     echo "Waiting for postgres..."

#     while ! nc -z $SQL_HOST $SQL_PORT; do
#       sleep 0.1
#     done

#     echo "PostgreSQL started"
# fi
# exec "$@"

python manage.py flush --no-input
python manage.py makemigrations
python manage.py migrate


# collect all static files to the root directory
# python manage.py collectstatic --no-input

python manage.py runserver 0.0.0.0:8000

# start the gunicorn worker processws at the defined port
# gunicorn shop_backend.wsgi:application --bind 0.0.0.0:8000 &

# wait