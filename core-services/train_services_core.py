import argparse, sys

from rasa_core import utils
from rasa_core.agent import Agent
from rasa_core.policies.keras_policy import KerasPolicy
from rasa_core.policies.memoization import MemoizationPolicy

parser = argparse.ArgumentParser()
parser.add_argument('--epochs', help='The number of epochs to train', type=int, default=30)
parser.add_argument('--aug', help='How much to augment the data', type=int, default=50)
parser.add_argument('--batch', help='Mini batch size to use', type=int, default=10)
parser.add_argument('--max_history', help='Depth to apply in memorization', type=int, default=8)

if __name__ == '__main__':
    utils.configure_colored_logging(loglevel="INFO")

    training_data_folder = 'data/core'
    model_path = 'models/dialogue'

    args = vars(parser.parse_args())

    print('Training services core model with args: {}'.format(args))

    memoization_policy = MemoizationPolicy(max_history=args['max_history'])
    lstm_policy = KerasPolicy(epochs=args['epochs'], batch_size=args['batch'], max_history=args['max_history'])

    agent = Agent("services_domain.yml", policies=[memoization_policy, lstm_policy])

    training_data = agent.load_data(training_data_folder, augmentation_factor=args['aug'])

    agent.train(
            training_data,
            augmentation_factor=args['aug'],
            validation_split=0.2
    )

agent.persist(model_path)
