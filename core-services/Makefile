.PHONY: clean test lint

TEST_PATH=./

help:
	@echo "    train-nlu"
	@echo "        Train the services domain natural language understanding using Rasa NLU."
	@echo "    train-core"
	@echo "        Train the services domain dialogue model using Rasa core."
	@echo "    run-cmdline"
	@echo "        Starts the bot on the command line"

train-nlu:
	python3 -m rasa_nlu.train -c services_nlu_config.yml --data data/nlu/nlu.md -o models --fixed_model_name services_nlu --project current --verbose

train-core:
	python3 train_services_core.py

run-cmdline:
	python3 -m rasa_core.run -d models/dialogue -u models/current/services_nlu --debug
