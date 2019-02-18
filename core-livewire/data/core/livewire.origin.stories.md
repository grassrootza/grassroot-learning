## first happy path
* take_action
    - utter_actions_menu
* create_livewire
    - action_check_for_groups
    - utter_confirm_livewire
    - livewire_basic_form
    - form{"name": "livewire_basic_form"}
    - form{"name": null}
    - utter_ask_livewire_location
* select{"longitude": 28.036162200000035, "latitude": -26.1947954}
    - utter_ask_media_file
* negate
    - utter_which_group
    - action_get_group
* select{"group_uid": "test_group"}
    - action_confirm_livewire
* affirm
    - action_send_livewire
    - action_restart

## second happy path with media file
* take_action
    - utter_actions_menu
* create_livewire
    - action_check_for_groups
    - utter_confirm_livewire
    - livewire_basic_form
    - form{"name": "livewire_basic_form"}
    - form{"name": null}
    - utter_ask_livewire_location
* select{"longitude": 29.963224743000126, "latitude": -36.78773264934675}
    - utter_ask_media_file
* select{"media_record_id": "e72f99e1-ff56-40bf-83a7-599cefcdddb1"}
    - action_save_media_file_id
    - utter_which_group
    - action_get_group
* select{"group_uid": "test_group"}
    - action_confirm_livewire
* affirm
    - action_send_livewire
    - action_restart

## third happy path, no location, with media file
* take_action
    - utter_actions_menu
* create_livewire
    - action_check_for_groups
    - utter_confirm_livewire
    - livewire_basic_form
    - form{"name": "livewire_basic_form"}
    - form{"name": null}
    - utter_ask_livewire_location
* negate
    - utter_ask_media_file
* select{"media_record_id": "9007169a-11e7-4934-9196-fa6312c201f4"}
    - action_save_media_file_id
    - utter_which_group
    - action_get_group
* select{"group_uid": "test_group"}
    - action_confirm_livewire
* affirm
    - action_send_livewire
    - action_restart

## fourth happy path, no location, with media file
* take_action
    - utter_actions_menu
* create_livewire
    - action_check_for_groups
    - utter_confirm_livewire
    - livewire_basic_form
    - form{"name": "livewire_basic_form"}
    - form{"name": null}
    - utter_ask_livewire_location
* negate
    - utter_ask_media_file
* negate
    - utter_which_group
    - action_get_group
* select{"group_uid": "test_group"}
    - action_confirm_livewire
* affirm
    - action_send_livewire
    - action_restart


## fifth happy path, no media file, user enquires on location then refuses to provide it
* create_livewire
    - action_check_for_groups
    - utter_confirm_livewire
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
    - action_get_group
* select{"group_uid": "test_group"}
    - action_confirm_livewire
* affirm
    - action_send_livewire
    - action_restart

## sixth happy path, no media file, user enquires on location then provides it
* take_action
    - utter_actions_menu
* create_livewire
    - action_check_for_groups
    - utter_confirm_livewire
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
    - action_get_group
* select{"group_uid": "test_group"}
    - action_confirm_livewire
* affirm
    - action_send_livewire
    - action_restart

## seventh happy path, no media file, user enquires on location, enters text location, then correct location
* create_livewire
    - action_check_for_groups
    - utter_confirm_livewire
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
    - action_get_group
* select{"group_uid": "test_group"}
    - action_confirm_livewire
* affirm
    - action_send_livewire
    - action_restart

## eighth happy path, with media file, user enquires on location, enters text location, then correct location
* take_action
    - utter_actions_menu
* create_livewire
    - action_check_for_groups
    - utter_confirm_livewire
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
* select{"media_record_id": "6661e0ea-f543-4792-9335-fb4ece4629d3"}
    - action_save_media_file_id
    - utter_which_group
    - action_get_group
* select{"group_uid": "test_group"}
    - action_confirm_livewire
* affirm
    - action_send_livewire
    - action_restart

## ninth happy path, with media file, wrong location format, then right format
* create_livewire
    - action_check_for_groups
    - utter_confirm_livewire
    - livewire_basic_form
    - form{"name": "livewire_basic_form"}
    - form{"name": null}
    - utter_ask_livewire_location
* text_location
    - utter_explain_livewire_location
* select{"longitude": 26.52412977277335, "latitude": -27.42354589546576}
    - utter_ask_media_file
* select{"media_record_id": "b3f56789-f5bb-4d5c-9455-9bcfd519b5d2"}
    - action_save_media_file_id
    - utter_which_group
    - action_get_group
* select{"group_uid": "test_group"}
    - action_confirm_livewire
* affirm
    - action_send_livewire
    - action_restart

## tenth happy path, no media file, user enquires on location then refuses to provide it, loads multiple group pages
* create_livewire
    - action_check_for_groups
    - utter_confirm_livewire
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
    - action_get_group
* next_page
    - action_increment_page
    - action_get_group
