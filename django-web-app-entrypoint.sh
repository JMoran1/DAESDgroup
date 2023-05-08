#!/bin/sh

echo "Waiting for MySQL Database Service to start..."

./wait-for mysql-db:3306

set -e
python manage.py migrate

# Load data into database
if [ ! -f /data_loaded.txt ]; then
    python manage.py loaddata data.json
    touch /data_loaded.txt
fi
python manage.py runserver 0.0.0.0:8000