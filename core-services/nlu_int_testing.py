from rasa_nlu.model import Interpreter
import json
interpreter = Interpreter.load("./models/current/services_nlu")

def parse_msg(message):
    result = interpreter.parse(message)
    print(json.dumps(result, indent=2))

