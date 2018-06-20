#!/bin/sh

sudo docker build -t terafirma .

sudo docker tag terafirma grassrootdocker/terafirma:skywalker

sudo docker push grassrootdocker/terafirma:skywalker
