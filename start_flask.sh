docker kill flask
docker rm -v flask
docker run -d \
    -p 5000:5000 \
    -e FLASK_APP=run.py \
    -e ENVIRONMENT=development \
    -e DEBUG=True \
    -e TESTING=False \
    -e SECRET_KEY= \
    -e DBUSER=user \
    -e DBPASSWORD=test \
    -e DBHOST=database \
    -e DBNAME=egar \
    --net flask \
    --name flask \
    data-access-api:manual_build \
    /code/wait-for-it.sh $DBHOST $DBUSER $DBPASSWORD $DBNAME
