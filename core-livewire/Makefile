.PHONY: clean test lint

train-nlu:
	python3 -m rasa_nlu.train -c nlu_config.yml --fixed_model_name platform_nlu --data data/nlu/ -o models --project current --verbose

train-core:
	python3 -m rasa_core.train -d domain.yml -s data/core -c policy.yml --debug -o models/dialogue

run-core:
	python3 -m rasa_core.run -d models/dialogue -u models/nlu/current --debug --endpoints endpoints.yml

run-actions:
	cd ..; python3 -m rasa_core_sdk.endpoint --actions actions-serverless.platform_actions

evaluate:
	python3 -m rasa_core.evaluate --core models/dialogue --stories data/test/test.md -o results

train-interactive:
	python3 -m rasa_core.train interactive -o models/dialogue -d domain.yml -c policy.yml -s data/core/ --nlu models/nlu/current --endpoints endpoints.yml
