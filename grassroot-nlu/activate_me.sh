#!/bin/sh


# Docker aws configurtion
#export AWS_ACCESS_KEY_ID=INCASEYOUNEEDAPROTIP
#export AWS_SECRET_ACCESS_KEY=THESEARENOTREALKEYS
#export AWS_DEFAULT_REGION=eu-west-1
#export AWS_DEFAULT_OUTPUT=json 
#aws ecr get-login --region eu-west-1


export FLASK_APP=start_application.py
flask run --host=0.0.0.0 > output.txt 2>&1 &
python trainer.py > training_output.txt 2>&1 &
python checker.py > system_status.txt 2>&1 &
tail -f output.txt
