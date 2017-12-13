#!/bin/sh

mkdir nsa

sudo docker build -t terafirma .

sudo docker tag terafirma grassrootdocker/terafirma:alpha

sudo docker push grassrootdocker/terafirma:alpha

