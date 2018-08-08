FROM tiangolo/uwsgi-nginx-flask:python3.6-alpine3.7

WORKDIR /app

RUN apk add --no-cache alpine-sdk

ADD ./grassroot-nlu /app

RUN sh depends.sh

ENV LANG en_US.UTF-8  
ENV LANGUAGE en_US:en  
ENV LC_ALL en_US.UTF-8