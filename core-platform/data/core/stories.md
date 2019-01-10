## full flow of meeting
* take_action
    - utter_actions_menu
> check_what_user_wants

## meeting happy path 1
* call_meeting
    - utter_confirm_meeting_intent
    - slot{"action": "call_meeting"}
    - action_get_group
* select{"group_uid": "a9c0bbdd-d850-45b7-a1d5-6c230f52d2c1"}
    - slot{"group_uid": "a9c0bbdd-d850-45b7-a1d5-6c230f52d2c1"}
    - request_subject
    - slot{"requested_slot": "subject"}
* select{"subject": "A new test"}
    - slot{"subject": "A new test"}
    - extract_and_validate_entity
    - slot{"subject": "A new test"}
    - slot{"requested_slot": null}
    - request_location
    - slot{"requested_slot": "location"}
* select{"location": "City Hall"}
    - slot{"location": "City Hall"}
    - extract_and_validate_entity
    - slot{"location": "City Hall"}
    - slot{"requested_slot": null}
    - request_datetime
    - slot{"requested_slot": "datetime"}
* select{"datetime": "tomorrow"}
    - slot{"datetime": "tomorrow"}
    - extract_and_validate_entity
    - slot{"datetime": "tomorrow"}
    - slot{"requested_slot": null}
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
    - action_get_group
* select{"group_uid": "6e0c4eb1-7133-4c39-a705-eadf78f5f2ea"}
    - slot{"group_uid": "6e0c4eb1-7133-4c39-a705-eadf78f5f2ea"}
    - utter_ask_subject
    - request_subject
    - slot{"requested_slot": "subject"}
* select{"subject": "Housing Permits"}
    - slot{"subject": "Housing Permits"}
    - extract_and_validate_entity
    - slot{"subject": "Housing Permits"}
    - slot{"requested_slot": null}
    - utter_ask_location
    - request_location
    - slot{"requested_slot": "location"}
* select{"location": "Khutso House"}
    - slot{"location": "Khutso House"}
    - extract_and_validate_entity
    - slot{"location": "Khutso House"}
    - slot{"requested_slot": null}
    - utter_ask_datetime
    - request_datetime
    - slot{"requested_slot": "datetime"}
* select{"datetime": "tomorrow at 9am"}
    - slot{"datetime": "tomorrow at 9am"}
    - extract_and_validate_entity
    - slot{"datetime": "tomorrow at 9am"}
    - slot{"requested_slot": null}
    - action_utter_meeting_status
    - utter_confirm_request
* affirm
    - action_send_meeting_to_server
    - action_restart

## user wants a meeting
> check_what_user_wants
* call_meeting
    - utter_confirm_meeting_intent
    - slot{"action": "call_meeting"}
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
    - utter_ask_subject
    - request_subject
    - slot{"requested_slot": "subject"}
* select{"subject": "Something awesome"}
    - slot{"subject": "A new test"}
    - extract_and_validate_entity
    - slot{"subject": "Something awesome"}
    - utter_ask_location
    - request_location
    - slot{"requested_slot": "location"}
* select{"location": "Secret Headquarters"}
    - slot{"location": "Secret Headquarters"}
    - extract_and_validate_entity
    - slot{"location": "Secret Headquarters"}
    - utter_ask_datetime
    - request_datetime
  - slot{"requested_slot": "datetime"}
* select{"datetime": "tomorrow"}
    - slot{"datetime": "tomorrow"}
    - extract_and_validate_entity
    - slot{"datetime": "tomorrow"}
    - slot{"requested_slot": null}
    - action_utter_meeting_status
    - utter_confirm_request
> check_meeting_correctness

## request is correct, send request to server
> check_meeting_correctness
* affirm
    - action_send_meeting_to_server
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

> restart_meeting_creation
* negate
    - utter_negation
    - action_restart

## livewire happy path 1
> check_what_user_wants
* create_livewire
    - utter_confirm_livewire_intent
    - action_get_group
* select{"group_uid": "6e0c4eb1-7133-4c39-a705-eadf78f5f2ea"}
    - slot{"group_uid": "6e0c4eb1-7133-4c39-a705-eadf78f5f2ea"}
    - utter_ask_subject
    - request_subject
    - slot{"requested_slot": "subject"}
* select{"subject": "Climate Change"}
    - slot{"subject": "Climate Change"}
    - extract_and_validate_entity
    - slot{"subject": "Climate Change"}
    - slot{"requested_slot": null}
    - utter_ask_livewire_content
    - request_livewire_content
    - slot{"requested_slot": "livewire_content"}
* select{"livewire_content": "lorem ipsum dolor sit amet, consectetur adipdcing elit"}
    - slot{"livewire_content": "lorem ipsum dolor sit amet, consectetur adipdcing elit"}
    - extract_and_validate_entity
    - slot{"livewire_content": "lorem ipsum dolor sit amet, consectetur adipdcing elit"}
    - slot{"requested_slot": null}
    - utter_ask_contact_name
    - request_contact_name
    - slot{"requested_slot": "contact_name"}
