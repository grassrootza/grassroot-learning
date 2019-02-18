## meeting, first happy path
* take_action
    - utter_actions_menu
* call_meeting
    - action_check_for_groups
    - utter_confirm_meeting
    - meeting_basic_form
    - form{"name": "meeting_basic_form"}
    - form{"name": null}
    - utter_which_meeting_group
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
    - action_confirm_meeting
* affirm
    - action_send_meeting
    - action_restart

## meeting, second happy path
* call_meeting
    - action_check_for_groups
    - utter_confirm_meeting
    - meeting_basic_form
    - form{"name": "meeting_basic_form"}
    - form{"name": null}
    - utter_which_meeting_group
    - action_get_group
* next_page
    - action_increment_page
    - action_get_group
* next_page
    - action_increment_page
    - action_get_group
* select{"group_uid": "test_group"}
    - action_confirm_meeting
* affirm
    - action_send_meeting
    - action_restart

## meeting, third happy path
* take_action
    - utter_actions_menu
* call_meeting
    - action_check_for_groups
    - utter_confirm_meeting
    - meeting_basic_form
    - form{"name": "meeting_basic_form"}
    - form{"name": null}
    - utter_which_meeting_group
    - action_get_group
* next_page
    - action_increment_page
    - action_get_group
* select{"group_uid": "test_group"}
    - action_confirm_meeting
* affirm
    - action_send_meeting
    - action_restart

## meeting, 4th happy path
* call_meeting
    - action_check_for_groups
    - utter_confirm_meeting
    - meeting_basic_form
    - form{"name": "meeting_basic_form"}
    - form{"name": null}
    - utter_which_meeting_group
    - action_get_group
* next_page
    - action_increment_page
    - action_get_group
* select{"group_uid": "test_group"}
    - action_confirm_meeting
* affirm
    - action_send_meeting
    - action_restart

## meeting, fifth happy path
* take_action
    - utter_actions_menu
* call_meeting
    - action_check_for_groups
    - utter_confirm_meeting
    - meeting_basic_form
    - form{"name": "meeting_basic_form"}
    - form{"name": null}
    - utter_which_meeting_group
    - action_get_group
* select{"group_uid": "test_group"}
    - action_confirm_meeting
* affirm
    - action_send_meeting
    - action_restart

## meeting, sixth happy path
* call_meeting
    - action_check_for_groups
    - utter_confirm_meeting
    - meeting_basic_form
    - form{"name": "meeting_basic_form"}
    - form{"name": null}
    - utter_which_meeting_group
    - action_get_group
* select{"group_uid": "test_group"}
    - action_confirm_meeting
* affirm
    - action_send_meeting
    - action_restart
