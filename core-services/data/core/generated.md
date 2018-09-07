## Generated Story 1698526148454156378
* select{"service_type": "24hr_hcf"}
    - slot{"service_type": "24hr_hcf"}
    - utter_confirm_24hr_hcf
* select{"longitude": 28.036162200000035, "latitude": -26.1947954}
    - slot{"latitude": -26.1947954}
    - slot{"longitude": 28.036162200000035}
    - action_retrieve_and_send_services
    - utter_anything_else
* negate
    - utter_goodbye
    - action_restart
## Generated Story -9093216445291346611
* select{"service_type": "thuthuzela"}
    - slot{"service_type": "thuthuzela"}
    - utter_confirm_thuthuzela
* select{"province": "limpopo"}
    - slot{"province": "limpopo"}
    - action_retrieve_and_send_services
    - utter_anything_else
* goodbye
    - utter_goodbye
    - action_restart
## Generated Story 1391153024072838405
* select{"service_type": "shelter"}
    - slot{"service_type": "shelter"}
    - utter_confirm_shelter
* select{"province": "eastern_cape"}
    - slot{"province": "eastern_cape"}
    - action_retrieve_and_send_services
    - utter_anything_else
* affirm
    - action_service_type_reset
    - utter_services_menu_reset
## Generated Story (alternate)
* select{"service_type": "shelter"}
    - slot{"service_type": "shelter"}
    - utter_confirm_shelter
* select{"province": "eastern_cape"}
    - slot{"province": "eastern_cape"}
    - action_retrieve_and_send_services
    - utter_anything_else
* affirm
    - action_service_type_reset
    - utter_services_menu_reset
* select{"service_type": "thuthuzela"}
    - action_retrieve_and_send_services
    - utter_goodbye
    - action_restart
## Generated Story -7528961615721468854
* find_services
    - utter_confirm_gbv_services
* select{"service_type": "shelter"}
    - slot{"service_type": "shelter"}
    - utter_confirm_shelter
* select{"province": "limpopo"}
    - slot{"province": "limpopo"}
    - action_retrieve_and_send_services
    - utter_anything_else
* affirm
    - action_service_type_reset
    - utter_services_menu_reset
* select{"service_type": "thuthuzela"}
    - slot{"service_type": "thuthuzela"}
    - action_retrieve_and_send_services
    - utter_goodbye
    - action_restart

## Generated Story 5424264101651828142
* find_services_gbv
    - utter_confirm_gbv_services
* select{"service_type": "24hr_hcf"}
    - slot{"service_type": "24hr_hcf"}
    - utter_confirm_24hr_hcf
* select{"longitude": "28.0365738", "latitude": "-26.1514362"}
    - slot{"latitude": "-26.1514362"}
    - slot{"longitude": "28.0365738"}
    - action_retrieve_and_send_services
    - utter_anything_else
* affirm
    - action_service_type_reset
    - slot{"service_type": null}
    - utter_services_menu_reset
* select{"service_type": "shelter"}
    - slot{"service_type": "shelter"}
    - action_retrieve_and_send_services
    - utter_goodbye
    - action_restart