* select{"contact_name": "Darth Vader"}
    - slot{"contact_name": "Darth Vader"}
    - extract_and_validate_entity
    - slot{"contact_name": "Darth Vader"}
    - slot{"requested_slot": null}
    - utter_ask_contact_number
    - request_contact_number
    - slot{"requested_slot": "contact_number"}
* select{"contact_number": "09454534566"}
    - slot{"contact_number": "09454534566"}
    - extract_and_validate_entity
    - slot{"contact_number": "09454534566"}
    - slot{"requested_slot": null}
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
    - action_utter_livewire_status
    - utter_confirm_request
* affirm
    - action_send_livewire_to_server
    - action_restart

## livewire happy path 2
* take_action
    - utter_actions_menu
* create_livewire
    - utter_confirm_livewire_intent
    - action_get_group
* select{"group_uid": "7a4cf877-26c0-4928-b8e1-13be36bc3fa7"}
    - slot{"group_uid": "7a4cf877-26c0-4928-b8e1-13be36bc3fa7"}
    - utter_ask_subject
    - request_subject
    - slot{"requested_slot": "subject"}
* select{"subject": "New Clinic Opened"}
    - slot{"subject": "New Clinic Opened"}
    - extract_and_validate_entity
    - slot{"subject": "New Clinic Opened"}
    - slot{"requested_slot": null}
    - utter_ask_livewire_content
    - request_livewire_content
    - slot{"requested_slot": "livewire_content"}
* select{"livewire_content": "something happened at a certain location that will affect a certain number of people"}
    - slot{"livewire_content": "something happened at a certain location that will affect a certain number of people"}
    - extract_and_validate_entity
    - slot{"livewire_content": "something happened at a certain location that will affect a certain number of people"}
    - slot{"requested_slot": null}
    - utter_ask_contact_name
    - request_contact_name
    - slot{"requested_slot": "contact_name"}
* select{"contact_name": "Vader"}
    - slot{"contact_name": "Vader"}
    - extract_and_validate_entity
    - slot{"contact_name": "Vader"}
    - slot{"requested_slot": null}
    - utter_ask_contact_number
    - request_contact_number
    - slot{"requested_slot": "contact_number"}
* select{"contact_number": "0845995345"}
    - slot{"contact_number": "0845995345"}
    - extract_and_validate_entity
    - slot{"contact_number": "0845995345"}
    - slot{"requested_slot": null}
    - utter_ask_livewire_location
* select{"longitude": 28.036162200000035, "latitude": -26.1947954}
    - slot{"latitude": -26.1947954}
    - slot{"longitude": 28.036162200000035}
    - utter_location_received
    - utter_ask_add_media_files
* affirm
    - utter_ask_media_file
* select{"media_record_id": "3446456-456-4567-34645656-657657"}
    - slot{"media_record_id": "3446456-456-4567-34645656-657657"}
    - action_save_media_file_id
    - slot{"media_record_ids": ["3446456-456-4567-34645656-657657"]}
    - utter_add_another
* negate
    - action_utter_livewire_status
    - utter_confirm_request
* affirm
    - action_send_livewire_to_server
    - action_restart

## livewire happy path 3
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

# user has chosen a group
> check_for_more_livewire_groups
* select{"group_uid": "Veritas"}
    - slot{"group_uid": "Veritas"}
    - request_subject
    - utter_ask_subject
    - slot{"requested_slot": "subject"}
* select{"subject": "New School Opened"}
    - slot{"subject": "New School Opened"}
    - extract_and_validate_entity
    - slot{"subject": "New School Opened"}
    - utter_ask_livewire_content
    - request_livewire_content
    - slot{"requested_slot": "livewire_content"}
* select{"livewire_content": "Lorem ipsum"}
    - slot{"livewire_content": "Lorem ipsum"}
    - extract_and_validate_entity
    - slot{"livewire_content": "Lorem ipsum"}
    - utter_ask_contact_name
    - request_contact_name
    - slot{"requested_slot": "contact_name"}
* select{"contact_name": "Jon Doe"}
    - slot{"contact_name": "Jon Doe"}
    - extract_and_validate_entity
    - slot{"contact_name": "Jon Doe"}
    - utter_ask_contact_number
    - request_contact_number
    - slot{"requested_slot": "contact_number"}
* select{"contact_number": "066 000 0000"}
    - slot{"contact_number": "066 000 0000"}
    - extract_and_validate_entity
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
    - action_utter_livewire_status
    - utter_confirm_request
> check_livewire_correctness

## request is correct, send request to server
> check_livewire_correctness
* affirm
    - action_send_livewire_to_server
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

# user doesnt have it in them to try again
> restart_livewire_creation
* negate
    - utter_negation
    - action_restart

## fallback story
* out_of_scope
    - action_reroute_to_new_domain
    - action_restart
