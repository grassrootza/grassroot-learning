## happy path, from start, for health care facilities
* find_services
    - utter_confirm_gbv_services
    - utter_services_menu
* select{"service_type":"24hr_hcf"}
    - utter_confirm_24hr_hcf
> request_province_or_pin

## same as above, for shelters
* find_services
    - utter_confirm_gbv_services
    - utter_services_menu
* select{"service_type":"shelter"}
    - utter_confirm_shelter
> request_province_or_pin

## and for thuthuzela
* find_services
    - utter_confirm_gbv_services
    - utter_services_menu
* select{"service_type":"thuthuzela"}
    - utter_confirm_thuthuzela
> request_province_or_pin

## a longer story, trying to reinforce memory
* find_services
    - utter_confirm_gbv_services
    - utter_services_menu
* select{"service_type":"thuthuzela"}
    - utter_confirm_thuthuzela
* select{"province":"gauteng"}
    - action_retrieve_and_send_services
    - utter_anything_else
* goodbye
    - utter_goodbye
    - action_restart

## happy path, straight to gbv intent
* find_services_gbv
    - utter_confirm_gbv_services
    - utter_services_menu
* select{"service_type":"24hr_hcf"}
    - utter_confirm_24hr_hcf
> request_province_or_pin

## same as above, for shelters
* find_services_gbv
    - utter_confirm_gbv_services
    - utter_services_menu
* select{"service_type":"shelter"}
    - utter_confirm_shelter
> request_province_or_pin

## and for thuthuzela
* find_services_gbv
    - utter_confirm_gbv_services
    - utter_services_menu
* select{"service_type":"thuthuzela"}
    - utter_confirm_thuthuzela
> request_province_or_pin

## happy path, repeating / emphasizing
* find_services_gbv
    - utter_confirm_gbv_services
    - utter_services_menu
* select{"service_type":"thuthuzela"}
    - utter_confirm_thuthuzela
* select{"province":"gauteng"}
    - action_retrieve_and_send_services
    - utter_anything_else
* goodbye
    - utter_goodbye
    - action_restart

## happy path, repeating / emphasizing
* find_services_gbv
    - utter_confirm_gbv_services
    - utter_services_menu
* select{"service_type":"thuthuzela"}
    - utter_confirm_thuthuzela
* select{"province":"gauteng"} OR select{"province":"western_cape"} OR select{"province":"eastern_cape"} OR select{"province":"northern_cape"} OR select{"province":"limpopo"} OR select{"province":"mpumalanga"} OR select{"province":"kzn"} OR select{"province":"north_west"} OR select{"province":"free_state"}
    - action_retrieve_and_send_services
    - utter_anything_else
* negate
    - utter_goodbye
    - action_restart

## happy path, shelters information
* request_shelter
    - slot{"service_type": "shelter"}
    - utter_confirm_shelter
> request_province_or_pin

## happy path, thuthuzela (rape care clinic) shelters
* request_thuthuzela
    - slot{"service_type": "thuthuzela"}
    - utter_confirm_thuthuzela
> request_province_or_pin

## happy path, straight to clinic
* request_24hr_hcf
    - slot{"service_type": "24hr_hcf"}
    - utter_confirm_24hr_hcf
> request_province_or_pin

## Generated Story -3893191575660869171
* select{"service_type": "shelter"}
    - slot{"service_type": "shelter"}
    - utter_confirm_shelter
* select{"province": "gauteng"}
    - slot{"province": "gauteng"}
    - action_retrieve_and_send_services

## Generated Story -1895316140752856410
* select{"service_type": "thuthuzela"}
    - slot{"service_type": "thuthuzela"}
    - utter_confirm_thuthuzela
* select{"province": "western_cape"}
    - slot{"province": "western_cape"}
    - action_retrieve_and_send_services

## Generated Story -6046854158320525225
* select{"service_type": "thuthuzela"}
    - slot{"service_type": "thuthuzela"}
    - utter_confirm_thuthuzela
* select{"province": "limpopo"}
    - slot{"province": "limpopo"}
    - action_retrieve_and_send_services

## Generated Story 1698526148454156378
* select{"service_type": "24hr_hcf"}
    - slot{"service_type": "24hr_hcf"}
    - utter_confirm_24hr_hcf
* select{"longitude": 28.036162200000035, "latitude": -26.1947954}
    - slot{"latitude": -26.1947954}
    - slot{"longitude": 28.036162200000035}
    - action_retrieve_and_send_services

## request province, or pin, and provide a province
> request_province_or_pin
* select{"province":"gauteng"} OR select{"province":"western_cape"} OR select{"province":"eastern_cape"} OR select{"province":"northern_cape"} OR select{"province":"limpopo"} OR select{"province":"mpumalanga"} OR select{"province":"kzn"} OR select{"province":"north_west"} OR select{"province":"free_state"}
    - action_retrieve_and_send_services
    - utter_anything_else
* negate OR goodbye
    - utter_goodbye
    - action_restart

## request province, or pin, and provide a province
> request_province_or_pin
* select{"province":"gauteng"} OR select{"province":"western_cape"} OR select{"province":"eastern_cape"} OR select{"province":"northern_cape"} OR select{"province":"limpopo"} OR select{"province":"mpumalanga"} OR select{"province":"kzn"} OR select{"province":"north_west"} OR select{"province":"free_state"}
    - action_retrieve_and_send_services
    - utter_anything_else
* affirm
    - action_service_type_reset
    - utter_menu_second_service
    - utter_services_menu
* select{"service_type": "24hr_hcf"} OR select{"service_type":"shelter"} OR select{"service_type": "thuthuzela"}
> request_province_or_pin

## request province, or pin, and provide a pin, as a dict
> request_province_or_pin
* select{"geo_location":"{latitude:\"-26.1947954\",longitude:\"28.036162200000035\"}"}
    - action_retrieve_and_send_services
    - utter_anything_else
* negate OR goodbye
    - utter_goodbye
    - action_restart

## request province, or pin, and provide a pin, as two floats
> request_province_or_pin
* select{"latitude":-26.1947954,"longitude":28.036162200000035}
    - action_retrieve_and_send_services
    - utter_anything_else
* negate OR goodbye
    - utter_goodbye
    - action_restart

## request province, or pin, and provide a province
> request_province_or_pin
* select{"province":"gauteng"} OR select{"province":"western_cape"} OR select{"province":"eastern_cape"} OR select{"province":"northern_cape"} OR select{"province":"limpopo"} OR select{"province":"mpumalanga"} OR select{"province":"kzn"} OR select{"province":"north_west"} OR select{"province":"free_state"}
    - action_retrieve_and_send_services
    - utter_anything_else
* select{"service_type": "24hr_hcf"} OR select{"service_type":"shelter"} OR select{"service_type": "thuthuzela"}
    - action_retrieve_and_send_services
    - utter_goodbye
    - action_restart
