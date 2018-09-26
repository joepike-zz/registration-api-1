FROM python:3.7

ENV PYTHONUNBUFFERED 1
ENV FLASK_APP=${FLASK_APP}
ENV ENVIRONMENT=${ENVIRONMENT}
ENV DEBUG=${DEBUG}
ENV TESTING=${TESTING}
ENV SECRET_KEY=${SECRET_KEY}
ENV DBUSER=${DBUSER}
ENV DBPASSWORD=${DBPASSWORD}
ENV DBHOST=${DBHOST}
ENV DBNAME=${DBNAME}

RUN apt-get update && \
    apt-get -y install --no-install-recommends \
    python3-dev \
    libmemcached11 \
    libmemcached-dev \
    apt-utils \
    postgresql-client

COPY ./src /code
ADD requirements.txt /requirements.txt

RUN pip install --upgrade pip && \
    pip install --upgrade pdbpp && \
    pip install -r /requirements.txt

RUN adduser --disabled-password -u 1000 flaskuser
RUN chown -R flaskuser /code
USER 1000

WORKDIR /code

ENTRYPOINT [ "/code/wait-for-it.sh" ]
