import logging

from rasa_core import utils
from rasa_core.agent import Agent
from rasa_core.channels.console import ConsoleInputChannel
from rasa_core.interpreter import RasaNLUInterpreter
from rasa_core.policies.keras_policy import KerasPolicy
from rasa_core.policies.memoization import MemoizationPolicy

logger = logging.getLogger(__name__)


def run_training_online(input_channel, interpreter,
                          domain_file="knowledge_domain.yml",
                          training_data_file='data/core'):
    agent = Agent(domain_file,
                  policies=[MemoizationPolicy(max_history=8), KerasPolicy()],
                  interpreter=interpreter)

    training_data = agent.load_data(training_data_file)
    agent.train_online(training_data,
                       input_channel=input_channel,
                       batch_size=10,
                       epochs=50,
                       max_training_samples=300)

    return agent


if __name__ == '__main__':
    utils.configure_colored_logging(loglevel="INFO")
    run_training_online(ConsoleInputChannel(), RasaNLUInterpreter("models/current/knowledge_nlu"))