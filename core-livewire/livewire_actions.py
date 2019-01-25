import logging

from typing import Dict, Text, Any, List, Union

from rasa_core_sdk import Action
from rasa_core_sdk import Tracker
from rasa_core_sdk.executor import CollectingDispatcher
from rasa_core_sdk.forms import FormAction, REQUESTED_SLOT
from rasa_core_sdk.events import SlotSet
from rasa_core_sdk import ActionExecutionRejection

from phonenumbers.phonenumberutil import number_type
from phonenumbers import carrier
from datetime import datetime
import phonenumbers
import requests
# import rollbar
import json
import os

auth_token = os.getenv('TOKEN_X')
logging.info('Setting auth token: %s' % auth_token)

BASE_URL = os.getenv('PLATFORM_BASE_URL', 'https://staging.grassroot.org.za/v2/api')
DATETIME_URL = os.getenv('DATE_TIME_URL', 'https://61r14lq1l9.execute-api.eu-west-1.amazonaws.com/production')

TOKEN_PATH = '/whatsapp/user/token'
GROUP_PATH = '/group/fetch/minimal/filtered'
GROUP_LIST_PATH = '/group/fetch/list'
GROUP_NAME_PATH = '/group/fetch/minimal/specified/'
LIVEWIRE_PATH = '/livewire/create/'
MEETING_PATH = '/task/create/meeting/'

parentType = 'GROUP'

permissionsMap = {
    'default': 'GROUP_PERMISSION_UPDATE_GROUP_DETAILS'
}

##########################################
#                LIVEWIRE                #
##########################################

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

    def validate(self,
                 dispatcher: CollectingDispatcher,
                 tracker: Tracker,
                 domain: Dict[Text, Any]) -> List[Dict]:
        """Validate extracted requested slot
            else reject the execution of the form action
        """
        # extract other slots that were not requested
        # but set by corresponding entity
        slot_values = self.extract_other_slots(dispatcher, tracker, domain)

        # extract requested slot
        slot_to_fill = tracker.get_slot(REQUESTED_SLOT)
        if slot_to_fill:
            slot_values.update(self.extract_requested_slot(dispatcher,
                                                           tracker, domain))
            if not slot_values:
                # reject form action execution
                # if some slot was requested but nothing was extracted
                # it will allow other policies to predict another action
                raise ActionExecutionRejection(self.name(),
                                               "Failed to validate slot {0} "
                                               "with action {1}"
                                               "".format(slot_to_fill,
                                                         self.name()))

        # we'll check when validation failed in order
        # to add appropriate utterances
        for slot, value in slot_values.items():
            logging.info("Now validating: %s: %s" % (slot, value))
            if slot == 'contact_number':
                try:
                    is_number = carrier._is_mobile(number_type(phonenumbers.parse(value, "ZA")))
                except phonenumbers.phonenumberutil.NumberParseException as e:
                    logging.warn(e)
                    is_number = False
                if is_number == False:
                    dispatcher.utter_template('utter_invalid_number', tracker)
                    # validation failed, set slot to None
                    slot_values[slot] = None

        # validation succeed, set the slots values to the extracted values
        return [SlotSet(slot, value) for slot, value in slot_values.items()]
    
    def submit(self, dispatcher, tracker, domain):
        logging.critical("Completed form")
        return []


class ActionConfirmLiveWire(Action):
    def name(self):
        return 'action_confirm_livewire'

    def run(self, dispatcher, tracker, domain):
        logging.info('Confirming LiveWire action')
        group_name, member_count = get_group_name(tracker.get_slot("group_uid"), get_sender_id(tracker.sender_id))
        template = [
                     "You have chosen %s as the title.",
                     "You have entered '%s' as the content.",
                     "You have chosen %s as the livewire's contact name",
                     "and provided %s as the contact number.",
                     "",
                     "You would like this to appear within the group %s which has %s member(s)."
                     "Is this correct?"
                    ]
        media_files = tracker.get_slot("media_record_ids")
        if media_files != None:
            if len(media_files) > 1:
        	    template[4] = "You have also included %s media files." % len(media_files)
            else: 
                if len(media_files) == 1:
                    template[4] = "You have also included an image to this livewire."
        else:
        	template.pop(4)
        livewire_status = ' '.join(template) % (tracker.get_slot("subject"), snip(tracker.get_slot("content")),
                                                get_contact_name(tracker.get_slot("contact_name")),
                                                tracker.get_slot("contact_number"),
                                                group_name, member_count)
        dispatcher.utter_message(livewire_status)
        return []


