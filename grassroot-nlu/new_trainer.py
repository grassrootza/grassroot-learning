import os
import json
import boto3
from rasa_nlu.converters import load_data
from rasa_nlu.config import RasaNLUConfig
from rasa_nlu.model import Trainer
from rasa_nlu.model import Metadata, Interpreter

os.system('python3 generate_mities.py')

mities = [['vote_training_data.json', 'vote_config_mitie.json', 'vote'],
          ['updates_training_data.json','updates_config_mitie.json', 'updates'],
          ['todo_training_data.json','todo_config_mitie.json', 'todo'],
          ['meeting_training_data.json', 'meeting_config_mitie.json', 'meeting'],
          ['intent_training_data.json', 'intent_config_mitie.json', 'intent'],
          ['group_training_data.json', 'group_config_mitie.json', 'group']]

for mit in mities:
    training_data = load_data('training_models/%s' % mit[0])
    trainer = Trainer(RasaNLUConfig(mit[1]))
    trainer.train(training_data)
    model_directory = trainer.persist('./models/%s/' % mit[2])

    print("New model stored in %s" % model_directory)
    """
    metadata = Metadata.load(model_directory)
    # where model_directory points to the folder the model is persisted in
    interpreter = Interpreter.load(metadata, RasaNLUConfig(mit[1]))
    
    print('\n\ntest this dataset. enter exit to when satisfied.')
    text = ''
    # if no input is entered after 30 seconds, continue.
    while text.lower() != 'exit':
	    text = input(":")
	    if text != 'exit':
	        print(interpreter.parse(text))
	    else:
	    	text = 'exit'
        """
print('Training complete. Model files generated.')

def upload_new_models():
    """Called by train_models() when a new model comes fresh out of training"""
    os.system('zip -r models/trained_models.zip models/*')
    client.upload_file('models/trained_models.zip', 'grassroot-nlu','models/')
    rootLogger.info('model upload successful')
    os.system('rm -r models/*')

# upload_new_models()