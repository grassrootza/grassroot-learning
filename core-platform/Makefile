.PHONY: clean test lint

TEST_PATH=./

help:
	@echo "    run-action-server"
	@echo "        Activates the action server"
	@echo "    train-nlu"
	@echo "        Trains nlu model"
	@echo "    train-core"
	@echo "        Train rasa core"
	@echo "    train-core-nlu"
	@echo "        Train dialogue and nlu models"
	@echo "    run-core-nlu"
	@echo "        Launch a core-nlu instance"
	@echo "    run-core-solo"
	@echo "        Run rasa core without nlu"
	@echo "    train-online"
	@echo "        Initiates interactive training"
	@echo "    visualize"
	@echo "        Visualizes bot logic"
	@echo "    evaluate"
	@echo "        evaluate the sanity of trained models."


train-online:
	python3 train_online.py

train-nlu:
	python3 -m rasa_nlu.train -c config.yml --data data/nlu -o models --fixed_model_name platform_nlu --project current --verbose

train-core:
	python3 train_platform_core.py --max_history 15

train-core-nlu:
	python3 -m rasa_nlu.train -c config.yml --data data/nlu -o models --fixed_model_name platform_nlu --project current --verbose
	python3 train_platform_core.py --max_history 15
run-core-nlu:
	python3 -m rasa_core.run -d models/dialogue -u models/current/platform_nlu --endpoints endpoints.yml --verbose

run-core-solo:
	python3 -m rasa_core.run -d models/dialogue --endpoints endpoints.yml --verbose

run-action-server:
	python3 -m rasa_core_sdk.endpoint --actions platform_actions

visualize:
	python3 -m rasa_core.visualize -s data/core/ -d actions_domain.yml -o story_graph.html

evaluate:
	python3 -m rasa_core.evaluate --stories test.md --core models/dialogue -o results
