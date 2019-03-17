#!/bin/sh
set -e

# change into app directory (start.sh can not be there because of volume)

# run django setup commands
python manage.py migrate --noinput

# run daphne dev server
python manage.py runserver 0.0.0.0:8000
# daphne asgi.py: