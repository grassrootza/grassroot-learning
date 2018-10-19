## happy path, housing
* greet
    - utter_greet
    - provide_issues_menu
* select{"issue":"housing"}
    - utter_confirmation
    - provide_procedures_menu
* select{"procedure":"know_rights"}
    - utter_confirmation
    - provide_housing_problems_main
* request_more_options
    - provide_housing_problems_more
* select{"problem":"proclamation"}
    - provide_actions_menu
* select{"action_taken":"none"}
    - utter_please_confirm
* mood_affirm
    - utter_completed

## happy path, water
* greet
    - utter_greet
    - provide_issues_menu
* select{"issue":"water"}
    - utter_confirmation
    - provide_procedures_menu
* select{"procedure":"take_action"}
    - utter_confirmation
    - provide_water_problems_main
* request_more_options
    - provide_water_problems_more
* select{"problem":"supply"}
    - provide_actions_menu
* select{"action_taken":"none"}
    - utter_please_confirm
* mood_affirm
    - utter_completed

## unhappy path, selecting issue not implemented yet
* greet
    - utter_greet
    - provide_issues_menu
* mood_confused
    - utter_orientation
* mood_confused
    - utter_grassroot_site
* goodbye
    - utter_goodbye

## shortcut path, straight to water
* request_water
    - slot{"issue":"water"}
    - provide_procedures_menu
* select{"procedure":"know_rights"}
    - utter_confirmation
    - provide_water_problems_main
* request_more_options
    - provide_water_problems_more
* select{"problem":"cutoff"}
    - provide_actions_menu
* select{"action_taken":"none"}
    - utter_please_confirm
* mood_affirm
    - utter_completed