## first happy path, no location, no media file, full opening
* take_action
    - utter_actions_menu
* create_livewire
    - livewire_basic_form
    - form{"name": "livewire_basic_form"}
    - form{"name": null}
    - utter_ask_livewire_location
* negate
    - utter_ask_media_file
* negate
    - utter_which_group
* select{"group_uid": ""}
    - action_confirm_livewire
* affirm
    - action_send_livewire
    - utter_goodbye
    - action_restart

## second happy path, location, and media file
* create_livewire
    - livewire_basic_form
    - form{"name": "livewire_basic_form"}
    - form{"name": null}
    - utter_ask_livewire_location
* select{"longitude": 35.4727402464, "latitude": -38.60409879348954}
    - utter_ask_media_file
* select{"media_record_id": "275ee866-ed4d-403d-9332-89e5664b80dc"}
    - action_save_media_file_id
    - utter_which_group
* select{"group_uid": "a6ddebb0-ae6f-4b9f-9be8-0453f1f5d903"}
    - action_confirm_livewire
* affirm
    - action_send_livewire
    - utter_goodbye
    - action_restart

# third, no location, no media file, but straight in (straight to livewire)
* create_livewire
    - livewire_basic_form
    - form{"name": "livewire_basic_form"}
    - form{"name": null}
    - utter_ask_livewire_location
* select{"longitude": 29.97956439506, "latitude": -38.775087447469545}
    - utter_ask_media_file
* negate
    - utter_which_group
* select{"group_uid": "15427c2b-83ae-4a42-8aed-8d926d3923d54"}
    - action_confirm_livewire
* affirm
    - action_send_livewire
    - utter_goodbye
    - action_restart

## fourth, no location, but media file
* take_action
    - utter_actions_menu
* create_livewire
    - livewire_basic_form
    - form{"name": "livewire_basic_form"}
    - form{"name": null}
    - utter_ask_livewire_location
* negate
    - utter_ask_media_file
* select{"media_record_id": "91f7a341-9145-4926-ab7e-f6aace72226b"}
    - action_save_media_file_id
    - utter_which_group
* select{"group_uid": "54c8b420-7041-4ea0-b7ed-2fcab97fd4fd"}
    - action_confirm_livewire
* affirm
    - action_send_livewire
    - utter_goodbye
    - action_restart

# fifth, some confusion on location
* take_action
    - utter_actions_menu
* create_livewire
    - livewire_basic_form
    - form{"name": "livewire_basic_form"}
    - form{"name": null}
    - utter_ask_livewire_location
* why_location
    - utter_explain_livewire_location
* select{"longitude": 20.27707859759183, "latitude": -22.204827094275448}
    - utter_ask_media_file
* negate
    - utter_which_group
* select{"group_uid": "test group"}
    - action_confirm_livewire
* affirm
    - action_send_livewire
    - utter_goodbye
    - action_restart

# sixth, user sends in city name as location
* take_action
    - utter_actions_menu
* create_livewire
    - livewire_basic_form
    - form{"name": "livewire_basic_form"}
    - form{"name": null}
    - utter_ask_livewire_location
* text_location
    - utter_explain_livewire_location
* negate
    - utter_ask_media_file
* select{"media_record_id": "e3c35c50-fa2f-425d-aa01-5070135c9ad1"}
    - utter_which_group
* select{"group_uid": "test group"}
    - action_confirm_livewire
* affirm
    - action_send_livewire
    - utter_goodbye
    - action_restart
    