import re
import os
import json
import logging
import threading
from flask import Flask, request, jsonify
from werkzeug.exceptions import default_exceptions
from werkzeug.exceptions import HTTPException

from datetime import datetime
from rasa_nlu.model import Interpreter
from rasa_core.agent import Agent

from flask import Flask, request, jsonify
from datetime import datetime

from rasa_core.interpreter import RasaNLUInterpreter
from rasa_core.channels import CollectingOutputChannel
from rasa_core.utils import EndpointConfig

logging.basicConfig(format="[NLULOGS] %(asctime)s [%(threadName)-12.12s] [%(levelname)-5.5s]  %(message)s", level=logging.DEBUG)

application = Flask(__name__)

# Now load up the various interpreters and agents
opening_nlu = RasaNLUInterpreter('./nlu-opening/models/current/opening_nlu')
service_nlu = RasaNLUInterpreter('./core-services/models/current/services_nlu')
platform_nlu = RasaNLUInterpreter('./core-livewire/models/current/platform_nlu')

services_actions_endpoint = os.getenv('SERVICE_ACTION_ENDPOINT_URL', 'http://localhost:5055/webhook')
platform_actions_endpoint = os.getenv('PLATFORM_ACTION_ENDPOINT_URL', 'http://localhost:5055/webhook')

intent_domain_map = {
    'find_services': 'service',
    'request_knowledge': 'knowledge',
    'call_meeting': 'action',
    'call_vote': 'action',
    'create_action_todo': 'action',
    'create_info_todo': 'action',
    'create_volunteer_todo': 'action',
    'create_validation_todo': 'action',
    'create_livewire': 'action',
    'take_action': 'action'
}

domain_agents = {
    "service": Agent.load('core-services/models/dialogue', interpreter = service_nlu, action_endpoint = EndpointConfig(services_actions_endpoint)),
    # "knowledge":  Agent.load('core-knowledge/models/dialogue', interpreter = RasaNLUInterpreter('core-knowledge/models/current/knowledge_nlu')),
    "action" : Agent.load('core-livewire/models/dialogue', interpreter = platform_nlu, action_endpoint = EndpointConfig(platform_actions_endpoint))
}

CONFIDENCE_THRESHOLD = 0.7

def reset_all_agents(user_id):
    for domain in domain_agents:
        domain_agents[domain].handle_text('/restart', sender_id = user_id)

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

def empty_result(domain, error):
    return {
        'domain': domain,
        'intent': '',
        'intent_list': [],
        'entities': [],
        'responses': [],
        'error': error
    }

def reshape_core_result(domain, core_results):
    logging.info('reshaping core_result: {}'.format(core_results))
    
    response_texts = []
    response_menu = []

    for core_result in core_results:
        if 'text' in core_result and core_result['text'] == 'DUM_SPIRO_SPERO':
            logging.warning('Found distress signal from %s domain. Initialising domain rerouting.' % domain)
            return False
        if 'text' in core_result and len(core_result['text']) > 0:
            response_texts.append(core_result['text'])
        if 'buttons' in core_result:
            extracted_text = []
            for idx, button in enumerate(core_result['buttons']):
                extracted_text.append('{}. {}'.format(idx + 1, button['title']))
            response_texts.extend(extracted_text)
            response_menu = core_result['buttons'] 
    
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
    return "Hello World! I am alive, on version 0-d. \n Service action URL is: {}, and platform action URL is: {}".format(services_actions_endpoint, platform_actions_endpoint)


@application.route('/restart', methods=['POST'])
def reset_user_session():
    """Resets all domains

    Query params:
        user_id (str): User ID to reset (required)
    """

    user_id = request.args.get('user_id')
    reset_all_agents(user_id)
    logging.info('Completed restart for {}'.format(user_id))
    return '', 200


@application.route('/province', methods=['GET'])
def parse_user_province():
    """
    We use the services NLU for this, because it is by far the heaviest user of province selection
    """
    user_message = request.args.get('message')
    nlu_result = error_catching_nlu_parse(user_message, service_nlu)
    resp = jsonify(reshape_nlu_result('service', nlu_result))
    resp.status_code = 200
    return resp


"""
@application.route('/evaluate', methods=['GET'])
def evaluate():
    user_message = request.args.get('message')
    nlu_result = error_catching_nlu_parse(user_message, opening_nlu)
    NLU_THRESHOLD = 0.1
    if nlu_result['intent']['confidence'] > NLU_THRESHOLD:
        intent = nlu_result['intent']['name']
        return json.dumps({'intent': intent})
    else:
        return json.dumps({'intent': None})
"""


@application.route('/opening/parse', methods=['GET'])
def parse_unknown_domain(*rerouted_message):
    """Parser when nothing is known about the message, i.e., at the start of a conversation (or at restart)

    Query params:
        message (str): The user message
    
    Returns:
        The best-guess intent, ranked intents, and any guessed entities, except for high-confidence results, in which case, domain parse result
    """
    if rerouted_message:
        user_message = rerouted_message[0]
    else:
        user_message = request.args.get('message')
    nlu_result = error_catching_nlu_parse(user_message, opening_nlu)
    
    primary_result = nlu_result['intent']
    logging.info('NLU result on opening: %s', nlu_result)
    result_as_response = reshape_nlu_result('opening', nlu_result)

    nlu_only = request.args.get('nlu_only', default=False)
    logging.info('Are we doing just an NLU parse? : %s', nlu_only)

    if (primary_result['confidence'] > CONFIDENCE_THRESHOLD and not nlu_only):
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
    logging.info('Parsing {} in domain {}'.format(user_message, domain))
    if domain not in domain_agents:
        logging.error('Error! Sent invalid domain: {}'.format(domain))
        response = jsonify(empty_result(domain, 'Invalid domain sent to core'))
        response.status_code = 200 # error will trigger fail upstream, so rather return 'don't know what this means', in effect 
        return response

    if 'user_id' in request.args:
        user_id = request.args.get('user_id')
        responses_to_user = domain_agents[domain].handle_text(user_message, sender_id=user_id)
    else:
        responses_to_user = domain_agents[domain].handle_text(user_message)

    logging.info('raw response: {}'.format(responses_to_user))
    
    # agent_response = { 'domain': domain, 'responses': responses_to_user }
    # logging.info('Domain agent response: %s', agent_response)

    to_send = responses_to_user if (responses_to_user and len(responses_to_user) > 0) else {}
    reshaped_response = reshape_core_result(domain, to_send)
    if not reshaped_response:
        parse_unknown_domain(*[user_message])

    logging.info('Newly reshaped response: {}'.format(reshaped_response)) 
    resp = jsonify(reshaped_response)
    resp.status_code = 200
    return resp


@application.errorhandler(Exception)
def make_json_error(ex):
    logging.error("Failure! : {}".format(ex))
    response = jsonify(error=str(ex))
    response.status_code = (ex.code
                            if isinstance(ex, HTTPException)
                            else 500)
    return response


if __name__ == "__main__":
    logging.info("Starting up Grassroot Rasa components")
    application.debug = True
        
    application.run(host='0.0.0.0')
