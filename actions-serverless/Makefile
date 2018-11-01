.PHONY: clean test lint

run-platform-actions:
	python3 -m rasa_core_sdk.endpoint --actions platform_actions

run-service-actions:
	python3 -m rasa_core_sdk.endpoint --actions services_actions

test-local-platform:
	sls invoke --local -f act -p test-event.json