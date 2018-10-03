#!/bin/bash

set -e

until PGPASSWORD="$DBPASSWORD" psql -h "$DBHOST" -U "$DBUSER" "$DBNAME" -c '\q'; do
    >&2 echo "Postgres is unavailable - sleeping"
    sleep 1
done

# postgres is now accepting connections
>&2 echo "Postgres is up - executing command"

# run migrations
flask db upgrade
# start flask app
python run.py
