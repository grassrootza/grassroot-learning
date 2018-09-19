from rasa_core_sdk import Action
from rasa_core_sdk.events import SlotSet
from rasa_core_sdk.events import AllSlotsReset
from rasa_core_sdk.events import Restarted

import os
import requests
import logging
import json

# need this just to map from newer friendlier better naming convention to that in lambda / dynamodb 
services_name_map = {
  'shelter': 'NSM',
  'thuthuzela': 'TCC',
  '24hr_hcf': 'HCF'
}

province_param_map = {
  'gauteng': 'ZA_GP',
  'western_cape': 'ZA_WC',
  'eastern_cape': 'ZA_EC',
  'northern_cape': 'ZA_NC',
  'limpopo': 'ZA_LP',
  'mpumalanga': 'ZA_MP',
  'kzn': 'ZA_KZN',
  'north_west': 'ZA_NW',
  'free_state': 'ZA_FS'
}

class ActionRetrieveAndSendServices(Action):
    def name(self):
      # type: () -> Text
      return "action_retrieve_and_send_services"


    def run(self, dispatcher, tracker, domain):
      # type: (Dispatcher, DialogueStateTracker, Domain) -> List[Event]
      # r = requests.get('http://localhost:3001/province', params = {'province': province})
      
      if (not isServiceTypeSelected(tracker)):
        dispatcher.utter_template('utter_services_menu', tracker)
      elif (not isLocationPresent(tracker)):
        dispatcher.utter_template('utter_generic_location', tracker)
      else:
        if hasLongLat(tracker):
          r = self._findClinicsByLongLat(tracker)
        else:
          r = self._findServiceByProvince(tracker)

        logging.info('requested: {}'.format(r.url))
        logging.info('result messages: {}'.format(r.text))

        responseArray = transformResponse(tracker.get_slot('service_type'), r)
        
        logging.info('as response messages: {}'.format(responseArray))

        dispatcher.utter_template('utter_pre_services', tracker)
        for response in responseArray:
          dispatcher.utter_message(response)
        dispatcher.utter_template('utter_post_services', tracker)
      
      return []


    def _findClinicsByLongLat(self, tracker):
      longitude = tracker.get_slot('longitude')
      latitude = tracker.get_slot('latitude')
      service = tracker.get_slot('service_type')
      logging.info('Got coordinates: longitude = {}, latitude = {}, and looking for service = {}'.format(longitude, latitude, service))
      infoUrl = os.getenv('LONG_LAT_LAMBDA_URL', 'http://localhost:3001/longlat')
      return requests.get(infoUrl, params = {'longitude': longitude, 'latitude': latitude, 'service': services_name_map[service]})


    def _findServiceByProvince(self, tracker):
      province = tracker.get_slot('province')
      service = tracker.get_slot('service_type')
      logging.info('Getting province: {}, for service: {}'.format(province, service))
      provinceUrl = os.getenv('PROVINCE_SERVICE_URL', 'http://localhost:3001/province')
      return requests.get(provinceUrl, params = { 'province': province_param_map[province], 'service': services_name_map[service] })    


def isServiceTypeSelected(tracker):
  return tracker.get_slot('service_type') is not None


def isLocationPresent(tracker):
  return tracker.get_slot('province') is not None or hasLongLat(tracker) 


def hasLongLat(tracker):
  return (tracker.get_slot('geo_location') is not None 
  or (tracker.get_slot('latitude') is not None and tracker.get_slot('longitude') is not None))


def transformResponse(service, response):
      if (service != '24hr_hcf'):
        return json.loads(response.text)
      else:
        return list(map(lambda clinic: clinic['key'], json.loads(response.text)))


class ActionAllSlotsReset(Action): 	
    def name(self): 		
        return 'action_all_slot_reset' 	
    def run(self, dispatcher, tracker, domain): 		
        return[AllSlotsReset()]


class ActionServiceTypeReset(Action):
    def name(self):
        return 'action_service_type_reset'
    def run(self, dispatcher, tracker, domain):
        return[SlotSet('service_type', None)]
