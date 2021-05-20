#!/bin/sh

# python manage.py flush --no-input
python manage.py 
#python manage.py collectstatic --no-input --clear

exec "$@"
