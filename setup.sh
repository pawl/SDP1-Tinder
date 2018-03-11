echo 'Installing pip requirements'
pip install -r requirements.txt

echo 'Installing bower requirements'
bower install

echo 'Creating private settings to wearhacks_website/settings/private.py'
cp sdp1_tinder/settings/example_private_settings.py sdp1_tinder/settings/private.py

echo 'Setting up database'

python manage.py makemigrations
python manage.py migrate

echo 'Generating dummy data'
python manage.py generate_models 3 3

echo 'Run server'
python manage.py runserver
