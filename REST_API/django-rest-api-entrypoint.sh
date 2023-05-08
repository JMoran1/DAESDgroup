#!/bin/sh

echo "Waiting for MySQL Database Service to start..."

./wait-for mysql-db:3306

python manage.py migrate
python manage.py runserver 0.0.0.0:8001