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