class ActionSendLiveWire(Action):
    def name(self):
        return 'action_send_livewire'

    def run(self, dispatcher, tracker, domain):
        logging.info('Sending LiveWire')
        headline = tracker.get_slot("subject")
        content = tracker.get_slot("content")
        contact_name = tracker.get_slot("contact_name")
        if contact_name.strip().lower() == 'me':
            contact_name = None
        contact_number =  tracker.get_slot("contact_number")
        task_uid = tracker.get_slot("task_uid")
        latitude = tracker.get_slot("latitude")
        longitude = tracker.get_slot("longitude")
        livewire_type = 'INSTANT'
        if (latitude != None) and (longitude != None):
            add_location = True
        else:
            add_location = False
        media_file_keys = tracker.get_slot("media_file_ids")
        dest_uid = tracker.get_slot("destination_uid")
        group_uid = tracker.get_slot("group_uid")
        url = BASE_URL + LIVEWIRE_PATH + get_sender_id(tracker.sender_id)
        response = requests.post(url, headers={'Authorization': 'Bearer ' + get_token(get_sender_id(tracker.sender_id))},
                                 params={
                                         'headline': headline,
                                         'description': content,
                                         'contactName': contact_name,
                                         'contactNumber': contact_number,
                                         'groupUid': group_uid,
                                         'taskUid': task_uid,
                                         'type': livewire_type,
                                         'addLocation': add_location,
                                         'mediaFileKeys': media_file_keys,
                                         'latitude': latitude,
                                         'longitude': longitude,
                                         'destUid': dest_uid
                                         })
        logging.info('Contructed livewire url: %s' % response.url)
        logging.info('Received response from platform: %s' % response.text)
        if response.status_code == 200:
            dispatcher.utter_message('We are making it happen for you. Thank you for using our service.')
        else:
            dispatcher.utter_message('I seem to have trouble processing your request. Please try again later.')
        return []


class ActionSaveMediaFile(Action):

    def name(self):
        return 'action_save_media_file_id'

    def run(self, dispatcher, tracker, domain):
        media_file = tracker.get_slot("media_record_id")
        logging.debug("Recieved media file: %s" % media_file)
        current_media_files = tracker.get_slot("media_record_ids")
        logging.debug("Current media files are: %s" % current_media_files)
        if current_media_files == None:
            current_media_files = []
        current_media_files.append(media_file)
        logging.debug("Media files now look like: %s" % current_media_files)
        return [SlotSet("media_record_ids", current_media_files)]


##########################################
#                MEETING                 #
##########################################


class MeetingBasicFormAction(FormAction):
    """Form action to fill out basic details for a Meeting action"""

    def name(self):
        # type: () -> Text
        return "meeting_basic_form"
    
    @staticmethod
    def required_slots(tracker):
        # type: () -> List[Text]
        logging.info("Returning required slot set")
        return ["subject", "meeting_location", "meeting_time"]

    def slot_mappings(self):
        return {"subject": self.from_text(), "meeting_location": self.from_text(), "meeting_time": self.from_text()}

    def validate(self,
                 dispatcher: CollectingDispatcher,
                 tracker: Tracker,
                 domain: Dict[Text, Any]) -> List[Dict]:
        """Validate extracted requested slot
            else reject the execution of the form action
        """
        # extract other slots that were not requested
        # but set by corresponding entity
        slot_values = self.extract_other_slots(dispatcher, tracker, domain)

        # extract requested slot
        slot_to_fill = tracker.get_slot(REQUESTED_SLOT)
        if slot_to_fill:
            slot_values.update(self.extract_requested_slot(dispatcher,
                                                           tracker, domain))
            if not slot_values:
                # reject form action execution
                # if some slot was requested but nothing was extracted
                # it will allow other policies to predict another action
                raise ActionExecutionRejection(self.name(),
                                               "Failed to validate slot {0} "
                                               "with action {1}"
                                               "".format(slot_to_fill,
                                                         self.name()))

        # we'll check when validation failed in order
        # to add appropriate utterances
        for slot, value in slot_values.items():
            logging.info("Now validating: %s: %s" % (slot, value))
            if slot == 'meeting_time':
                try:
                    return_value = epoch(formalize(value))
                except Exception as e:
                    logging.warn(e)
                    return_value = b'ERROR_PARSING'
                    # rollbar.report_exc_info()
                logging.info('Got this back during meeting_time validation: %s' % return_value)
                if return_value == b'ERROR_PARSING':
                    dispatcher.utter_template('utter_invalid_time', tracker)
                    # validation failed, set slot to None
                    slot_values[slot] = None

        # validation succeed, set the slots values to the extracted values
        return [SlotSet(slot, value) for slot, value in slot_values.items()]

    def submit(self, dispatcher, tracker, domain):
        logging.critical("Completed form")
        dispatcher.utter_template('utter_which_meeting_group', tracker)
        return []


