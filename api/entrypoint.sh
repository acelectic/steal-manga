#!/bin/bash

echo 'Running migrations...'
python manage.py migrate

echo 'Collecting static files...'
python manage.py collectstatic --no-input

python manage.py runserver 0.0.0.0:8000