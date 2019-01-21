## first happy path
* take_action
    - utter_actions_menu
* create_livewire
    - livewire_basic_form
    - form{"name": "livewire_basic_form"}
    - form{"name": null}
    - utter_ask_livewire_location
* select{"longitude": 28.036162200000035, "latitude": -26.1947954}
    - utter_ask_media_file
* negate
    - utter_which_group
* select{"group_uid": "test_group"}
    - action_confirm_livewire
* affirm
    - action_send_livewire
    - utter_goodbye
    - action_restart

## second happy path with media file
* take_action
    - utter_actions_menu
* create_livewire
    - livewire_basic_form
    - form{"name": "livewire_basic_form"}
    - form{"name": null}
    - utter_ask_livewire_location
* select{"longitude": 28.036162200000035, "latitude": -26.1947954}
    - utter_ask_media_file
* select{"media_record_id": "034crt34-34534c34-345vr34v-34v4"}
    - action_save_media_file_id
    - utter_which_group
* select{"group_uid": "test_group"}
    - action_confirm_livewire
* affirm
    - action_send_livewire
    - utter_goodbye
    - action_restart