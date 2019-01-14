import argparse, sys
from log import *

import logging

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
parser.add_argument('--max_history', help='Max history to pass to policy', type=int, default=5)
parser.add_argument('--memo', help='Whether to use memoization', type=bool, default=False)
parser.add_argument('--embedding', help='Whether to use embedding', type=bool, default=False)

if __name__ == '__main__':
    utils.configure_colored_logging(loglevel="INFO")

    training_data_folder = 'data/core'
    model_path = 'models/dialogue'

    args = vars(parser.parse_args())

    logging.info('Training platform core model with args: {}'.format(args))

    memoization_policy = MemoizationPolicy(max_history=args['max_history'])

    lstm_policy = KerasPolicy(epochs=args['epochs'], batch_size=args['batch'], max_history=args['max_history'])
    embedding_policy = EmbeddingPolicy(epochs=args['epochs'])
    training_policy = embedding_policy if args['embedding'] else lstm_policy

    policy_ensemble = [FormPolicy(), memoization_policy, training_policy] if args['memo'] else [FormPolicy(), training_policy]
    logging.info("Policy ensemble has {} members".format(len(policy_ensemble)))
    agent = Agent("actions_domain.yml", policies=policy_ensemble)

    training_data = agent.load_data(training_data_folder, augmentation_factor=args['aug'])

    agent.train(
            training_data,
            augmentation_factor=args['aug'],
            validation_split=0.2
    )

agent.persist(model_path)
