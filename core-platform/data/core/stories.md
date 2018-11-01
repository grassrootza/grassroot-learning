## a new beginning
* take_action
  - utter_actions_initialiser
  - utter_actions_menu
> check_what_user_wants

## user wants a meeting
> check_what_user_wants
* call_meeting
  - slot{"action": "call_meeting"}
  - action_get_group
* select{"group": "Veritas"}
  - slot{"group": "Veritas"}
  - action_create_meeting_routine
  - slot{"requested_slot": "subject"}
* select{"subject": "world domination"}
  - action_create_meeting_routine
  - slot{"subject": "world domination"}
  - slot{"requested_slot": "description"}
* select{"description": "none"}
  - action_create_meeting_routine
  - slot{"description": "none"}
  - slot{"requested_slot": "location"}
* select{"location": "Nowhere"}
  - action_create_meeting_routine
  - slot{"location": "Nowhere"}
  - slot{"requested_slot": "datetime"}
* select{"datetime": "soon"}
  - action_create_meeting_routine
  - slot{"datetime": "soon"}
  - utter_confirm_request
> check_meeting_correctness

## request is correct, send request to server
> check_meeting_correctness
* affirm
  - action_create_meeting_complete
  - action_restart

## request is wrong
> check_meeting_correctness
* negate
  - utter_negation
  - action_restart

## user wants to vote
> check_what_user_wants
* call_vote
  - slot{"action": "call_vote"}
  - action_get_group
* select{"group": "Veritas"}
  - slot{"group": "Veritas"}
  - action_create_vote_routine
  - slot{"requested_slot": "subject"}
* select{"subject": "world domination"}
  - action_create_vote_routine
  - slot{"subject": "world domination"}
  - slot{"requested_slot": "description"}
* select{"description": "None"}
  - action_create_vote_routine
  - slot{"description": "world domination"}
  - slot{"requested_slot": "datetime"}
* select{"datetime": "later"}
  - action_create_vote_routine
  - slot{"datetime": "later"}
  - utter_vote_options_initialiser
* select{"vote_option": "yes"}
  - action_save_vote_option
  - utter_confirm_request
> check_vote_correctness

## request is correct, send request to server
> check_vote_correctness
* affirm
  - action_create_vote_complete
  - action_restart

## request is wrong
> check_vote_correctness
* negate
  - utter_negation
  - action_restart

## user wants to post a livewire
> check_what_user_wants
* create_livewire
  - action_get_group
* select{"group": "Veritas"}
  - slot{"group": "Veritas"}
  - action_livewire_routine
  - slot{"requested_slot": "subject"}
* select{"subject": "New Clinic Open"}
  - action_livewire_routine
  - slot{"subject": "New Clinic Open"}
  - utter_ask_livewire_content
  - slot{"requested_slot": "description"}
*  select{"description": "A new clinic has open within our community"}
  - action_livewire_routine
  - slot{"description": "A new clinic has opened within our comminity"}
  - utter_ask_contact_name
  - slot{"requested_slot": "contact_name"}
* select{"contact_name": "Jack Ryan"}
  - action_livewire_routine
  - slot{"contact_name": "Jack Ryan"}
  - utter_ask_contact_number
  - slot{"requested_slot": "contact_number"}
* select{"contact_number": "011 111 1111"}
  - action_livewire_routine
  - slot{"contact_number": "011 111 1111"}
  - utter_ask_media_files
* select{"media_file_keys": []}
  - action_save_media_file
  - utter_confirm_request
> check_livewire_correctness

## request is correct, send request to server
> check_livewire_correctness
* affirm
  - action_create_livewire_complete
  - action_restart

## request is wrong
> check_livewire_correctness
* negate
  - utter_negation
  - action_restart

## user wants volunteers
> check_what_user_wants
* create_volunteer_todo
  - action_get_group
* select{"group": "Veritas"}
  - slot{"group": "Veritas"}
  - action_todo_volunteer_routine
  - slot{"requested_slot": "subject"}
