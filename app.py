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
opening_nlu = Interpreter.load('./nlu-opening/models/current/opening_nlu')

intent_domain_map = {
    'find_services': 'service',
    'request_knowledge': 'knowledge'
}

domain_agents = {
    "service": Agent.load('core-services/models/dialogue', interpreter = 'core-services/models/current/services_nlu'),
    "knowledge":  Agent.load('core-knowledge/models/dialogue', interpreter='core-knowledge/models/current/knowledge_nlu')
}

CONFIDENCE_THRESHOLD = 0.7

"""
Common response format: {
    'domain': what this belongs to (non-empty),
    'intent': best guess of the intent
    'responses': what should be sent back,
    'intent_list': the list of guessed intents, in order,
    'entities': any entities passed back
}
"""

def reshape_nlu_result(domain, nlu_result):
    return {
        'domain': domain,
        'intent': nlu_result['intent'],
        'intent_list': nlu_result.get('intent_ranking', []),
        'entities': nlu_result.get('entities', []),
        'responses': []
    }

def reshape_core_result(domain, core_result):
    logging.info('reshaping core_result: {}'.format(core_result))
    
    response_texts = []
    response_menu = []

    if 'text' in core_result:
        response_texts.append(core_result['text'])
    
    if 'data' in core_result:
        # extracted_text = list(map(lambda button: button['title'], core_result['data']))
        extracted_text = []
        for idx, button in enumerate(core_result['data']):
            extracted_text.append('{}. {}'.format(idx + 1, button['title']))
        response_texts.extend(extracted_text)
        response_menu = core_result['data']
    else:
        response_menu = []
        
    
    logging.info('Extracted response texts: {}'.format(response_texts))

    return {
        'domain': domain,
        'responses': response_texts,
        'menu': response_menu
    }


def error_catching_nlu_parse(user_message, interpreter):
    logging.info('Parsing user message: %s', user_message)
    try:
        return interpreter.parse(user_message)
    except ValueError as ErrorMesage:
        logging.error('Error parsing! Value error')
        logging.error('Error message: %s', ErrorMesage)
        return interpreter.parse('')


@application.route('/status')
def say_hello():
    return "Hello World! I am alive"


@application.route('/opening/parse', methods=['GET'])
def parse_unknown_domain():
    """Parser when nothing is known about the message, i.e., at the start of a conversation (or at restart)

    Query params:
        message (str): The user message
    
    Returns:
        The best-guess intent, ranked intents, and any guessed entities, except for high-confidence results, in which case, domain parse result
    """
    user_message = request.args.get('message')
    nlu_result = error_catching_nlu_parse(user_message, opening_nlu)
    
    primary_result = nlu_result['intent']
    logging.info('NLU result on opening: %s', nlu_result)
    result_as_response = reshape_nlu_result('opening', nlu_result); 
    if (primary_result['confidence'] > CONFIDENCE_THRESHOLD):
        # since we are now pretty sure of the result, check if we can skip straight into domain
        if (primary_result['name'] in intent_domain_map):
            domain = intent_domain_map[primary_result['name']]
            logging.info('Short cutting straight to domain: %s', domain)
            resp = parse_knowledge_domain(domain)
        else:
            resp = jsonify(result_as_response)
    else:
        resp = jsonify(result_as_response)
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
        responses_to_user = domain_agents[domain].handle_message(user_message, sender_id=user_id)
    else:
        responses_to_user = domain_agents[domain].handle_message(user_message)
    
    # agent_response = { 'domain': domain, 'responses': responses_to_user }
    # logging.info('Domain agent response: %s', agent_response)

    reshaped_response = reshape_core_result(domain, responses_to_user[0])
    logging.info('Newly reshaped response: {}'.format(reshaped_response))
    
    resp = jsonify(reshaped_response)
    resp.status_code = 200
    return resp


if __name__ == "__main__":
    logging.info("Starting up Grassroot Rasa components")
    application.debug = True
    application.run(host='0.0.0.0')
