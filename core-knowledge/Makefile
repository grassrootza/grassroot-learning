.PHONY: clean test lint

TEST_PATH=./

help:
	@echo "    train-nlu"
	@echo "        Train the natural language understanding using Rasa NLU."
	@echo "    train-core"
	@echo "        Train a dialogue model using Rasa core."
	@echo "    run-cmdline"
	@echo "        Starts the bot on the command line"
	@echo "    visualize"
	@echo "        Saves the story graphs into a file"

train-nlu:
	python3 -m rasa_nlu.train -c knowledge_nlu_config.yml --data data/nlu/nlu.md -o models --fixed_model_name knowledge_nlu --project current --verbose

train-core:
	python3 train.py

train-online:
	python3 train_online.py

run-cmdline:
	python3 -m rasa_core.run -d models/dialogue -u models/current/knowledge_nlu --debug

run-slack:
	python -m rasa_core.run -d models/dialogue -u models/current/knowledge_nlu --port 5002 --connector slack --credentials slack_credentials.yml --debug

visualize:
	python3 -m rasa_core.visualize -s data/core/ -d domain.yml -o story_graph.png