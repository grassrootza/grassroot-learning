import logging

from rasa_core_sdk import Action
from rasa_core_sdk.forms import FormAction

class LiveWireBasicFormAction(FormAction):
    """Form action to fill out basic details for a LiveWire alert"""

    def name(self):
        # type: () -> Text
        return "livewire_basic_form"
    
    @staticmethod
    def required_slots(tracker):
        # type: () -> List[Text]
        logging.info("Returning required slot set")
        return ["subject", "content", "contact_name", "contact_number"]

    def slot_mappings(self):
        return {"subject": self.from_text(), "content": self.from_text(), "contact_name": self.from_text(), 
            "contact_number": self.from_text()}

    def submit(self, dispatcher, tracker, domain):
        logging.critical("Completed form")
        return []


class ActionGetGroup(Action):
    def name(self):
        return 'action_get_group'

    def run(self, dispatcher, tracker, domain):
        logging.info('Initiating get group ...')
        return []


class ActionConfirmLiveWire(Action):
    def name(self):
        return 'action_confirm_livewire'

    def run(self, dispatcher, tracker, domain):
        logging.info('Confirming LiveWire action')


class ActionSendLiveWire(Action):
    def name(self):
        return 'action_send_livewire'

    def run(self, dispatcher, tracker, domain):
        logging.info('Sending LiveWire')