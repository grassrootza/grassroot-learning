#!/bin/sh


pip3 install flask


pip3 install pymongo


pip3 install schedule


pip3 install boto3


pip3 install rasa_nlu==0.10.6


pip3 install duckling==1.7.3


pip3 install dateparser==0.6.0


pip3 install git+https://github.com/mit-nlp/MITIE.git


pip3 install psutil

pip3 install boto3

[ -f MITIE-models-v0.2.tar.bz2 ] && echo "Requirement already satisfied
 MITIE-models-v0.2.tar.bz2" || wget -P ./ https://github.com/mit-nlp/MITIE/releases/download/v0.4/MITIE-models-v0.2.tar.bz2
 

tar xvjf MITIE-models-v0.2.tar.bz2 --no-same-owner --directory ./model/

