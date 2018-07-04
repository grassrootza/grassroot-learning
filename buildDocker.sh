#!/bin/sh
timestamp() {
  date +"%T"
}

sudo docker build -t terafirma .

sudo docker tag terafirma grassrootdocker/terafirma:timestamp

sudo docker push grassrootdocker/terafirma:timestamp
