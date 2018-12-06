## a new beginning
* take_action
  - utter_actions_initialiser
  - utter_actions_menu
> check_what_user_wants

## user wants a meeting
> check_what_user_wants
* call_meeting
  - utter_confirm_meeting_intent
  - slot{"action": "call_meeting"}
  - action_get_group
> check_for_more_meeting_groups

## user wants more groups
> check_for_more_meeting_groups
* next_page
  - action_increment_page
  - action_get_group
> check_for_more_meeting_groups

## user has selected desired group, continue meeting flow
> check_for_more_meeting_groups
* select{"group_uid": "Veritas"}
  - slot{"group_uid": "Veritas"}
  - action_create_meeting_routine
  - slot{"requested_slot": "subject"}
* select{"subject": "world domination"}
  - action_create_meeting_routine
  - slot{"subject": "world domination"}
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
  - utter_restart_action
> restart_meeting_creation

> restart_meeting_creation
* affirm
  - utter_restarting
  - utter_actions_menu
  - action_restart
> check_what_user_wants

> restart_meeting_creation
* negate
  - utter_negation
  - action_restart

## user wants to vote
> check_what_user_wants
* call_vote
  - utter_confirm_vote_intent
  - slot{"action": "call_vote"}
  - action_get_group
> check_for_more_vote_groups

## user wants more groups
> check_for_more_vote_groups
* next_page
  - action_increment_page
  - action_get_group
> check_for_more_vote_groups

## user has selected desired group, continue vote flow
> check_for_more_vote_groups
* select{"group_uid": "Veritas"}
  - slot{"group_uid": "Veritas"}
  - action_create_vote_routine
  - slot{"requested_slot": "subject"}
* select{"subject": "world domination"}
  - action_create_vote_routine
  - slot{"subject": "world domination"}
  - slot{"requested_slot": "datetime"}
* select{"datetime": "later"}
  - action_create_vote_routine
  - slot{"datetime": "later"}
  - utter_ask_options_type
> check_default_or_custom

## user is okay with default yes/no options
> check_default_or_custom
* negate
  - action_default_vote_options
  - slot{"vote_options": "['vote', 'options']"}
  - action_utter_vote_status
  - utter_confirm_request
> check_vote_correctness

## user would like custom vote options
> check_default_or_custom
* affirm
  - utter_ask_vote_option
* select{"temp": "vote option"}
  - slot{"temp": "vote option"}
  - action_add_to_vote_options
  - slot{"vote_options": "['vote', 'options']"}
  - utter_add_another
> check_for_more

## user would like to add another vote option
> check_for_more
* affirm
  - utter_ask_vote_option
* select{"temp": "vote option"}
  - slot{"temp": "vote option"}
  - action_add_to_vote_options
  - slot{"vote_options": ["vote", "options"]}
  - utter_add_another
> check_for_more

## user is done adding vote options
> check_for_more
* negate
  - action_utter_vote_status
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
  - utter_restart_action
> restart_vote_creation

# user would like to make a redo
> restart_vote_creation
* affirm
  - utter_restarting
  - utter_actions_menu
  - action_restart
> check_what_user_wants

# user doesnt have it in them to try again
> restart_vote_creation
* negate
  - utter_negation
  - action_restart

## user wants to post a livewire
> check_what_user_wants
* create_livewire
  - utter_confirm_livewire_intent
  - action_get_group
> check_for_more_livewire_groups

## user wants more groups
> check_for_more_livewire_groups
* next_page
  - action_increment_page
  - action_get_group
> check_for_more_livewire_groups

## user has selected desired group, continue livewire flow
> check_for_more_livewire_groups
* select{"group_uid": "Veritas"}
  - slot{"group_uid": "Veritas"}
  - action_livewire_routine
  - slot{"requested_slot": "subject"}
* select{"subject": "New Clinic Open"}
  - action_livewire_routine
  - slot{"subject": "New Clinic Open"}
  - slot{"requested_slot": "livewire_content"}
*  select{"livewire_content": "A new clinic has open within our community"}
  - action_livewire_routine
  - slot{"livewire_content": "A new clinic has opened within our comminity"}
  - slot{"requested_slot": "contact_name"}
* select{"contact_name": "Jack Ryan"}
  - action_livewire_routine
  - slot{"contact_name": "Jack Ryan"}
  - slot{"requested_slot": "contact_number"}
* select{"contact_number": "011 111 1111"}
  - action_livewire_routine
  - slot{"contact_number": "011 111 1111"}
  - utter_ask_add_media_files
> check_for_media_file

## user wants to add a media file
> check_for_media_file
* affirm
  - utter_ask_media_file
* select{"media_record_ids": ["762aef58-4865-407a-b793-af6114ab3444"]}
  - slot{"media_record_ids": ["762aef58-4865-407a-b793-af6114ab3444"]}
  - action_save_media_file_id
  - utter_add_another
> check_for_more_media_files

## user would like to add another media file
> check_for_more_media_files
* affirm
  - utter_ask_media_file
* select{"media_record_ids": ["762aef58-4865-407a-b793-af6114ab3444"]}
  - slot{"media_record_ids": ["762aef58-4865-407a-b793-af6114ab3444"]}
  - action_save_media_file_id
  - utter_add_another
> check_for_more_media_files  

