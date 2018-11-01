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
	python3 -m rasa_nlu.train -c services_nlu_config.yml --data data/nlu -o models --fixed_model_name services_nlu --project current --verbose

train-core: # default
	python3 train_services_core.py

train-core-quick: # for local experimenting etc
	python3 train_services_core.py --aug 10 --epochs 50 --batch 128 --memdepth 0

evaluate-provinces:
	python3 -m rasa_nlu.evaluate --data data/examples/provinces_testing_data.json --model models/current/services_nlu

run-core:
	python3 -m rasa_core.run -d models/dialogue -u models/current/services_nlu --endpoints endpoints.yml --debug

run-nlu:
	python3 -m rasa_nlu.server --path models/current/services_nlu/

evaluate:
	python3 -m rasa_core.evaluate -s data/core/test.md -d models/dialogue -o matrix.pdf