docker run -d \
    -p 5432:5432 \
    -e LC_ALL=C.UTF-8 \
    -e POSTGRES_USER=user \
    -e POSTGRES_PASSWORD=test \
    -e POSTGRES_DB=egar \
    --name database \
    --net flask \
    postgres:10.4
