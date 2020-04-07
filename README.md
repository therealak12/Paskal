# PASKAL

A powerful full-featured persian Q&A website

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
GRANT ALL PRIVILEGES ON DATABASE paskal TO paskal_user;
```

## Run The Project

```bash
cd Paskal
python3 -m venv .env
source .env/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

The website is then up and running at <http://localhost:8000>