## user is happy with currently added files, now check for location
> check_for_more_media_files
* negate
  - utter_location_or_not
> check_for_location

## alternatively, user is happy without any media files, check for location
> check_for_media_file
* negate
  - utter_location_or_not
> check_for_location

## user would like to add livewire location
> check_for_location
* affirm
  - utter_ask_livewire_location
* select{"longitude": 28.036162200000035, "latitude": -26.1947954}
  - slot{"latitude": -26.1947954}
  - slot{"longitude": 28.036162200000035}
  - utter_location_received
  - action_utter_livewire_status
  - utter_confirm_request
> check_livewire_correctness

## user is easy to please and is happy without livewire location
> check_for_location
* negate
  - utter_location_skipped
  - action_utter_livewire_status
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
  - utter_restart_action
> restart_livewire_creation

# user would like to make a redo
> restart_livewire_creation
* affirm
  - utter_restarting
  - utter_actions_menu
  - action_restart
> check_what_user_wants

# user doesnt have it in them to try again
> restart_livewire_creation
* negate
  - utter_negation
  - action_restart

## user wants volunteers
> check_what_user_wants
* create_volunteer_todo
  - utter_confirm_volunteer_intent
  - action_get_group
> check_for_more_volunteer_groups

## user wants more groups
> check_for_more_volunteer_groups
* next_page
  - action_increment_page
  - action_get_group
> check_for_more_volunteer_groups

## user has selected desired group, continue volunteer flow
> check_for_more_volunteer_groups
* select{"group_uid": "Veritas"}
  - slot{"group_uid": "Veritas"}
  - action_todo_volunteer_routine
  - slot{"requested_slot": "subject"}
* select{"subject": "protest"}
  - action_todo_volunteer_routine
  - slot{"subject": "protest"}
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
  - utter_restart_action
> restart_volunteer_creation

# user would like to make a redo
> restart_volunteer_creation
* affirm
  - utter_restarting
  - utter_actions_menu
  - action_restart
> check_what_user_wants

# user doesnt have it in them to try again
> restart_volunteer_creation
* negate
  - utter_negation
  - action_restart

## user wants group member information
> check_what_user_wants
* create_info_todo
  - utter_confirm_info_intent
  - action_get_group
> check_for_more_info_groups

## user wants more groups
> check_for_more_info_groups
* next_page
  - action_increment_page
  - action_get_group
> check_for_more_info_groups

## user has selected desired group, continue info-todo flow
> check_for_more_info_groups
* select{"group_uid": "Veritas"}
  - slot{"group_uid": "Veritas"}
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
  - utter_restart_action
> restart_info_todo_creation

# user would like to make a redo
> restart_info_todo_creation
* affirm
  - utter_restarting
  - utter_actions_menu
  - action_restart
> check_what_user_wants

# user doesnt have it in them to try again
> restart_info_todo_creation
* negate
  - utter_negation
  - action_restart

## user wants to call for action
> check_what_user_wants
* create_action_todo
  - utter_confirm_action_intent
  - action_get_group
> check_for_more_action_groups

## user wants more groups
> check_for_more_action_groups
* next_page
  - action_increment_page
  - action_get_group
> check_for_more_action_groups

## user has selected desired group, continue action flow
> check_for_more_action_groups
* select{"group_uid": "Veritas"}
  - slot{"group_uid": "Veritas"}
  - action_todo_action_routine
  - slot{"requested_slot": "subject"}
* select{"subject": "protest"}
  - action_todo_action_routine
  - slot{"subject": "protest"}
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
  - utter_restart_action
> restart_action_todo_creation

# user would like to make a redo
> restart_action_todo_creation
* affirm
  - utter_restarting
  - utter_actions_menu
  - action_restart
> check_what_user_wants

# user doesnt have it in them to try again
> restart_action_todo_creation
* negate
  - utter_negation
  - action_restart

## user seeks validation
> check_what_user_wants
* create_validation_todo
  - utter_confirm_validation_intent
  - action_get_group
> check_for_more_validation_groups

## user wants more groups
> check_for_more_validation_groups
* next_page
  - action_increment_page
  - action_get_group
> check_for_more_validation_groups

## user has selected desired group, continue validation flow
> check_for_more_validation_groups
* select{"group_uid": "Veritas"}
  - slot{"group_uid": "Veritas"}
  - action_todo_validation_routine
  - slot{"requested_slot": "subject"}
* select{"subject": "protest"}
  - action_todo_validation_routine
  - slot{"subject": "protest"}
  - slot{"requested_slot": "datetime"}
* select{"datetime": "later"}
  - action_todo_validation_routine
  - slot{"datetime": "later"}
  - utter_confirm_request
> check_validation_correctness

## request is correct, send to server
> check_validation_correctness
* affirm
  - create_validation_todo_complete
  - action_restart

## request is wrong
> check_validation_correctness
* negate
  - utter_restart_action
> restart_validation_creation

# user would like to make a redo
> restart_validation_creation
* affirm
  - utter_restarting
  - utter_actions_menu
  - action_restart
> check_what_user_wants

# user doesnt have it in them to try again
> restart_validation_creation
* negate
  - utter_negation
  - action_restart

## fallback story
* out_of_scope
  - action_reroute_to_new_domain
  - action_restart