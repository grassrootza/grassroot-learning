import logging

from rasa_core import utils, train, run
from rasa_core.agent import Agent
from rasa_core.interpreter import RasaNLUInterpreter
from rasa_core.policies.keras_policy import KerasPolicy
from rasa_core.policies.memoization import MemoizationPolicy

from rasa_core.training import online

logger = logging.getLogger(__name__)


def run_training_online(interpreter,
                        domain_file="services_domain.yml",
                        training_data_file='data/core'):
    
    agent = Agent(domain_file,
                  policies=[MemoizationPolicy(max_history=8), KerasPolicy()],
                  interpreter=interpreter)

    training_data = agent.load_data(training_data_file)
    return train.train_dialogue_model(domain_file="services_domain.yml", 
                        stories_file = "data/core", 
                        output_path = "models/dialogue",
                        max_history=8, 
                        kwargs={
                            "batch_size": 10,
                            "epochs": 50,
                            "max_training_samples": 300
                        })


if __name__ == '__main__':
    utils.configure_colored_logging(loglevel="INFO")
    agent = run_training_online(RasaNLUInterpreter("models/current/services_nlu"))
    online.run_online_learning(agent)
