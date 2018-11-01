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
	python3 -m rasa_nlu.train -c core-platform/config.yml --data core-platform/data/nlu -o core-platform/models --fixed_model_name platform_nlu --project current --verbose

train-core:
	cd ./core-services; python3 train_services_core.py --aug 10 --epochs 50 --batch 128 --memdepth 0 # note that too high an aug factor seems to create over-fitting
	cd ./core-knowledge; python3 train_knowledge_core.py
	cd ./core-platform; python3 -m rasa_core.train -d actions_domain.yml -s data/core -o models/dialogue --history 10

run-flask:
	python3 app.py
