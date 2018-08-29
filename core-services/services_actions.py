from rasa_core.actions import Action
from rasa_core.events import SlotSet

import requests
import logging

class ActionRetrieveAndSendServices(Action):
    def name(self):
      # type: () -> Text
      return "action_retrieve_and_send_services"
    
    def run(self, dispatcher, tracker, domain):
      # type: (Dispatcher, DialogueStateTracker, Domain) -> List[Event]
      province = tracker.get_slot('province')
      r = requests.get('http://localhost:3000/province', params = {'province': province})
      logging.warning('requested: {}'.format(r.url))
      dispatcher.utter_message("Hello this is a custom message, you entered province {0}".format(r.text))
      return []