* select{"subject": "protest"}
  - action_todo_volunteer_routine
  - slot{"subject": "protest"}
  - slot{"requested_slot": "description"}
* select{"description": "Volunteer gathering to clean up our neighbourhood."}
  - action_todo_volunteer_routine
  - slot{"description": "Volunteer gathering to clean up our neighbourhood."}
  - slot{"requested_slot": "datetime"}
* select{"datetime": "later"}
  - action_todo_volunteer_routine
  - slot{"datetime": "later"}
  - action_todo_volunteer_routine
  - utter_confirm_request
> check_volunteer_action_correctness

## all is well, send to server
> check_volunteer_action_correctness
* affirm
  - action_create_volunteer_todo_complete
  - action_restart

## request is wrong
> check_volunteer_action_correctness
* negate
  - utter_negation
  - action_restart

## user wants group member information
> check_what_user_wants
* create_info_todo
  - action_get_group
* select{"group": "Veritas"}
  - slot{"group": "Veritas"}
  - action_todo_info_routine
  - slot{"requested_slot": "subject"}
* select{"subject": "protest"}
  - action_todo_info_routine
  - slot{"subject": "protest"}
  - action_todo_info_routine
  - slot{"requested_slot": "information_required"}
* select{"information_required": "id numbers"}
  - action_todo_info_routine
  - slot{"information_required": "id numbers"}
  - slot{"requested_slot": "response_tag"}
* select{"response_tag": "id: "}
  - action_todo_info_routine
  - slot{"response_tag": "id: "}
  - slot{"requested_slot": "datetime"}
* select{"datetime": "later"}
  - action_todo_info_routine
  - slot{"datetime": "later"}
  - utter_confirm_request
> check_info_action_correctness

## all clear, proceed to server
> check_info_action_correctness
* affirm
  - action_create_info_todo_complete
  - action_restart

## request is wrong
> check_info_action_correctness
* negate
  - utter_negation
  - action_restart

## user wants to call for action
> check_what_user_wants
* create_action_todo
  - action_get_group
* select{"group": "Veritas"}
  - slot{"group": "Veritas"}
  - action_todo_action_routine
  - slot{"requested_slot": "subject"}
* select{"subject": "protest"}
  - action_todo_action_routine
  - slot{"subject": "protest"}
  - slot{"requested_slot": "description"}
* select{"description": "Volunteer gathering to clean up our neighbourhood."}
  - action_todo_action_routine
  - slot{"description": "Volunteer gathering to clean up our neighbourhood."}
  - slot{"requested_slot": "datetime"}
* select{"datetime": "later"}
  - action_todo_action_routine
  - slot{"datetime": "later"}
  - action_todo_action_routine
  - utter_confirm_request
> check_action_correctness

## request is correct, send to server
> check_action_correctness
* affirm
  - action_create_todo_action_complete
  - action_restart

## request is wrong
> check_action_correctness
* negate
  - utter_negation
  - action_restart

## user seeks validation
> check_what_user_wants
* create_validation_todo
  - action_get_group
* select{"group": "Veritas"}
  - slot{"group": "Veritas"}
  - action_todo_validation_routine
  - slot{"requested_slot": "subject"}
* select{"subject": "protest"}
  - action_todo_validation_routine
  - slot{"subject": "protest"}
  - slot{"requested_slot": "description"}
* select{"description": "Volunteer gathering to clean up our neighbourhood."}
  - action_todo_validation_routine
  - slot{"description": "Volunteer gathering to clean up our neighbourhood."}
  - slot{"requested_slot": "datetime"}
* select{"datetime": "later"}
  - action_todo_validation_routine
  - slot{"datetime": "later"}
  - utter_confirm_request
> check_validation_correctness

## request is correct, send to server
> check_validation_carrectness
* affirm
  - create_validation_todo_complete
  - action_restart

## request is wrong
> check_validation_carrectness
* negate
  - utter_negation
  - action_restart
