import json
import logging
import rasa_core_sdk

from rasa_core_sdk.executor import ActionExecutor

logger = logging.getLogger()
logger.setLevel(level=logging.INFO)

action_executor = ActionExecutor()
action_executor.register_package('services_actions')

def act(event, context):
    logger.info('event from the proxy: {}'.format(event))
    action_call = json.loads(event['body'])
    logger.info('action call: {}'.format(action_call))
    action_response = action_executor.run(action_call)
    
    logger.info("Action response: {}".format(action_response))

    response = {
        "statusCode": 200,
        "body": json.dumps(action_response)
    }

    return response


if __name__ == '__main__':
    # Running as standalone python application
    print("Hello!")
    