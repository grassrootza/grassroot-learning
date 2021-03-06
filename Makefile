.PHONY: clean test lint

TEST_PATH=./

help:
	@echo "    train-nlu"
	@echo "        Train all the natural language understanding models using Rasa NLU."
	@echo "    train-core"
	@echo "        Train all the domain dialogue models using Rasa core."
	@echo "    run-flask"
	@echo "        Starts the Flask app that will serve across all domains"

train-nlu:
	python3 -m rasa_nlu.train -c nlu-opening/opening_nlu_config.yml --data nlu-opening/data/nlu -o nlu-opening/models --fixed_model_name opening_nlu --project current --verbose
	python3 -m rasa_nlu.train -c core-knowledge/knowledge_nlu_config.yml --data core-knowledge/data/nlu/nlu.md -o core-knowledge/models --fixed_model_name knowledge_nlu --project current --verbose
	python3 -m rasa_nlu.train -c core-services/services_nlu_config.yml --data core-services/data/nlu -o core-services/models --fixed_model_name services_nlu --project current --verbose
	python3 -m rasa_nlu.train -c core-livewire/nlu_config.yml --data core-livewire/data/nlu -o core-livewire/models --fixed_model_name platform_nlu --project current --verbose

train-core:
	cd ./core-services; python3 train_services_core.py # note that too high an aug factor seems to create over-fitting
	cd ./core-livewire; python3 -m rasa_core.train -d domain.yml -s data/core -c policy.yml --debug -o models/dialogue

run-flask:
	python3 app.py
