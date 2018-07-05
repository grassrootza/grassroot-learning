import json
from rasa_nlu.converters import load_data
from rasa_nlu.config import RasaNLUConfig
from rasa_nlu.model import Trainer
from rasa_nlu.model import Metadata, Interpreter

vote_mitie = {"pipeline": "mitie", 
               "mitie_file": "current_model/model/MITIE-models/english/total_word_feature_extractor.dat", 
               "path": "current_model/trained_models/", 
               "data": "training_models/vote_training_data.json"}

group_mitie = {"pipeline": "mitie",
                "mitie_file": "current_model/model/MITIE-models/english/total_word_feature_extractor.dat", 
                "path": "current_model/trained_models/", 
                "data": "training_models/group_training_data.json"}

intent_mitie = {"pipeline": "mitie", 
                "mitie_file": "current_model/model/MITIE-models/english/total_word_feature_extractor.dat",
                "path": "current_model/trained_models/", 
                "data": "training_models/intent_training_data.json"}

meeting_mitie = {"pipeline": "mitie", 
                 "mitie_file": "current_model/model/MITIE-models/english/total_word_feature_extractor.dat", 
                 "path": "current_model/trained_models/", 
                 "data": "training_models/meeting_training_data.json"}

todo_mitie = {"pipeline": "mitie", 
              "mitie_file": "current_model/model/MITIE-models/english/total_word_feature_extractor.dat", 
              "path": "current_model/trained_models/", 
              "data": "training_models/todo_training_data.json"}

updates_mitie = {"pipeline": "mitie", 
                 "mitie_file": "current_model/model/MITIE-models/english/total_word_feature_extractor.dat", 
                 "path": "current_model/trained_models/", 
                 "data": "training_models/updates_training_data.json"}

vm = open("vote_config_mitie.json", "w")
vm.write(json.dumps(vote_mitie))
vm.close()

g = open("group_config_mitie.json", "w")
g.write(json.dumps(group_mitie))
g.close()

i = open("intent_config_mitie.json", "w")
i.write(json.dumps(intent_mitie))
i.close()

m = open("meeting_config_mitie.json", "w")
m.write(json.dumps(meeting_mitie))
m.close()

t = open("todo_config_mitie.json", "w")
t.write(json.dumps(todo_mitie))
t.close()

u = open("updates_config_mitie.json", "w")
u.write(json.dumps(updates_mitie))
u.close()

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