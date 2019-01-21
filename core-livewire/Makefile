.PHONY: clean test lint

train-nlu:
	python3 -m rasa_nlu.train -c nlu_config.yml --fixed_model_name current --data data/nlu/ -o models --project nlu --verbose

train-core:
	python3 -m rasa_core.train -d domain.yml -s data/core -c policy.yml --debug -o models/dialogue

run-core:
	python3 -m rasa_core.run -d models/dialogue -u models/nlu/current --debug --endpoints endpoints.yml

run-actions:
	python3 -m rasa_core_sdk.endpoint --actions livewire_actions

evaluate:
	python3 -m rasa_core.evaluate --core models/dialogue --stories data/test/test.md -o results