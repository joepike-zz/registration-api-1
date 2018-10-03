# Egar Data API v0.1.0

## Clone this repo
```bash
git clone https://github.com/joepike/registration-api-1.git
```

## Create an environment file
```bash
touch .env
```

## Add required environment variable/values to `.flaskenv`
```bash
# the variable values below only work in development mode
FLASK_APP=run.py
FLASK_ENV=development
FLASK_DEBUG=True
FLASK_TESTING=False
DEBUG=True
DBUSER=user
DBPASSWORD=test
DBHOST=database
DBNAME=egar
```

## Build and start docker-compose
```bash
docker-compose up --build
```


## Creating migration files

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
flask db migrate -m "0001"  # creates a migration appending '0001' at the end of the migration name.
...
Generating /code/migrations/versions/ae11a6ca17c5_0001.py ... done 
```
Now it becomes easier to spot the first migration from the second one, etc..


## Running migrations
```bash
flask db upgrade  # runs migration
```


## Runing tests

Make sure docker compose is up and running (if not, please run it).
Then go into the `api` container by executing:
```bash
docker-compose run --rm <container_name> bash
```

To run unittests:
```bash
python -m unittests
```

To run coverage:
```
coverage run --source application --branch -m unittest discover
```

To run coverage html report:
```
coverage html
```
