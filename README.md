# Egar Data API v0.1.0

## Clone this repo
```bash
git clone x
```

## Create an environment file
```bash
touch .flaskenv
```

## Add required environment variable/values to `.flaskenv`
```bash
# the variable values below only work in development mode
FLASK_APP=run.py
ENVIRONMENT=development
DEBUG=True
SECRET_KEY=2sfjaADF!$%#$AFAS23r
DBUSER=user
DBPASSWORD=test
DBHOST=database
DBNAME=egar
```

## Build and start docker-compose
```bash
docker-compose up --build
```

## Running migrations
Make sure docker compose is up and running (if not, please run it).
To go into the `api` container execute:
```bash
docker-compose run --rm <container_name> bash
```
Once in the container execute:
```bash
flask db upgrade
```

## Creating migrations

Make sure docker compose is up and running (if not, please run it).
To go into the `api` container execute:
```bash
docker-compose run --rm <container_name> bash
```

When creating migrations Flask-Migrate assigns an hash string as the migration name, for example:
```bash
flask db migrate
...
Generating /code/migrations/versions/ae11a6ca17c5.py ... done
```
So far so good, but if you have 20 migrations how do you know which one is the first one without going into every single migration?

This said, its probably a good idea to add an index as a message when creating migrations, for example:
```bash
flask db migrate -m "0001"  # adds '0001' at the end of the migration name.
...
Generating /code/migrations/versions/ae11a6ca17c5_0001.py ... done 
```
Now it becomes easier to spot the first migration from the second one, etc..
