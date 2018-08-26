## Generated Story -8982863629809492989
* greet
    - utter_greet
    - provide_issues_menu
* select{"issue": "water"}
    - slot{"issue": "water"}
    - utter_confirmation
    - provide_procedures_menu
* select{"procedure": "take_action"}
    - slot{"procedure": "take_action"}
    - utter_confirmation
    - provide_water_problems_main
* request_more_options
    - provide_water_problems_more
* select{"problem": "interruption"}
    - slot{"problem": "interruption"}
    - provide_actions_menu
* select{"action_taken": "councillor"}
    - slot{"action_taken": "councillor"}
    - utter_please_confirm
* mood_affirm
    - utter_completed
## Generated Story -2219059682658056476
* greet
    - utter_greet
    - provide_issues_menu
* select{"issue": "housing", "procedure": "know_rights"}
    - slot{"issue": "housing"}
    - slot{"procedure": "know_rights"}
    - utter_confirmation
    - provide_housing_problems_main
* select{"problem": "obtain_public_housing"}
    - slot{"problem": "obtain_public_housing"}
    - provide_actions_menu
* select{"action_taken": "called_municipality"}
    - slot{"action_taken": "called_municipality"}
    - utter_please_confirm
* mood_affirm
    - export

## Generated Story -2196966070674676576
* greet
    - utter_greet
    - provide_issues_menu
* select{"procedure": "know_rights"}
    - slot{"procedure": "know_rights"}
    - utter_confirmation
    - provide_issues_menu
* select{"issue": "housing"}
    - slot{"issue": "housing"}
    - provide_housing_problems_main
* select{"problem": "eviction"}
    - slot{"problem": "eviction"}
    - provide_actions_menu
* select{"action_taken": "councillor"}
    - slot{"action_taken": "councillor"}
    - utter_please_confirm
    - export

## Generated Story 9007737986982243659
* request_water
    - slot{"issue":"water"}
    - provide_procedures_menu
* select{"procedure": "obtain_contact"}
    - slot{"procedure": "obtain_contact"}
    - utter_confirmation
    - provide_water_problems_main
* request_more_options
    - provide_water_problems_more
* select{"problem": "health_concerns"}
    - slot{"problem": "health_concerns"}
    - provide_actions_menu
* select{"action_taken": "called_municipality"}
    - slot{"action_taken": "called_municipality"}
    - utter_please_confirm
* mood_affirm
    - export

