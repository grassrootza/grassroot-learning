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
* select{"longitude": 29.963224743000126, "latitude": -36.78773264934675}
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
* select{"media_record_id": "7fc3cc91-a050-42cf-b8e5-cf3eceb426cb"}
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
* select{"longitude": 39.4865452840113, "latitude": -27.462631882480874}
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
* create_livewire
    - livewire_basic_form
    - form{"name": "livewire_basic_form"}
    - form{"name": null}
    - utter_ask_livewire_location
* why_location
    - utter_why_location
* text_location
    - utter_explain_livewire_location
* select{"longitude": 23.957154139186457, "latitude": -24.81948868219614}
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
* select{"longitude": 22.18221549685437, "latitude": -32.44978668214415}
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
* create_livewire
    - livewire_basic_form
    - form{"name": "livewire_basic_form"}
    - form{"name": null}
    - utter_ask_livewire_location
* text_location
    - utter_explain_livewire_location
* select{"longitude": 26.52412977277335, "latitude": -27.42354589546576}
    - utter_ask_media_file
* select{"media_record_id": "f9b60411-ea04-472a-a32a-eb501cc8255f"}
    - action_save_media_file_id
    - utter_which_group
* select{"group_uid": "test_group"}
    - action_confirm_livewire
* affirm
    - action_send_livewire
    - utter_goodbye
    - action_restart