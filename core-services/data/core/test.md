## Standard happy path
* find_services
    - utter_confirm_gbv_services
    - utter_services_menu
* select{"service_type":"shelter"}
    - utter_confirm_shelter
* select{"province":"mpumalanga"}
    - action_retrieve_and_send_services
    - utter_anything_else
* negate
    - utter_goodbye
    - action_restart

## Happy path, with gratitude
* find_services
    - utter_confirm_gbv_services
    - utter_services_menu
* select{"service_type":"shelter"}
    - utter_confirm_shelter
* select{"province":"limpopo"}
    - action_retrieve_and_send_services
    - utter_anything_else
* goodbye
    - utter_goodbye
    - action_restart

## Happy path, different service
* find_services_gbv
    - utter_confirm_gbv_services
    - utter_services_menu
* select{"service_type":"thuthuzela"}
    - utter_confirm_thuthuzela
* select{"province":"kzn"}
    - action_retrieve_and_send_services
    - utter_anything_else
* negate
    - utter_goodbye
    - action_restart

## Happy path, using a coordinate
* find_services
    - utter_confirm_gbv_services
    - utter_services_menu
* select{"service_type":"24hr_hcf"}
    - utter_confirm_24hr_hcf
* select{"longitude": 31.0218, "latitude": -29.8587}
    - slot{"latitude": -29.8587}
    - slot{"longitude": 31.0218}
    - action_retrieve_and_send_services
    - utter_anything_else
* negate
    - utter_goodbye
    - action_restart

## Happy path, asking for multiple services
* find_services_gbv
    - utter_confirm_gbv_services
    - utter_services_menu
* select{"service_type":"24hr_hcf"}
    - utter_confirm_24hr_hcf
* select{"longitude": 18.4241, "latitude": -33.9249}
    - slot{"latitude": -33.9249}
    - slot{"longitude": 18.4241}
    - action_retrieve_and_send_services
    - utter_anything_else
* select{"service_type":"thuthuzela"}
    - slot{"service_type": "thuthuzela"}
    - action_retrieve_and_send_services
    - utter_goodbye

## Asking for multiple services, different order
* find_services
    - utter_confirm_gbv_services
    - utter_services_menu
* select{"service_type":"shelter"}
    - utter_confirm_shelter
* select{"longitude": 28.2293, "latitude": -25.7479}
    - slot{"latitude": -25.7479}
    - slot{"longitude": 28.2293}
    - action_retrieve_and_send_services
    - utter_anything_else
* select{"service_type":"24hr_hcf"}
    - slot{"service_type": "24hr_hcf"}
    - action_retrieve_and_send_services
    - utter_goodbye
