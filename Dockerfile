##########################
# Bulletin
# Based on ubuntu:latest
##########################
FROM ubuntu:latest

MAINTAINER John Lane <john.lane93@gmail.com>

ENV DEBIAN_FRONTEND noninteractive

RUN apt-get update && apt-get install -y python3 python3-pip libpq-dev python3-psycopg2 gunicorn3 \
    && rm -rf /var/lib/apt/lists/*

# Setup django application
COPY . /deploy/app
WORKDIR /deploy/app
RUN pip3 install -r requirements.txt
RUN python3 manage.py collectstatic --no-input

EXPOSE 8080