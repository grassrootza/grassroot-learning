import re
import json

from flask import Flask, request, jsonify
from datetime import datetime
from rasa_core.agent import Agent
from rasa_core.channels.console import ConsoleInputChannel

import logging

logging.basicConfig(format="[NLULOGS] %(asctime)s [%(threadName)-12.12s] [%(levelname)-5.5s]  %(message)s", level=logging.DEBUG)

application = Flask(__name__)
knowledge_agent = Agent.load('core-knowledge/models/dialogue', interpreter='core-knowledge/models/current/knowledge_nlu')

@application.route('/')
def say_hello():
    return "Hello World!"


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
