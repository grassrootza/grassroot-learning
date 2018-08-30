## happy path, shelters information
* request_shelters
    - slot{"service_type": "shelter"}
    - utter_confirm_shelters
> request_province_or_pin

## happy path, thuthuzela (rape care clinic) shelters
* request_thuthuzela
    - slot{"service_type": "thuthuzela"}
    - utter_confirm_thuthuzela
> request_province_or_pin

## request province, or pin
> request_province_or_pin
* select{"province":"gauteng"} OR select{"province":"western_cape"} OR select{"province":"eastern_cape"} OR select{"province":"northern_cape"} OR select{"province":"limpopo"} OR select{"province":"mpumalanga"} OR select{"province":"kzn"} OR select{"province":"north_west"} OR select{"province":"free_state"}
    - action_retrieve_and_send_services