import re
import json

from flask import Flask, request, jsonify
from datetime import datetime

from rasa_nlu.model import Interpreter

from rasa_core.agent import Agent
from rasa_core.channels.console import ConsoleInputChannel

import logging

logging.basicConfig(format="[NLULOGS] %(asctime)s [%(threadName)-12.12s] [%(levelname)-5.5s]  %(message)s", level=logging.DEBUG)

application = Flask(__name__)

# Now load up the various interpreters and agents
opening_nlu = Interpreter.load('./nlu-opening/models/current/nlu')
knowledge_agent = Agent.load('core-knowledge/models/dialogue', interpreter='core-knowledge/models/current/knowledge_nlu')

CONFIDENCE_THRESHOLD = 0.8

@application.route('/status')
def say_hello():
    return "Hello World! I am alive"


@application.route('/parse', methods=['GET'])
def parse_unknown_domain():
    user_message = request.args.get('message')
    nlu_result = opening_nlu.parse(user_message)
    primary_result = nlu_result['intent']
    if (primary_result['confidence'] > CONFIDENCE_THRESHOLD):
        resp = jsonify(primary_result)
    else:
        resp = jsonify(nlu_result['intent_ranking'])
    resp.status_code = 200
    return resp


@application.route('/knowledge/parse', methods=['GET'])
def parse_knowledge_domain():
    user_message = request.args.get('message')
    if 'user_id' in request.args:
        user_id = request.args.get('user_id')
        agent_response = knowledge_agent.handle_message(user_message, sender_id=user_id)
    else:
        agent_response = knowledge_agent.handle_message(user_message)
    
    logging.warning('Knowledge agent: %s', agent_response)
    resp = jsonify(agent_response)
    resp.status_code = 200
    return resp

if __name__ == "__main__":
    application.debug = True
    application.run()
