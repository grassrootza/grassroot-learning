import argparse, sys

from rasa_core import utils
from rasa_core.agent import Agent
from rasa_core.policies.keras_policy import KerasPolicy
from rasa_core.policies.memoization import MemoizationPolicy
from rasa_core.policies.form_policy import FormPolicy
from rasa_core.policies.embedding_policy import EmbeddingPolicy

parser = argparse.ArgumentParser()
parser.add_argument('--epochs', help='The number of epochs to train', type=int, default=50)
parser.add_argument('--aug', help='How much to augment the data', type=int, default=50)
parser.add_argument('--batch', help='Mini batch size to use', type=int, default=10)
parser.add_argument('--memdepth', help='Depth to apply in memorization', type=int, default=8)

if __name__ == '__main__':
    utils.configure_colored_logging(loglevel="INFO")

    training_data_folder = 'data/core'
    model_path = 'models/dialogue'

    args = vars(parser.parse_args())

    print('Training core model with args: {}'.format(args))

    # training_policy = KerasPolicy(epochs=args['epochs'], batch_size=args['batch'])
    training_policy = EmbeddingPolicy()

    agent = Agent("actions_domain.yml",
                  policies=[MemoizationPolicy(max_history=args['memdepth']), FormPolicy(), training_policy])

    training_data = agent.load_data(training_data_folder)

    agent.train(
            training_data,
            augmentation_factor=args['aug'],
            validation_split=0.2
    )

agent.persist(model_path)
