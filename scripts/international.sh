#!/bin/bash

export PYTHONPATH="${PYTHONPATH}:`pwd`"
echo "Python path: ${PYTHONPATH}"
export DJANGO_SETTINGS_MODULE=app.settings
echo "Django settings module: ${DJANGO_SETTINGS_MODULE}"
echo $PATH

echo "Make messages in root dir `pwd`"
pwd
django-admin makemessages -x js -l fr --settings=${DJANGO_SETTINGS_MODULE}
cd app
mkdir -p locale

echo "Make messages in app dir `pwd`"
django-admin makemessages -x js -l fr --settings=${DJANGO_SETTINGS_MODULE}

cd ../static/js
echo "Make messages in dir `pwd`"
django-admin makemessages -d djangojs -l fr --settings=${DJANGO_SETTINGS_MODULE}

cd ../..
echo "Compile messages in dir `pwd`"
django-admin compilemessages --settings=${DJANGO_SETTINGS_MODULE}
python manage.py runserver
