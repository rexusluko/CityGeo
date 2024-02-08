#!/bin/sh
python citygeo/manage.py makemigrations city_api
sleep 15
python citygeo/manage.py migrate
python citygeo/manage.py runserver 0.0.0.0:8000