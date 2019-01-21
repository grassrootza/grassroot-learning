## first happy path
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
* select{"group_uid": "some_group"}
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
* select{"longitude": 28.036162, "latitude": -26.2949354}
    - utter_ask_media_file
* select{"media_record_id": "235434-345345-2345234444t-34444"}
    - action_save_media_file_id
    - utter_which_group
* select{"group_uid": "234324-234234-23425365-655673"}
    - action_confirm_livewire
* affirm
    - action_send_livewire
    - utter_goodbye
    - action_restart

# first happy path
* take_action
    - utter_actions_menu
* create_livewire
    - livewire_basic_form
    - form{"name": "livewire_basic_form"}
    - form{"name": null}
    - utter_ask_livewire_location
* select{"longitude": 28.0361645672, "latitude": -26.2949354}
    - utter_ask_media_file
* negate
    - utter_which_group
* select{"group_uid": "32534-34-345345345-345345-354354"}
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
* select{"longitude": 28.0365675162, "latitude": -26.2949354}
    - utter_ask_media_file
* select{"media_record_id": "034crt34-34534c34-345vr34v-34v4"}
    - action_save_media_file_id
    - utter_which_group
* select{"group_uid": "235434-34534-43534-5345435"}
    - action_confirm_livewire
* affirm
    - action_send_livewire
    - utter_goodbye
    - action_restart

# first happy path
* take_action
    - utter_actions_menu
* create_livewire
    - livewire_basic_form
    - form{"name": "livewire_basic_form"}
    - form{"name": null}
    - utter_ask_livewire_location
* select{"longitude": 28.03616256756, "latitude": -26.2949354}
    - utter_ask_media_file
* negate
    - utter_which_group
* select{"group_uid": "test group"}
    - action_confirm_livewire
* affirm
    - action_send_livewire
    - utter_goodbye
    - action_restart