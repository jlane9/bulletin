##########################
# Bulletin
# Based on python:3
##########################
FROM python:3

MAINTAINER John Lane <john.lane93@gmail.com>

ENV DEBIAN_FRONTEND noninteractive
ENV PYTHONUNBUFFERED=1

RUN apt-get update && apt-get install -y libpq-dev python3-psycopg2 gunicorn \
    && rm -rf /var/lib/apt/lists/*

# Setup django application
COPY . /deploy/app
WORKDIR /deploy/app
RUN pip install -r requirements.txt
RUN python manage.py collectstatic --no-input

EXPOSE 8080