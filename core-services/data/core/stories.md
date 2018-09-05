## happy path, from start, for health care facilities
* find_services
    - utter_confirm_gbv_services
* select{"service_type":"24hr_hcf"}
    - utter_confirm_24hr_hcf
> request_province_or_pin

## same as above, for shelters
* find_services
    - utter_confirm_gbv_services
* select{"service_type":"shelter"}
    - utter_confirm_shelter
> request_province_or_pin

## and for thuthuzela
* find_services
    - utter_confirm_gbv_services
* select{"service_type":"thuthuzela"}
    - utter_confirm_thuthuzela
> request_province_or_pin

## happy path, straight to gbv intent
* find_services_gbv
    - utter_confirm_gbv_services
* select{"service_type":"24hr_hcf"}
    - utter_confirm_24hr_hcf
> request_province_or_pin

## same as above, for shelters
* find_services_gbv
    - utter_confirm_gbv_services
* select{"service_type":"shelter"}
    - utter_confirm_shelter
> request_province_or_pin

## and for thuthuzela
* find_services_gbv
    - utter_confirm_gbv_services
* select{"service_type":"thuthuzela"}
    - utter_confirm_thuthuzela
> request_province_or_pin

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

## request province, or pin, and provide a province
> request_province_or_pin
* select{"province":"gauteng"} OR select{"province":"western_cape"} OR select{"province":"eastern_cape"} OR select{"province":"northern_cape"} OR select{"province":"limpopo"} OR select{"province":"mpumalanga"} OR select{"province":"kzn"} OR select{"province":"north_west"} OR select{"province":"free_state"}
    - action_retrieve_and_send_services

## request province, or pin, and provide a pin, as a dict
> request_province_or_pin
* select{"geo_location":"{latitude:\"-26.1947954\",longitude:\"28.036162200000035\"}"}
    - action_retrieve_and_send_services

## request province, or pin, and provide a pin, as two floats
> request_province_or_pin
* select{"latitude":-26.1947954,"longitude":28.036162200000035}
    - action_retrieve_and_send_services