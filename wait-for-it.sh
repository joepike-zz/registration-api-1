#!/bin/bash

set -e
host="$1"      # database
user="$2"      # user
pass="$3"      # test
database="$4"  # egar
shift

until PGPASSWORD="$pass" psql -h "$host" -U "$user" "$database" -c '\q'; do
    >&2 echo "Postgres is unavailable - sleeping"
    sleep 1
done

# postgres is now accepting connections
>&2 echo "Postgres is up - executing command"

# start flask app
python run.py
