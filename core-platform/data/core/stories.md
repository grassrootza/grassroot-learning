## full flow of meeting
* take_action
    - utter_actions_menu
* call_meeting
    - utter_confirm_meeting_intent
    - slot{"action": "call_meeting"}
    - utter_ask_subject
* select{"subject": "A new test"}
    - slot{"subject": "A new test"}
    - utter_ask_location
* select{"location": "City Hall"}
    - slot{"location": "City Hall"}
    - utter_ask_datetime
* select{"datetime": "tomorrow"}
    - slot{"datetime": "tomorrow"}
    - action_get_group
* select{"group_uid": "a9c0bbdd-d850-45b7-a1d5-6c230f52d2c1"}
    - slot{"group_uid": "a9c0bbdd-d850-45b7-a1d5-6c230f52d2c1"}
    - action_utter_meeting_status
    - utter_confirm_request
* affirm
    - action_send_meeting_to_server
    - action_restart


## meeting happy path 2
* take_action
    - utter_actions_menu
* call_meeting
    - utter_confirm_meeting_intent
    - utter_ask_subject
* select{"subject": "Housing Permits"}
    - slot{"subject": "Housing Permits"}
    - utter_ask_location
* select{"location": "Khutso House"}
    - slot{"location": "Khutso House"}
    - utter_ask_datetime
* select{"datetime": "tomorrow at 9am"}
    - slot{"datetime": "tomorrow at 9am"}
    - action_get_group
* select{"group_uid": "6e0c4eb1-7133-4c39-a705-eadf78f5f2ea"}
    - slot{"group_uid": "6e0c4eb1-7133-4c39-a705-eadf78f5f2ea"}
    - action_utter_meeting_status
    - utter_confirm_request
* affirm
    - action_send_meeting_to_server
    - action_restart


## user wants a meeting
* take_action
    - utter_actions_menu
* call_meeting
    - utter_confirm_meeting_intent
    - slot{"action": "call_meeting"}
    - utter_ask_subject
* select{"subject": "Something awesome"}
    - slot{"subject": "A new test"}
    - utter_ask_location
* select{"location": "Secret Headquarters"}
    - slot{"location": "Secret Headquarters"}
    - utter_ask_datetime
* select{"datetime": "tomorrow"}
    - slot{"datetime": "tomorrow"}
    - action_get_group
> check_for_more_groups

## user wants more groups
> check_for_more_groups
* next_page
    - action_increment_page
    - action_get_group
> check_for_more_groups

# user has chosen a group
> check_for_more_groups
* select{"group_uid": "Veritas"}
    - slot{"group_uid": "Veritas"}
    - action_utter_meeting_status
    - utter_confirm_request
* affirm
    - action_send_meeting_to_server
    - action_restart
* negate
    - utter_restart_action
* affirm
    - utter_restarting
    - utter_actions_menu
    - action_restart
* negate
    - utter_negation
    - action_restart


## livewire happy path 1
> check_what_user_wants
* create_livewire
    - utter_confirm_livewire_intent
    - utter_ask_subject
* select{"subject": "Climate Change"}
    - slot{"subject": "Climate Change"}
    - utter_ask_livewire_content
* select{"livewire_content": "lorem ipsum dolor sit amet, consectetur adipdcing elit"}
    - slot{"livewire_content": "lorem ipsum dolor sit amet, consectetur adipdcing elit"}
    - utter_ask_contact_name
* select{"contact_name": "Darth Vader"}
    - slot{"contact_name": "Darth Vader"}
    - utter_ask_contact_number
* select{"contact_number": "09454534566"}
    - slot{"contact_number": "09454534566"}
    - utter_ask_livewire_location
* select{"longitude": 28.036162200000035, "latitude": -26.1947954}
    - slot{"latitude": -26.1947954}
    - slot{"longitude": 28.036162200000035}
    - utter_location_received
    - utter_ask_add_media_files
* affirm
    - utter_ask_media_file
* select{"media_record_id": "34654-654-564564567-45645646"}
    - slot{"media_record_id": "34654-654-564564567-45645646"}
    - action_save_media_file_id
    - slot{"media_record_ids": ["34654-654-564564567-45645646"]}
    - utter_add_another
* negate
    - action_get_group
* select{"group_uid": "6e0c4eb1-7133-4c39-a705-eadf78f5f2ea"}
    - slot{"group_uid": "6e0c4eb1-7133-4c39-a705-eadf78f5f2ea"}
    - action_utter_livewire_status
    - utter_confirm_request
* affirm
    - action_send_livewire_to_server
    - action_restart


## livewire happy path 3
* take_action
    - utter_actions_menu
* create_livewire
    - utter_confirm_livewire_intent
    - utter_ask_subject
* select{"subject": "New School Opened"}
    - slot{"subject": "New School Opened"}
    - utter_ask_livewire_content
* select{"livewire_content": "Lorem ipsum"}
    - slot{"livewire_content": "Lorem ipsum"}
    - utter_ask_contact_name
* select{"contact_name": "Jon Doe"}
    - slot{"contact_name": "Jon Doe"}
    - utter_ask_contact_number
* select{"contact_number": "066 000 0000"}
    - slot{"contact_number": "066 000 0000"}
    - utter_ask_livewire_location
* select{"longitude": 28.036162200000035, "latitude": -26.1947954}
    - slot{"latitude": -26.1947954}
    - slot{"longitude": 28.036162200000035}
    - utter_location_received
    - utter_ask_add_media_files
> check_for_media_file

## user wants to add a media file
> check_for_media_file
* affirm
    - utter_ask_media_file
* select{"media_record_id": ["762aef58-4865-407a-b793-af6114ab3444"]}
    - slot{"media_record_id": ["762aef58-4865-407a-b793-af6114ab3444"]}
    - action_save_media_file_id
    - utter_add_another
> check_for_media_file

> check_for_media_file
* negate
    - action_get_group
> check_for_more_livewire_groups

## user wants more groups
> check_for_more_livewire_groups
* next_page
    - action_increment_page
    - action_get_group
> check_for_more_livewire_groups

# user has chosen a group
> check_for_more_livewire_groups
* select{"group_uid": "Veritas"}
    - slot{"group_uid": "Veritas"}
    - action_utter_livewire_status
    - utter_confirm_request
* affirm
    - action_send_livewire_to_server
    - action_restart
* negate
    - utter_restart_action
* affirm
    - utter_restarting
    - utter_actions_menu
    - action_restart
* negate
    - utter_negation
    - action_restart

## fallback story
* out_of_scope
    - action_reroute_to_new_domain
    - action_restart
