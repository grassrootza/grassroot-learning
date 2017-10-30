# Grassroot NLU 

A nlu component that takes in text input and returns parsed entity values.

## Getting Started

Open a terminal in the directory with start_application.py. Enter the following lines:

 ~$ bash activate_me.sh

This will start a flask server on 127.0.0.1:5000/
 
Note: Make sure to have the appropriate database instance running in the background.

To kill the program:

 ~$ bash kill_me.sh

This will grant you instant, localised.. death. To the program.

### Prerequisites

* DynamoDB or MongoDB (preferably both)
* Python 3.6.1 and its standard library as well as the following additional libraries:
  * pymongo(when using MongoDB)
  * flask
  * rasa_nlu
  * mitie
  * duckling
  * schedule
  * boto3


## Deployment

Make sure all environment variables are set correctly.

This API includes an auto-training routine aimed at making the results better over time. This feature may be turned on or off at anytime without affecting the main program. to activate auto-training (which commences by default at 00:30 every night),
simply open a new terminal window in the same directory that contains the start_application.py file and type:

  ~$ python trainer.py

The script will come to life at the designated time. Kill this script should you wish auto-training to stop. You will not need to restart the main script. 

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