* select{"group_uid": "test_group"}
    - action_confirm_livewire
* affirm
    - action_send_livewire
    - action_restart

#eleventh happy path
* take_action
    - utter_actions_menu
* create_livewire
    - action_check_for_groups
    - utter_confirm_livewire
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
    - action_get_group
* next_page
    - action_increment_page
    - action_get_group
* next_page
    - action_increment_page
    - action_get_group
* select{"group_uid": "test_group"}
    - action_confirm_livewire
* affirm
    - action_send_livewire
    - action_restart

## twelfth happy path
* create_livewire
    - action_check_for_groups
    - utter_confirm_livewire
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
    - action_get_group
* next_page
    - action_increment_page
    - action_get_group
* next_page
    - action_increment_page
    - action_get_group
* next_page
    - action_increment_page
    - action_get_group
* select{"group_uid": "test_group"}
    - action_confirm_livewire
* affirm
    - action_send_livewire
    - action_restart

## 13th happy path
* take_action
    - utter_actions_menu
* create_livewire
    - action_check_for_groups
    - utter_confirm_livewire
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
* select{"media_record_id": "c8498498-fc6b-4ba4-a5db-4f2e2f1c1862"}
    - action_save_media_file_id
    - utter_which_group
    - action_get_group
* next_page
    - action_increment_page
    - action_get_group
* next_page
    - action_increment_page
    - action_get_group
* next_page
    - action_increment_page
    - action_get_group
* next_page
    - action_increment_page
    - action_get_group
* select{"group_uid": "test_group"}
    - action_confirm_livewire
* affirm
    - action_send_livewire
    - action_restart

## 14th happy path
* create_livewire
    - action_check_for_groups
    - utter_confirm_livewire
    - livewire_basic_form
    - form{"name": "livewire_basic_form"}
    - form{"name": null}
    - utter_ask_livewire_location
* text_location
    - utter_explain_livewire_location
* select{"longitude": 26.52412977277335, "latitude": -27.42354589546576}
    - utter_ask_media_file
* select{"media_record_id": "488f83db-d306-441c-a79c-545ce87c32b5"}
    - action_save_media_file_id
    - utter_further_media_file
    - utter_which_group
    - action_get_group
* next_page
    - action_increment_page
    - action_get_group
* next_page
    - action_increment_page
    - action_get_group
* next_page
    - action_increment_page
    - action_get_group
* next_page
    - action_increment_page
    - action_get_group
* next_page
    - action_increment_page
    - action_get_group
* select{"group_uid": "test_group"}
    - action_confirm_livewire
* affirm
    - action_send_livewire
    - action_restart

## 15th happy path
* take_action
    - utter_actions_menu
* create_livewire
    - action_check_for_groups
    - utter_confirm_livewire
    - livewire_basic_form
    - form{"name": "livewire_basic_form"}
    - form{"name": null}
    - utter_ask_livewire_location
* select{"longitude": 29.963224743000126, "latitude": -36.78773264934675}
    - utter_ask_media_file
* select{"media_record_id": "f8c9410d-629e-4578-a3a1-dbea87b1b6e9"}
    - action_save_media_file_id
    - utter_further_media_file
* select{"media_record_id": "7cea8886-a7e6-4e64-8728-9af4ffc99745"}
    - action_save_media_file_id
    - utter_further_media_file
* negate
    - utter_which_group
    - action_get_group
* select{"group_uid": "test_group"}
    - action_confirm_livewire
* affirm
    - action_send_livewire
    - action_restart

## 16th happy path
* take_action
    - utter_actions_menu
* create_livewire
    - action_check_for_groups
    - utter_confirm_livewire
    - livewire_basic_form
    - form{"name": "livewire_basic_form"}
    - form{"name": null}
    - utter_ask_livewire_location
* negate
    - utter_ask_media_file
* select{"media_record_id": "7fc3cc91-a050-42cf-b8e5-cf3eceb426cb"}
    - action_save_media_file_id
    - utter_further_media_file
* select{"media_record_id": "8051d226-9daf-436c-9b72-b301b3ad8045"}
    - action_save_media_file_id
    - utter_further_media_file
* select{"media_record_id": "4aea7019-7167-4632-8441-0ab9d3925627"}
    - action_save_media_file_id
    - utter_further_media_file
* negate
    - utter_which_group
    - action_get_group
* select{"group_uid": "test_group"}
    - action_confirm_livewire
* affirm
    - action_send_livewire
    - action_restart

## 17th happy path
* take_action
    - utter_actions_menu
* create_livewire
    - action_check_for_groups
    - utter_confirm_livewire
    - livewire_basic_form
    - form{"name": "livewire_basic_form"}
    - form{"name": null}
    - utter_ask_livewire_location
* negate
    - utter_ask_media_file
* negate
    - utter_which_group
    - action_get_group
* select{"group_uid": "test_group"}
    - action_confirm_livewire
