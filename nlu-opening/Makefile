.PHONY: clean test lint

TEST_PATH=./

help:
	@echo "    train-nlu"
	@echo "        Train the opening NLU using Rasa NLU."

train-nlu:
	python3 -m rasa_nlu.train -c opening_nlu_config.yml --data data/nlu -o models --fixed_model_name opening_nlu --project current --verbose
