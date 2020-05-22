# PASKAL

A powerful full-featured persian Q&A website

## Demo

You can see a demo [here](https://paskal.herokuapp.com/action/questions)

## Install Prerequisites

First thing, you need postgresql

```bash
sudo apt-get install libpq-dev python3-dev
sudo apt-get install postgresql postgresql-contrib
```

Also create a database an user

```bash
CREATE DATABASE paskal;
CREATE USER paskal_user WITH ENCRYPTED PASSWORD 'secure_pass';
ALTER ROLE paskal_user SET client_encoding TO 'utf8';
ALTER ROLE paskal_user SET default_transaction_isolation TO 'read committed';
ALTER ROLE paskal_user SET timezone TO 'UTC';
ALTER USER paskal_user CREATEDB;
GRANT ALL PRIVILEGES ON DATABASE paskal TO paskal_user;
```

## Run The Project

```bash
cd Paskal
python3 -m venv .env
source .env/bin/activate
pip install -r requirements.txt
cd paskal
python manage.py migrate
python manage.py runserver
```

The website is then up and running at <http://localhost:8000>

## Test The Project

```bash
cd paskal
coverage run manage.py test -v 2
```
There are some test that use selenium, if you want to run them:
first download [appropriate chromedriver](https://chromedriver.chromium.org/downloads) and put in the path ```/usr/bin/chromedirver```.

Then enable the tests by setting ```SELENIUM_TESTS``` to ```True``` in settings.py file and finally run the test with the command above.
