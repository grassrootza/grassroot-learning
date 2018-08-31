from rasa_core.agent import Agent
from rasa_core.channels.console import ConsoleInputChannel
agent = Agent.load('models/dialogue', interpreter='models/current/nlu')
agent.handle_channel(ConsoleInputChannel())