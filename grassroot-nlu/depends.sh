#!/bin/sh


pip3 install flask

pip3 install googletrans
<<<<<<< HEAD

=======
>>>>>>> circle2-working

pip3 install pymongo

pip3 install schedule

pip3 install boto3

pip3 install rasa_nlu==0.10.6

pip3 install duckling

pip3 install dateparser

pip3 install git+https://github.com/mit-nlp/MITIE.git

pip3 install psutil

[ -f MITIE-models-v0.2.tar.bz2 ] && echo "Requirement already satisfied
 MITIE-models-v0.2.tar.bz2" || wget -P ./ https://github.com/mit-nlp/MITIE/releases/download/v0.4/MITIE-models-v0.2.tar.bz2
 
tar xvjf MITIE-models-v0.2.tar.bz2 --directory ./current_model/model/

sudo rm -r MITIE-models-v0.2.tar.bz2
