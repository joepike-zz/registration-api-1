FROM python:3
ENV PYTHONUNBUFFERED 1
RUN mkdir /code
RUN adduser -D -u 1000 flaskuser
RUN chown -R flaskuser /code
USER 1000
WORKDIR /code
ADD requirements.txt /code/

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
