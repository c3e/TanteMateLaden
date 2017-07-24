# TanteMateLaden
TanteMateLaden is a Mete/Donatr replacement.

This app is built with Django and is currently maintained by CBluoss and fronbasal.


## Installation
### Requirements
  python(3)
  
  virtualenv

### Setup
    git clone TanteMateLaden
    cd TanteMateLaden
    virtualenv venv
    source venv/bin/activate
    pip install -r requirements.txt
    cd TanteMateLaden
    ./manage.py makemigrations
    ./manage.py migrate
    ./manage.py createsuperuser
    ./manage.py loaddata store/fixtures/drinks.json
 
### Run the Server
    ./manage.py runserver
 open http://localhost:8000/
 
 ???
 
 profit
  
