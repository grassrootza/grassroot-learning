from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import logging

from rasa_core import utils, train
from rasa_core.training import online

logger = logging.getLogger(__name__)


def train_agent():
    return train.train_dialogue_model(domain_file="actions_domain.yml",
                                      stories_file="data/core/stories.md",
                                      output_path="models/dialogue",
                                      max_history=2,
                                      kwargs={"batch_size": 64,
                                              "epochs": 50,
                                              "max_training_samples": 300
                                              })


if __name__ == '__main__':
    utils.configure_colored_logging(loglevel="INFO")
    agent = train_agent()
    online.serve_agent(agent)
