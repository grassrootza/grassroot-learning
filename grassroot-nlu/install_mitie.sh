#!/bin/sh


[ -f MITIE-models-v0.2.tar.bz2 ] && echo "Requirement already satisfied
 MITIE-models-v0.2.tar.bz2" || wget -P ./ https://github.com/mit-nlp/MITIE/releases/download/v0.4/MITIE-models-v0.2.tar.bz2
 

tar xvjf MITIE-models-v0.2.tar.bz2 --directory ./current_model/model/

sudo rm -r MITIE-models-v0.2.tar.bz2