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
* select{"media_record_id": "55c81565-40df-4ec4-86ca-a448d29844d0"}
    - action_save_media_file_id
    - utter_which_group
* select{"group_uid": "test_group"}
    - action_confirm_livewire
* affirm
    - action_send_livewire
    - utter_goodbye
    - action_restart

## third happy path, no location, with media file
* take_action
    - utter_actions_menu
* create_livewire
    - livewire_basic_form
    - form{"name": "livewire_basic_form"}
    - form{"name": null}
    - utter_ask_livewire_location
* negate
    - utter_ask_media_file
* select{"media_record_id": "3a370932-ec3d-4d68-9a1a-596f0a3ff5af4"}
    - action_save_media_file_id
    - utter_which_group
* select{"group_uid": "test_group"}
    - action_confirm_livewire
* affirm
    - action_send_livewire
    - utter_goodbye
    - action_restart

## fourth happy path, no location, with media file
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
* select{"group_uid": "test_group"}
    - action_confirm_livewire
* affirm
    - action_send_livewire
    - utter_goodbye
    - action_restart


## fifth happy path, no media file, user enquires on location then refuses to provide it
* take_action
    - utter_actions_menu
* create_livewire
    - livewire_basic_form
    - form{"name": "livewire_basic_form"}
    - form{"name": null}
    - utter_ask_livewire_location
* why_location
    - utter_why_location
* negate
    - utter_ask_media_file
* negate
    - utter_which_group
* select{"group_uid": "test_group"}
    - action_confirm_livewire
* affirm
    - action_send_livewire
    - utter_goodbye
    - action_restart

## sixth happy path, no media file, user enquires on location then provides it
* take_action
    - utter_actions_menu
* create_livewire
    - livewire_basic_form
    - form{"name": "livewire_basic_form"}
    - form{"name": null}
    - utter_ask_livewire_location
* why_location
    - utter_why_location
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

## seventh happy path, no media file, user enquires on location, enters text location, then correct location
* take_action
    - utter_actions_menu
* create_livewire
    - livewire_basic_form
    - form{"name": "livewire_basic_form"}
    - form{"name": null}
    - utter_ask_livewire_location
* why_location
    - utter_why_location
* text_location
    - utter_explain_livewire_location
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

## eighth happy path, with media file, user enquires on location, enters text location, then correct location
* take_action
    - utter_actions_menu
* create_livewire
    - livewire_basic_form
    - form{"name": "livewire_basic_form"}
    - form{"name": null}
    - utter_ask_livewire_location
* why_location
    - utter_why_location
* text_location
    - utter_explain_livewire_location
* select{"longitude": 28.036162200000035, "latitude": -26.1947954}
    - utter_ask_media_file
* select{"media_record_id": "3a370932-ec3d-4d68-9a1a-596f0a3ff5af4"}
    - action_save_media_file_id
    - utter_which_group
* select{"group_uid": "test_group"}
    - action_confirm_livewire
* affirm
    - action_send_livewire
    - utter_goodbye
    - action_restart

## ninth happy path, with media file, wrong location format, then right format
* take_action
    - utter_actions_menu
* create_livewire
    - livewire_basic_form
    - form{"name": "livewire_basic_form"}
    - form{"name": null}
    - utter_ask_livewire_location
* text_location
    - utter_explain_livewire_location
* select{"longitude": 28.036162200000035, "latitude": -26.1947954}
    - utter_ask_media_file
* select{"media_record_id": "3a370932-ec3d-4d68-9a1a-596f0a3ff5af4"}
    - action_save_media_file_id
    - utter_which_group
* select{"group_uid": "test_group"}
    - action_confirm_livewire
* affirm
    - action_send_livewire
    - utter_goodbye
    - action_restart