class ActionConfirmMeeting(Action):

    def name(self):
        return 'action_confirm_meeting'

    def run(self, dispatcher, tracker, domain):
        group_name, member_count = get_group_name(tracker.get_slot("group_uid"), get_sender_id(tracker.sender_id))
        responses = [
                     "You have chosen %s as your location." % tracker.get_slot("meeting_location"),
                     "You have chosen %s as your subject." % tracker.get_slot("subject"),
                     "You would like to meet on *%s*." % human_readable_time(formalize(tracker.get_slot("meeting_time"))),
                     "You have chosen %s as your group which has %s members." % (group_name, member_count),
                     "Is this correct?"
                    ]
        dispatcher.utter_message(' '.join(responses))
        return []


class ActionSendMeeting(Action):

    def name(self):
        return 'action_send_meeting'

    def run(self, dispatcher, tracker, domain):
        groupUid = tracker.get_slot("group_uid")
        url = BASE_URL + MEETING_PATH + '%s/%s' % (parentType, groupUid)
        logging.info('Constructed url for create meeting: %s' % url)
        response = requests.post(url, headers={'Authorization': 'Bearer ' + get_token('auto_16475')},
                                 params={
                                         'location': tracker.get_slot("meeting_location"),
                                         'dateTimeEpochMillis': epoch(formalize(tracker.get_slot("meeting_time"))),
                                         'subject': tracker.get_slot("subject"),
                                         })
        logging.info('Constructed url for create meeting: %s' % response.url)
        logging.info('Dispatched to platform, response: %s' % response.text)
        if response.status_code == 200:
            dispatcher.utter_message('We are making it happen for you. Thank you for using our service.')
        else:
            dispatcher.utter_message('I seem to have trouble processing your request. Please try again later.')
        return []


##########################################
#               UTILITIES                #
##########################################

class ActionGetGroup(Action):
    def name(self):
        return 'action_get_group'

    def run(self, dispatcher, tracker, domain):
        logging.info('Initiating get group ...')
        logging.info("Greetings. Page value is currently set to %s" % tracker.get_slot("page"))
        current_action = tracker.get_slot("action")
        if current_action is None:
            current_action = "default"
        logging.info("Fetching groups, action = %s, required permission = %s" % (current_action, permissionsMap[current_action]))
        dispatcher.utter_button_message("Choose one (use a number or the group name): ",
                                        get_group_menu_items(get_sender_id(tracker.sender_id),
                                                             tracker.get_slot("page"),
                                                             permissionsMap[current_action]))
        return []


def get_group_name(groupUid, sender_id):
    response = requests.get(BASE_URL + GROUP_NAME_PATH + groupUid,
                            headers={'Authorization': 'Bearer ' + get_token(sender_id)})
    logging.debug('Got this back from group name retrieval: %s' % response.content)
    if response.ok:
        data = json.loads(response.text)
        group_name = data['name']
        member_count = data['memberCount']
        return group_name, member_count
    return '', ''


