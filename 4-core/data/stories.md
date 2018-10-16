## vote
* call_vote
  - action_get_group
* select{"group": "Veritas"}
  - action_utter_save_selected_group
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
* affirm
  - action_create_vote_url
  - action_restart


## meeting
* call_meeting
  - action_get_group
* select{"group": "Veritas"}
  - action_utter_save_selected_group
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
* select{"loaction": "Nowhere"}
  - action_create_meeting_routine
  - slot{"location": "Nowhere"}
  - slot{"requested_slot": "datetime"}
* select{"datetime": "soon"}
  - action_create_meeting_routine
  - slot{"datetime": "soon"}
* affirm
  - action_create_meeting_url
  - action_restart


## todo path 1
* create_volunteer_todo
  - action_get_group
* select{"group": "Veritas"}
  - action_utter_save_selected_group
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
* affirm
  - action_create_volunteer_todo_url
  - action_restart


## todo path 1
* create_validation_todo
  - action_get_group
* select{"group": "Veritas"}
  - action_utter_save_selected_group
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
* affirm
  - create_validation_todo_url
  - action_restart


## todo path 1
* create_info_todo
  - action_get_group
* select{"group": "Veritas"}
  - action_utter_save_selected_group
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
* affirm
  - action_create_info_todo_url
  - action_restart


## todo path 1
* create_action_todo
  - action_get_group
* select{"group": "Veritas"}
  - action_utter_save_selected_group
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
* affirm
  - action_create_todo_action_url
  - action_restart


## livewire
* create_livewire
  - action_get_group
* select{"group": "Veritas"}
  - action_utter_save_selected_group
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
* affirm
  - action_create_livewire_url
  - action_restart


## group
# * create_group
#  _name
#   - action_create_group_routine
#   - slot{"requested_slot": "group_name"}
# * select{"group_name": "Python Everywhere"}
#   - action_create_group_routine
#   - slot{"group_name": "Python Everywhere"}
#   - utter_ask_description
#   - slot{"requested_slot": "description"}
#* select{"description": "None"}
#   - action_create_group_routine
#   - slot{"description": "None"}
#   - utter_ask_reminder_minutes
#   - slot{"requested_slot": "reminderMinutes"}
#* select{"reminderMinutes": "30 minutes"}
#   - action_create_group_routine
#   - slot{"reminderMinutes": "30 minutes"}
# * affirm
#   - action_create_group_url
#   - action_restart


* negate
  - utter_negation
  - action_restart
