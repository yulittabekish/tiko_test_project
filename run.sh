#!/bin/bash
echo "Running migrations"
python manage.py migrate --noinput
echo "Starting DJANGO"
python manage.py runserver 0.0.0.0:8000