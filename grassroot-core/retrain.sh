#!/bin/bash

python train.py
python -m rasa_nlu.train -c opening_nlu_config.yml --data opening_nlu.md -o models --fixed_model_name opening_nlu --project current --verbose
