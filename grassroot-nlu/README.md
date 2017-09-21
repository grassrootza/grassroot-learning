# Project Title

A nlu component that takes in text input and returns parsed entity values.

## Getting Started

Open a terminal in the directory with start_application.py. Enter the following lines:

 export FLASK_APP=start_application.py

 flask run

This will start a flask server on 127.0.0.1:5000/
 
Note: If using MongoDB make sure to have a mongod instance running before running the above code.

### Prerequisites

MongoDB or other compatible database
Python 3.6 and its standard library as well as the following addition libraries:
   pymongo(when using MongoDB)
   flask
   rasa_nlu
   mitie
   duckling
   schedule


### Installing

Once all prerequisites have been installed, place the API within your python path.

edit the 'mitie_file' value in config_mitie.json, replace the default value with the path to your 
MITIE-models total_word_feature_extractor.dat file.

similarily, within the config_mitie.json file, edit the 'data' value to the location of your training_data.json

example:

{
"pipeline": "mitie",
"mitie_file": "/path/to/MITIE-models/english/total_word_feature_extractor.dat",
"path" : "./models",
"data" : "/path/to/training_data.json"
}


## Deployment

Add additional notes about how to deploy this on a live system

## Built With

* [flask](http://flask.pocoo.org/) - The web framework used
* [rasa_nlu](http://rasa.ai/) - The nlu processor
* [mitie](https://https://github.com/mit-nlp/MITIE) - rasa_nlu backend
* [MongoDB](https://www.mongodb.com/) - Default database


## Authors

* **Luke Jordan** - *Lead developer*

* **FRTNX** - *Supporting work* 

See also the list of [contributors](https://github.com/your/project/contributors) who participated in this project.


## Acknowledgments

*
* 
*

