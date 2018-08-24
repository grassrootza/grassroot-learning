## action path
* greet
  - utter_greet
  - provide_opening_menu
* act
  - provide_action_menu
* meet

## std action path
* greet
  - utter_greet
  - provide_opening_menu
* know
  - provide_knowledge_menu

## std straight action path
* act
  - provide_action_menu

## service menu
* greet
  - utter_greet
  - provide_opening_menu
* find
  - provide_izwe_lami_service_menu

## straight to find menu, then ask for shelter
* find
  - provide_izwe_lami_service_menu
* request_izwe_lami_service{"izwe_lami_service":"shelter"}
  - utter_goodbye

## straight to find menu, then say goodbye
* find
  - provide_izwe_lami_service_menu
* goodbye
  - utter_goodbye

## goodbye
* goodbye
  - utter_goodbye