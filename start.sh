#!/bin/bash

# Build
docker build -t data-access-api:manual_build .

# Remove all stale stuff
docker kill flask
docker kill database
docker rm -v flask
docker rm -v database

# Start DB
docker run -d \
    -p 5432:5432 \
    -e LC_ALL=C.UTF-8 \
    -e POSTGRES_USER=user \
    -e POSTGRES_PASSWORD=test \
    -e POSTGRES_DB=egar \
    --name database \
    --net flask \
    postgres:10.4

# Start flask app
docker run -d \
    -p 5000:5000 \
    -e FLASK_APP=run.py \
    -e FLASK_ENV=development \
    -e FLASK_DEBUG=True \
    -e FLASK_TESTING=False \
    -e DBUSER=user \
    -e DBPASSWORD=test \
    -e DBHOST=database \
    -e DBNAME=egar \
    --net flask \
    --name flask \
    data-access-api:manual_build \
    /code/wait-for-it.sh $DBHOST $DBUSER $DBPASSWORD $DBNAME
