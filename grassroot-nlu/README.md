# Grassroot NLU 

A nlu component that takes in text input and returns parsed entity values.

## Getting Started

Open a terminal in the directory with start_application.py. Enter the following lines as root:

 ~$ bash activate_me.sh

This will start a flask server on 127.0.0.1:5000/
 
Note: For your own convenience, run all commands as root.

To kill the program:

 ~$ bash kill_me.sh


To kill the program:

 ~$ bash kill_me.sh

This will grant you instant, localised.. death. To the program.

### Prerequisites

All dependencies(save for python and mongodb) can be installed by running this in the main directory:

 ~$bash install_dependencies.sh

But if you want to go at it old school then here's the dependency list: 

* DynamoDB or MongoDB (preferably both)
* Python 3.6.1 and its standard library as well as the following additional libraries:
  * pymongo(when using MongoDB)
  * flask
  * rasa_nlu
  * mitie
  * duckling
  * schedule
  * boto3


## Databases

This API uses DynamoDB by default, but this can easily be swapped out for Mongodb by simply opening the config.py file and uncommenting:

 #database = MongoDB

while commenting out
 
 #database = DynamoDB

Note: You'll need to have a MongoDB running in the background to use MongoDB features.


## Deployment

If you already have MITIE-models on your machine, do make sure to set an environment variable called PATH_TO_MITIE and set a post-fix of .../MITIE-models/english/total_word_feature_extractor.dat. For example:

  PATH_TO_MITIE=/home/donnie/MITIE-models/english/total_word_feature_extractor.dat

If you already have the model file and fail to  set the appropriate env var then the API will assume you don't have the models and download(or in this case, redownload) the file for you and set the environment variable as well. You might be wondering whats the big deal. Well not much really, except the file is above 400MB and will slow down initialisation. So if you have the file, please make sure to set the env var.

This API includes an auto-training routine aimed at making the results better over time. This feature may be turned on or off at anytime without affecting the main program. By default, it is turned on upon initialisation. To deactivate auto-training (which commences by default at 00:30 every night),
simply open the activate_me.sh file and comment out:

  python trainer.py > training_output.txt 2>&1 &


## Built With

* [flask](http://flask.pocoo.org/)
* [rasa_nlu](http://rasa.ai/)
* [MongoDB](https://www.mongodb.com/)
* [DynamoDB](https://aws.amazon.com/dynamodb/)
* [Amazon s3](https://aws.amazon.com/s3‎/)


## Authors

* **Luke Jordan** - *Lead developer*

* **FRTNX** - *Apprentice* 


## License

This project is licensed under the BSD-3 Clause License