def get_group_menu_items(sender_id, page,required_permission = permissionsMap['default']):
    full_url = BASE_URL + GROUP_PATH
    logging.info('Getting group menu items, for sender ID : %s' % sender_id)
    # get paginated groups
    request = requests.get(full_url, headers={'Authorization': 'Bearer ' + get_token(sender_id)},
                                                  params={
                                                          'pageNumber': page,
                                                          'requiredPermission': required_permission
                                                         }
                          )
    raw_json = json.loads(request.text)
    logging.info('Sent group-fetch url: %s' % request.url)
    logging.info("Content of response, raw: %s" % raw_json)
    try:
        page_content = raw_json['content']
        logging.info('Page content: %s' % page_content)
        menu_items = []
        logging.info('How many groups do we have? %d' % len(page_content))
        for group in range(len(page_content)):
            menu_items.append({
                               'title': page_content[group]['name'],
                               'payload': 'group_uid::' + page_content[group]['groupUid']
                              })
        if raw_json['last'] == False:
            menu_items.append({
                               'title': 'Load more groups',
                               'payload': '/next_page'
                              })
    except KeyError as e:
        logging.error('Error: platform_actions.py: get_group_menu_items(): %s' % str(e))
        # rollbar.report_exc_info()
        return []
    return menu_items


def get_token(sender_id):
    request_token = requests.post(BASE_URL + TOKEN_PATH, headers={'Authorization': 'Bearer ' + auth_token},\
                                    params={'userId': '%s' % sender_id}).text
    logging.debug('request_token: %s' % request_token)
    if request_token.startswith('{'):
        request_token = json.loads(request_token)
        logging.debug("request token successfully converted to %s" % type(request_token))
        if isinstance(request_token, dict):
            if request_token['status'] == 403:
                request_token['file_path'] = os.path.realpath(__file__)
                error_message = "Greetings.\n\nplatform_actions.py has failed to retrieve auth token.\n Details: %s\
                        \n\nThis may be due to an expired token.\n\nRegards\n\nCore-Actions" % request_token
                # error_alert(error_message, inspect.stack()[0][3])
                logging.error("Error during token retrieval.")
    else:
        return request_token


def get_sender_id(tracker_value):
    logging.info("Current sender id is %s " % tracker_value)
    if tracker_value == 'default':
        logging.warn('Changing tracker value to privileged user.')
        return 'auto_16475'
    else:
        return tracker_value


def snip(text):
    """This function shortens large text data and adds ellipsis if 
       text exceeds 20 characters. Typcially used for previewing livewire content.

        params:
             text: type -> string;
    """

    if text != None and len(text) > 20:
        return text[:20] + "..."
    else:
        return text


def formalize(datetime_string):
    """This function converts arbitrary date-strings to a standard format.

        params:
            date_string: arbitrary date string (e.g., 'tomorrow at 3', 'next year on the first monday of May at 4pm')
    """

    try:
        response = requests.get(DATETIME_URL, params={
                                                      'date_string': datetime_string
                                                     })
        logging.info('constructed datetime url: %s' % response.url)
        logging.debug('datetime engine returned: %s' % response.content)
        return response.content.decode('ascii')
    except Exception as e:
        logging.error('platform_actions: formalize: %s' % e)
        # rollbar.report_exc_info()
        return datetime_string


def epoch(formalized_datetime):
    """This function converts the output of formalize() to epoch milisecond.

        params:
            formalized_datetime: date-string of format YYYY-mm-ddTHH:MM
    """

    utc_time = datetime.strptime(formalized_datetime, '%Y-%m-%dT%H:%M')
    return int((utc_time - datetime(1970, 1, 1)).total_seconds() * 1000)


def human_readable_time(formalized_datetime):
    """This function translates the output of formalize() to a more humanly
       explicit format.

        params:
            formalized_datetime: date-string of format YYYY-mm-ddTHH:MM
    """

    try:
        datetime_obj = datetime.strptime(formalized_datetime, '%Y-%m-%dT%H:%M')
        human_readable_time = datetime.strftime(datetime_obj, '%b %d, %Y at %H:%M')
        return human_readable_time
    except Exception as e:
        logging.error('platform_actions: human_readable_time: %s ' % e)
        # rollbar.report_exc_info()
        return formalized_datetime


def get_contact_name(user_input):
    if user_input.strip().lower() == 'me':
        return 'your account name'
    else:
        return user_input