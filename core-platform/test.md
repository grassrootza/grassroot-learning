## meeting path 1
* take_action
  - utter_actions_initialiser
  - utter_actions_menu
* call_meeting
  - utter_confirm_meeting_intent
  - slot{"action": "call_meeting"}
  - action_get_group
* select{"group_uid": "0a56b88b-25f7-4365-aa3b-bbe9b903a143"}
  - slot{"group_uid": "0a56b88b-25f7-4365-aa3b-bbe9b903a143"}
  - action_create_meeting_routine
  - slot{"requested_slot": "subject"}
* select{"subject": "Environmental awareness"}
  - action_create_meeting_routine
  - slot{"subject": "Environmental awareness"}
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

## livewire, path 1
* take_action
  - utter_actions_initialiser
  - utter_actions_menu
* create_livewire
  - utter_confirm_livewire_intent
  - action_get_group
* select{"group_uid": "0a56b88b-25f7-4365-aa3b-bbe9b903a143"}
  - slot{"group_uid": "0a56b88b-25f7-4365-aa3b-bbe9b903a143"}
  - action_livewire_routine
  - slot{"requested_slot": "subject"}
* select{"subject": "New Clinic Open"}
  - action_livewire_routine
  - slot{"subject": "New Clinic Open"}
  - utter_ask_livewire_content
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
* select{"media_record_ids": ["762aef58-4865-407a-b793-af6114ab3444"]}
  - slot{"media_record_ids": ["762aef58-4865-407a-b793-af6114ab3444"]}
  - action_save_media_file_id
  - utter_add_another
* affirm
  - utter_ask_media_file
* select{"media_record_ids": ["762aef58-4865-407a-b793-af6114ab3444"]}
  - slot{"media_record_ids": ["762aef58-4865-407a-b793-af6114ab3444"]}
  - action_save_media_file_id
  - utter_add_another
* negate
  - utter_location_or_not
* affirm
  - utter_ask_livewire_location
* select{"longitude": 28.036162200000035, "latitude": -26.1947954}
  - slot{"latitude": -26.1947954}
  - slot{"longitude": 28.036162200000035}
  - utter_location_received
  - action_utter_livewire_status
  - utter_confirm_request
* affirm
  - action_create_livewire_complete
  - action_restart