* affirm
    - action_send_livewire
    - action_restart

## 18th happy path
* take_action
    - utter_actions_menu
* create_livewire
    - action_check_for_groups
    - utter_confirm_livewire
    - livewire_basic_form
    - form{"name": "livewire_basic_form"}
    - form{"name": null}
    - utter_ask_livewire_location
* why_location
    - utter_why_location
* select{"longitude": 39.4865452840113, "latitude": -27.462631882480874}
    - utter_ask_media_file
* select{"media_record_id": "5387df44-67cb-4e82-83ef-5b9177ecb6c0"}
    - action_save_media_file_id
    - utter_further_media_file
* select{"media_record_id": "dbbe0e70-79f5-4204-ab6c-0dd59178d659"}
    - action_save_media_file_id
    - utter_further_media_file
* select{"media_record_id": "ec7bc90c-a40d-4a0a-9da2-61e1986a67e9"}
    - action_save_media_file_id
    - utter_further_media_file
* negate
    - utter_which_group
    - action_get_group
* select{"group_uid": "test_group"}
    - action_confirm_livewire
* affirm
    - action_send_livewire
    - action_restart

## 19th happy path
* take_action
    - utter_actions_menu
* create_livewire
    - action_check_for_groups
    - utter_confirm_livewire
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
    - utter_further_media_file
* select{"media_record_id": "8c33e36b-ff1a-4a6e-a946-ec63d3c9d92d"}
    - action_save_media_file_id
    - utter_further_media_file
* select{"media_record_id": "2591f578-45c4-4dde-802c-ae5da517d718"}
    - action_save_media_file_id
    - utter_further_media_file
* select{"media_record_id": "adcf3323-14d6-4cb1-98aa-06a91c8af63c"}
    - action_save_media_file_id
    - utter_further_media_file
* negate
    - utter_which_group
    - action_get_group
* select{"group_uid": "test_group"}
    - action_confirm_livewire
* affirm
    - action_send_livewire
    - action_restart

## 20th happy path
* create_livewire
    - action_check_for_groups
    - utter_confirm_livewire
    - livewire_basic_form
    - form{"name": "livewire_basic_form"}
    - form{"name": null}
    - utter_ask_livewire_location
* text_location
    - utter_explain_livewire_location
* select{"longitude": 26.52412977277335, "latitude": -27.42354589546576}
    - utter_ask_media_file
* select{"media_record_id": "f26b8945-fa96-4ce4-bdbd-a14522d33350"}
    - action_save_media_file_id
    - utter_further_media_file
* select{"media_record_id": "947d499f-1858-43bb-bffd-8cc7a794c62b"}
    - action_save_media_file_id
    - utter_further_media_file
* negate
    - utter_which_group
    - action_get_group
* select{"group_uid": "test_group"}
    - action_confirm_livewire
* affirm
    - action_send_livewire
    - action_restart

## 21st happy path
* take_action
    - utter_actions_menu
* create_livewire
    - action_check_for_groups
    - utter_confirm_livewire
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
* select{"media_record_id": "55c81565-40df-4ec4-86ca-a448d29844d0"}
    - action_save_media_file_id
    - utter_further_media_file
* select{"media_record_id": "2e9f2a67-ea5a-4ae1-b451-8176547ceaae"}
    - action_save_media_file_id
    - utter_further_media_file
* select{"media_record_id": "a47f7fa8-5c1c-4867-979c-679acb843696"}
    - action_save_media_file_id
    - utter_further_media_file
* negate
    - utter_which_group
    - action_get_group
* next_page
    - action_increment_page
    - action_get_group
* next_page
    - action_increment_page
    - action_get_group
* next_page
    - action_increment_page
    - action_get_group
* next_page
    - action_increment_page
    - action_get_group
* select{"group_uid": "test_group"}
    - action_confirm_livewire
* affirm
    - action_send_livewire
    - action_restart

## 22nd happy path
* create_livewire
    - action_check_for_groups
    - utter_confirm_livewire
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
    - utter_further_media_file
* select{"media_record_id": "55c81565-40df-4ec4-86ca-a448d29844d0"}
    - action_save_media_file_id
    - utter_further_media_file
* select{"media_record_id": "55c81565-40df-4ec4-86ca-a448d29844d0"}
    - action_save_media_file_id
    - utter_further_media_file
* select{"media_record_id": "55c81565-40df-4ec4-86ca-a448d29844d0"}
    - action_save_media_file_id
    - utter_further_media_file
* negate
    - utter_which_group
    - action_get_group
* next_page
    - action_increment_page
    - action_get_group
* next_page
    - action_increment_page
    - action_get_group
* next_page
    - action_increment_page
    - action_get_group
* next_page
    - action_increment_page
    - action_get_group
* next_page
    - action_increment_page
    - action_get_group
* select{"group_uid": "test_group"}
    - action_confirm_livewire
* affirm
    - action_send_livewire
    - action_restart