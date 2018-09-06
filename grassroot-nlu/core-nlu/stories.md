## vote
* call_vote
  - utter_affirm_intent
  - utter_affirm_entities
  - slot{"vote_option": "March", "datetime": 0, "subject": "this"}  

## meeting
* call_meeting
  - utter_affirm_intent
  - utter_affirm_entities
  - slot{"location": "here", "datetime": 0, "subject": "this"}

## create_todo
* create_action_todo
  - utter_affirm_intent
  - utter_affirm_entities

## group
* create_group
  - utter_affirm_intent
  - utter_affirm_entities

## affirm
* affirm
  - utter_affirm_action

## negate
* negate
  - utter_negate_action
