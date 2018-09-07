#!/bin/bash

echo "Activate virtual env"
source activate gr-rasa

echo "Training NLU models"
make train-nlu

echo "Training core"
make train-core

echo "Building image and tagging"
docker build -t grassroot-rasa:latest .
docker tag grassroot-rasa:latest 257542705753.dkr.ecr.eu-west-1.amazonaws.com/grassroot-rasa:latest

echo "Logging in to ECR and pushing"
eval $(aws ecr get-login --no-include-email --region eu-west-1)
docker push 257542705753.dkr.ecr.eu-west-1.amazonaws.com/grassroot-rasa:latest

echo "Exiting virtual env"
source deactivate
