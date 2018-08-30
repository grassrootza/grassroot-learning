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

intent_domain_map = {
    'find_services': 'service',
    'request_knowledge': 'knowledge'
}

domain_agents = {
    "service": Agent.load('core-services/models/dialogue', interpreter = 'core-services/models/current/services_nlu'),
    "knowledge":  Agent.load('core-knowledge/models/dialogue', interpreter='core-knowledge/models/current/knowledge_nlu')
}

CONFIDENCE_THRESHOLD = 0.8

@application.route('/status')
def say_hello():
    return "Hello World! I am alive"


@application.route('/parse', methods=['GET'])
def parse_unknown_domain():
    """Parser when nothing is known about the message, i.e., at the start of a conversation (or at restart)

    Query params:
        message (str): The user message
    
    Returns:
        The best-guess intent, ranked intents, and any guessed entities, except for high-confidence results, in which case, domain parse result
    """
    user_message = request.args.get('message')
    nlu_result = opening_nlu.parse(user_message)
    primary_result = nlu_result['intent']
    if (primary_result['confidence'] > CONFIDENCE_THRESHOLD):
        # since we are now pretty sure of the result, check if we can skip straight into domain
        if (primary_result['intent'] in intent_domain_map):
            domain = intent_domain_map[primary_result['intent']]
            logging.info('Short cutting straight to domain: %s', domain)
            resp = parse_knowledge_domain(domain)
        else:
            resp = jsonify(primary_result)
    else:
        resp = jsonify(nlu_result['intent_ranking'])
    resp.status_code = 200
    return resp


@application.route('/<domain>/parse', methods=['GET'])
def parse_knowledge_domain(domain):
    """Parser when it is known (or high-confidence guessed) that user is in the find knowledge domain

    Params:
        domain (str): The domain of the response (path variable)
        message (str): The user message
        user_id: The user ID, for tracking within Rasa core (can be any type of value, as long as consistent within session)
    """
    user_message = request.args.get('message')
    if 'user_id' in request.args:
        user_id = request.args.get('user_id')
        agent_response = domain_agents[domain].handle_message(user_message, sender_id=user_id)
    else:
        agent_response = domain_agents[domain].handle_message(user_message)
    
    agent_response['domain'] = domain
    logging.info('Domain agent response: %s', agent_response)
    
    resp = jsonify(agent_response)
    resp.status_code = 200
    return resp

if __name__ == "__main__":
    application.debug = True
    application.run()
