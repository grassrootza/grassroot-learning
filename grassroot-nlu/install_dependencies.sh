#!/bin/sh

sudo apt-get update

if hash pip; then 
    echo "pip is installed"
else
    sudo apt install python3-pip
fi

if hash git; then 
    echo "git is installed"
else
    sudo apt install git
fi

# conda install libgcc

# jvm

pip3 install flask


pip3 install pymongo


pip3 install schedule


pip3 install boto3


pip3 install rasa_nlu


pip3 install duckling


pip3 install git+https://github.com/mit-nlp/MITIE.git


pip3 install psutil


[ -f MITIE-models-v0.2.tar.bz2 ] && echo "Requirement already satisfied
 MITIE-models-v0.2.tar.bz2" || wget -P ./ https://github.com/mit-nlp/MITIE/releases/download/v0.4/MITIE-models-v0.2.tar.bz2
 

tar xvjf MITIE-models-v0.2.tar.bz2 --directory ./model/


if hash aws; then
    echo "aws is installed.
    You're ready to go. Run 'sudo bash activate_me.sh' to fire up the API."
else
	sudo apt install awscli;
	echo "Your AWS credentials are not configured.
	Please run 'aws configure' and enter the associated details."
fi