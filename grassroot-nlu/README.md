# Grassroot NLU 

A nlu component that takes in text input and returns parsed entity values.

## Getting Started

Open a terminal in the directory with start_application.py. Enter the following lines as root:

 ~$ export AUTH_TOKEN='enter your feersum authorisation token'

 ~$ sudo bash activate_me.sh

This will start a flask server on 0.0.0.0:5000/ (where '0.0.0.0' is the hosts machine's ip)
 
Note: For your own convenience, sudo all commands.

To kill the program:

 ~$ sudo bash kill_me.sh


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

After running $ bash install_dependencies.sh and $ bash activate_me.sh you should be good to go. Just make sure that your database is up and running (esp. when using MongoDB or a local instance of DynamoDB)

This API includes an auto-training routine aimed at making the results better over time. This feature may be turned on or off at anytime without affecting the main program. By default, it is turned on upon initialisation. To deactivate auto-training (which commences by default at 00:30 every night),
simply open the activate_me.sh file and comment out:

 python trainer.py > training_output.txt 2>&1 &

Then run:

 $ sudo bash restart.sh


## Built With

* [flask](http://flask.pocoo.org/)
* [rasa_nlu](http://rasa.ai/)
* [MongoDB](https://www.mongodb.com/)
* [DynamoDB](https://aws.amazon.com/dynamodb/)
* [Amazon s3](https://aws.amazon.com/s3‎/)


# DateTime parser

This API also includes a date-time parser for formalising date values. For example an input of 'tomorrow at 5 in the evening' will return 'YYYY-MM-DDT17:00'.
To call this API and pass values to it:

  /parse?date_string=tomorrow at 5 in the evening

The base url is http://hostmachineIP where 'hostmachineIP' is as advertised, your host machines IP. To utilise this service you will need to have a Feersum nlu authorisation token. See [here](http://feersum.io/).


## Authors

* **Luke Jordan** - *Lead developer*

* **FRTNX** - *Apprentice* 


## License

This project is licensed under the BSD-3 Clause License