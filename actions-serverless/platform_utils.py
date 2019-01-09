from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from typing import Dict, Text, Any, List, Union

from rasa_core_sdk import ActionExecutionRejection
from rasa_core_sdk import Tracker
from rasa_core_sdk.executor import CollectingDispatcher
from rasa_core_sdk.forms import FormAction, REQUESTED_SLOT
from rasa_core_sdk import Action
from rasa_core_sdk.events import SlotSet


class RequestSubject(Action):

    def name(self):
        return 'request_subject'

    def run(self, dispatcher, tracker, domain):
        return [SlotSet("requested_slot", "subject")]


class RequestLocation(Action):

    def name(self):
        return 'request_location'

    def run(self, dispatcher, tracker, domain):
        return [SlotSet("requested_slot", "location")]


class RequestDatetime(Action):

    def name(self):
        return 'request_datetime'

    def run(self, dispatcher, tracker, domain):
        return [SlotSet("requested_slot", "datetime")]


class RequestContactName(Action):

    def name(self):
        return 'request_contact_name'

    def run(self, dispatcher, tracker, domain):
        return [SlotSet("requested_slot", "contact_name")]


class RequestContactNumber(Action):

    def name(self):
        return 'request_contact_number'

    def run(self, dispatcher, tracker, domain):
        return [SlotSet("requested_slot", "contact_number")]
        

class RequestLivewireContent(Action):

    def name(self):
        return 'request_livewire_content'

    def run(self, dispatcher, tracker, domain):
        return [SlotSet("requested_slot", "livewire_content")]