FROM python:3.7
ENV PYTHONUNBUFFERED 1
RUN mkdir /code
WORKDIR /code
ADD requirements.txt /code/

ENV FLASK_APP=${FLASK_APP}
ENV FLASK_ENV=${FLASK_ENV}
ENV FLASK_DEBUG=${FLASK_DEBUG}
ENV FLASK_TESTING=${FLASK_TESTING}
ENV DBHOST=${DBHOST}
ENV DBNAME=${DBNAME}
ENV DBUSER=${DBUSER}
ENV DBPASSWORD=${DBPASSWORD}

RUN apt-get update && \
    apt-get -y install --no-install-recommends \
    python3-dev \
    libmemcached11 \
    libmemcached-dev \
    apt-utils \
    postgresql-client
RUN pip install --upgrade pip && \
    pip install --upgrade pdbpp && \
    pip install -r requirements.txt

ADD . /code/
