## first happy path
* take_action
    - utter_actions_menu
* call_meeting
    - meeting_basic_form
    - form{"name": "meeting_basic_form"}
    - form{"name": "null"}
    - utter_which_group
* select{"group_uid": "test_group"}
    - action_confirm_meeting
* affirm
    - action_send_meeting
    - utter_goodbye
    - action_restart