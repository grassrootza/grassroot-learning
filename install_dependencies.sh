#!/bin/sh

pip install flask

pip install pymongo

pip install schedule

pip install boto3

pip install rasa_nlu

pip install duckling

pip install git+https://github.com/mit-nlp/MITIE.git

wget -P ./ https://github.com/mit-nlp/MITIE/releases/download/v0.4/MITIE-models-v0.2.tar.bz2

tar xvjf MITIE-models-v0.2.tar.bz2 --directory ./model/
