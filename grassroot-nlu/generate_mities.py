import json

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
