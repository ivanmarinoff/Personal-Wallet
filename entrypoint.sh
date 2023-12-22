#!/bin/sh

echo "Install the dependencies"
pip install -r requirements.txt


echo "Running Database Migrations"
python manage.py makemigrations
python manage.py migrate

echo "Running app commands"
python manage.py collectstatic --noinput
python manage.py runserver &
exec "$@"