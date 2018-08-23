from rasa_core.policies.memoization import MemoizationPolicy
from rasa_core.policies.keras_policy import KerasPolicy
from rasa_core.policies.fallback import FallbackPolicy
from rasa_core.featurizers import \
    MaxHistoryTrackerFeaturizer, BinarySingleStateFeaturizer
from rasa_core.agent import Agent

agent = Agent("domain.yml", policies=[
            MemoizationPolicy(max_history=6),
            KerasPolicy(MaxHistoryTrackerFeaturizer(BinarySingleStateFeaturizer(), max_history=6)), 
            FallbackPolicy(nlu_threshold=0.8, core_threshold=0.3)])

training_data = agent.load_data("stories/")
agent.train(training_data)
