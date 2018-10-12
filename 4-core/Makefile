.PHONY: clean test lint

TEST_PATH=./

help:
	@echo "    run-action-server"
	@echo "        Activates the action server"
	@echo "    train-nlu"
	@echo "        Train the natural language understanding using Rasa NLU."
	@echo "    train-core"
	@echo "        Train a dialogue model using Rasa core."
    @echo "    run-core-nlu"
    @echo "        Launch a core-nlu instance"
	@echo "    train-online"
	@echo "        Initiates interactive training."
	@echo "    visualize"
	@echo "        Visualizes bot logic"


train-online:
	python3 train_online.py

train-nlu:
	python3 -m rasa_nlu.train -c config.yml --data nlu.json -o models --fixed_model_name nlu --project current --verbose

train-core:
	python3 -m rasa_core.train -d platform_domain.yml -s data/stories.md -o models/dialogue

run-core-nlu:
	python3 -m rasa_core.run -d models/dialogue -u models/current/nlu --endpoints endpoints.yml --verbose

run core-solo:
    python3 -m rasa_core.run -d models/dialogue --endpoints endpoints.yml --verbose

run-action-server:
	python3 -m rasa_core.run -d models/dialogue --endpoints endpoints.yml

visualize:
	python3 -m rasa_core.visualize -s data/core/ -d domain.yml -o story_graph.png
