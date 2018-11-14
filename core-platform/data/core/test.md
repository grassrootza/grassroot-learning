## meeting path 1
* take_action
  - utter_actions_initialiser
  - utter_actions_menu
* call_meeting
  - slot{"action": "call_meeting"}
  - action_get_group
* select{"group_uid": "0a56b88b-25f7-4365-aa3b-bbe9b903a143"}
  - slot{"group_uid": "0a56b88b-25f7-4365-aa3b-bbe9b903a143"}
  - action_create_meeting_routine
  - slot{"requested_slot": "subject"}
* select{"subject": "Environmental awareness"}
  - action_create_meeting_routine
  - slot{"subject": "Environmental awareness"}
  - slot{"requested_slot": "description"}
* select{"description": "An effort to inform the public on better ways of interacting with their environment"}
  - action_create_meeting_routine
  - slot{"description": "An effort to inform the public on better ways of interacting with their environment"}
  - slot{"requested_slot": "location"}
* select{"location": "Tau Ceti"}
  - action_create_meeting_routine
  - slot{"location": "Tau Ceti"}
  - slot{"requested_slot": "datetime"}
* select{"datetime": "next week friday at 12 in the afternoon"}
  - action_create_meeting_routine
  - slot{"datetime": "next week friday at 12 in the afternoon"}
  - utter_confirm_request
* affirm
  - action_create_meeting_complete
  - action_restart

## vote path 1
* take_action
  - utter_actions_initialiser
  - utter_actions_menu
* call_vote
  - slot{"action": "call_meeting"}
  - action_get_group
* select{"group_uid": "0a56b88b-25f7-4365-aa3b-bbe9b903a143"}
  - slot{"group_uid": "0a56b88b-25f7-4365-aa3b-bbe9b903a143"}
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
  - utter_ask_options_type
* affirm
  - utter_ask_vote_option
* select{"temp": "vote option"}
  - slot{"temp": "vote option"}
  - action_add_to_vote_options
  - slot{"vote_options": "['vote', 'options']"}
  - utter_add_another
* affirm
  - utter_ask_vote_option
* select{"temp": "vote option"}
  - slot{"temp": "vote option"}
  - action_add_to_vote_options
  - slot{"vote_options": "['vote', 'options']"}
  - utter_add_another
* negate
  - action_utter_vote_status
  - utter_confirm_request
* affirm
  - action_create_vote_complete
  - action_restart

## livewire, path 1
* take_action
  - utter_actions_initialiser
  - utter_actions_menu
* create_livewire
  - slot{"action": "call_meeting"}
  - action_get_group
* select{"group_uid": "0a56b88b-25f7-4365-aa3b-bbe9b903a143"}
  - slot{"group_uid": "0a56b88b-25f7-4365-aa3b-bbe9b903a143"}
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
  - utter_ask_add_media_files
* affirm
  - utter_ask_media_file
* select{"media_file_ids": ["762aef58-4865-407a-b793-af6114ab3444"]}
  - slot{"media_file_ids": ["762aef58-4865-407a-b793-af6114ab3444"]}
  - action_save_media_file_id
  - utter_add_another
* affirm
  - utter_ask_media_file
* select{"media_file_ids": ["762aef58-4865-407a-b793-af6114ab3444"]}
  - slot{"media_file_ids": ["762aef58-4865-407a-b793-af6114ab3444"]}
  - action_save_media_file_id
  - utter_add_another
* negate
  - action_utter_livewire_status
  - utter_confirm_request
* affirm
  - action_create_livewire_complete
  - action_restart

## volunteer todo path 1
* take_action
  - utter_actions_initialiser
  - utter_actions_menu
* create_volunteer_todo
  - slot{"action": "call_meeting"}
  - action_get_group
* select{"group_uid": "0a56b88b-25f7-4365-aa3b-bbe9b903a143"}
  - slot{"group_uid": "0a56b88b-25f7-4365-aa3b-bbe9b903a143"}
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
* affirm
  - action_create_volunteer_todo_complete
  - action_restart

## info todo path 1
* take_action
  - utter_actions_initialiser
  - utter_actions_menu
* create_info_todo
  - slot{"action": "call_meeting"}
  - action_get_group
* select{"group_uid": "0a56b88b-25f7-4365-aa3b-bbe9b903a143"}
  - slot{"group_uid": "0a56b88b-25f7-4365-aa3b-bbe9b903a143"}
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
* affirm
  - action_create_info_todo_complete
  - action_restart

## action todo path 1
* take_action
  - utter_actions_initialiser
  - utter_actions_menu
* create_action_todo
  - slot{"action": "call_meeting"}
  - action_get_group
* select{"group_uid": "0a56b88b-25f7-4365-aa3b-bbe9b903a143"}
  - slot{"group_uid": "0a56b88b-25f7-4365-aa3b-bbe9b903a143"}
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
* affirm
  - action_create_todo_action_complete
  - action_restart

## validation todo path 1
* take_action
  - utter_actions_initialiser
  - utter_actions_menu
* create_validation_todo
  - slot{"action": "call_meeting"}
  - action_get_group
* select{"group_uid": "0a56b88b-25f7-4365-aa3b-bbe9b903a143"}
  - slot{"group_uid": "0a56b88b-25f7-4365-aa3b-bbe9b903a143"}
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
* affirm
  - create_validation_todo_complete
  - action_restart