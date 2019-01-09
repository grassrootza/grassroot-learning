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

from platform_utils import *

from datetime import datetime
from difflib import SequenceMatcher
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import requests
import inspect
import logging
import json
import uuid
import os
import smtplib


logging.basicConfig(format="[NLULOGS] %(asctime)s [%(threadName)-12.12s] [%(levelname)-5.5s]  %(message)s", level=logging.DEBUG)

auth_token = os.getenv('TOKEN_X')
logging.info('Setting auth token: %s' % auth_token)

BASE_URL = os.getenv('PLATFORM_BASE_URL', 'https://staging.grassroot.org.za/v2/api')
DATETIME_URL = os.getenv('DATE_TIME_URL', 'https://61r14lq1l9.execute-api.eu-west-1.amazonaws.com/production')

TOKEN_PATH = '/whatsapp/user/token'
GROUP_PATH = '/group/fetch/minimal/filtered'
GROUP_NAME_PATH = '/group/fetch/minimal/specified/'
LIVEWIRE_PATH = '/livewire/create/'
ACTION_TODO_PATH = '/task/create/todo/action/'
VOLUNTEER_TODO_PATH = '/task/create/todo/volunteer/'
VALIDATION_TODO_PATH = '/task/create/todo/confirmation/'
INFO_TODO_PATH = '/task/create/todo/information/'
MEETING_PATH = '/task/create/meeting/'
VOTE_PATH = '/task/create/vote/'

parentType = 'GROUP'

permissionsMap = {
    'default': 'GROUP_PERMISSION_UPDATE_GROUP_DETAILS',
    'create_meeting': 'GROUP_PERMISSION_CREATE_GROUP_MEETING',
    'call_vote': 'GROUP_PERMISSION_CREATE_GROUP_VOTE'
}


class ActionGetGroup(Action):

    def name(self):
        return 'action_get_group'

    def run(self, dispatcher, tracker, domain):
        logging.info("Detected user: %s" % tracker.sender_id)
        logging.info("Greetings. Page value is currently set to %s" % tracker.get_slot("page"))
        current_action = tracker.get_slot("action")
        if current_action is None:
            current_action = "default"
        logging.info("Fetching groups, action = %s, required permission = %s" % (current_action, permissionsMap[current_action]))
        dispatcher.utter_button_message("Choose a group", get_group_menu_items(tracker.sender_id, tracker.get_slot("page"), permissionsMap[current_action]))
        return []


def get_group_menu_items(sender_id, page,required_permission = permissionsMap['default']):
    full_url = BASE_URL + GROUP_PATH
    logging.info('Getting group menu items, for sender ID : %s' % sender_id)
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
                error_alert(error_message, inspect.stack()[0][3])
    else:
        return request_token

            
def error_alert(error_message, function):
    try:
        message = MIMEMultipart()
        message['From'] = os.getenv('ALERT_EMAIL', 'grassrootnlu@gmail.com')
        message['To'] = os.getenv('DEVELOPER', '')
        message['Subject'] = "Token Trouble"
        message.attach(MIMEText(
                                error_message,
                                'plain'
                               ))
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(
                     message['From'],
                     os.getenv(
                               'ALERT_PWD',
                                   ''
                     ))
        text = message.as_string()
        server.sendmail(
                        message['From'],
                        message['To'], text
                       )
        server.quit()
        logging.debug('developer notified.')
        return ''
    except Exception as e:
        logging.error("platform_actions: error_alert:" 
                      " failed to notify developer about function %s() failure."
                      " Details %s" % (
                                       function,
                                       e
                                      ))
        return ''


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


class ActionIncrementPage(Action):

    def name(self):
        return 'action_increment_page'

    def run(self, dispatcher, tracker, domain):
        current_page = tracker.get_slot("page")
        if current_page == None:
            current_page = 0
        current_page += 1
        logging.debug("Now loading group page: %s" % current_page)
        return [SlotSet("page", current_page)] 


class ExtractValidateEntity(Action):

    def name(self):
        return 'extract_and_validate_entity'

    def run(self, dispatcher, tracker, domain):
        expected_entity = tracker.get_slot('requested_slot')
        expected_value = (tracker.latest_message)['text']
        # run_evaluation() where need be.
        logging.info("setting value '%s' for entity '%s'" % (expected_value, expected_entity))
        return [SlotSet(expected_entity, expected_value), SlotSet("requested_slot", None)]


class ActionAcquireMeetingDetails(FormAction):

    @staticmethod
    def required_slots(tracker: Tracker) -> List[Text]:
        """A list of required slots that the form has to fill"""

        return [
                "location",
                "subject",
                "datetime"
               ]

    def name(self):
        return 'action_create_meeting_routine'

    def submit(self, dispatcher, tracker, domain):
        group_name, member_count = get_group_name(tracker.get_slot("group_uid"), tracker.sender_id)
        responses = [
                     "You have chosen %s as your location." % tracker.get_slot("location"),
                     "You have chosen %s as your subject." % tracker.get_slot("subject"),
                     "You want this to happen *%s*." % human_readable_time(formalize(tracker.get_slot("datetime"))),
                     "You have chosen %s as your group which has %s members." % (group_name, member_count)
                    ]
        dispatcher.utter_message(' '.join(responses))
        return []


class ActionUtterMeetingStatus(Action):

    def name(self):
        return 'action_utter_meeting_status'

    def run(self, dispatcher, tracker, domain):
        group_name, member_count = get_group_name(tracker.get_slot("group_uid"), tracker.sender_id)
        responses = [
                     "You have chosen %s as your location." % tracker.get_slot("location"),
                     "You have chosen %s as your subject." % tracker.get_slot("subject"),
                     "You want this to happen *%s*." % human_readable_time(formalize(tracker.get_slot("datetime"))),
                     "You have chosen %s as your group which has %s members." % (group_name, member_count)
                    ]
        dispatcher.utter_message(' '.join(responses))
        return []


class ActionSendMeetingToServer(Action):

    def name(self):
        return 'action_send_meeting_to_server'

    def run(self, dispatcher, tracker, domain):
        groupUid = tracker.get_slot("group_uid")
        url = BASE_URL + MEETING_PATH + '%s/%s' % (parentType, groupUid)
        logging.info('Constructed url for create meeting: %s' % url)
        response = requests.post(url, headers={'Authorization': 'Bearer ' + get_token(tracker.sender_id)},
                                 params={
                                         'location': tracker.get_slot("location"),
                                         'dateTimeEpochMillis': epoch(formalize(tracker.get_slot("datetime"))),
                                         'subject': tracker.get_slot("subject"),
                                         })
        logging.info('Constructed url for create meeting: %s' % response.url)
        logging.info('Dispatched to platform, response: %s' % response.text)
        if response.status_code == 200:
            dispatcher.utter_message('We are making it happen for you. Thank you for using our service.')
        else:
            dispatcher.utter_message('I seem to have trouble processing your request. Please try again later.')
        return []


class ActionAcquireVoteDetails(FormAction):

    @staticmethod
    def required_slots(tracker: Tracker) -> List[Text]:
        """A list of required slots that the form has to fill"""

        return [
                "subject",
                "datetime"
               ]

    def name(self):
        return 'action_create_vote_routine'

    def submit(self, dispatcher, tracker, domain):
        return []


class ActionSetDefaultVoteOptions(Action):

    def name(self):
        return 'action_default_vote_options'

    def run(self, dispatcher, tracker, domain):
        return [SlotSet("vote_options", ["Yes", "No"])]


class ActionAddToVoteOptions(Action):
    
    def name(self):
        return 'action_add_to_vote_options'

    def run(self, dispatcher, tracker, domain):
        vote_option = (tracker.latest_message)['text']
        logging.debug("Found vote option: %s" % vote_option)
        dispatcher.utter_message("Vote option '%s' recieved." % vote_option)
        current_options = tracker.get_slot("vote_options")
        logging.debug("Found pre-existing options: %s" % current_options)
        if current_options == None:
            current_options = []
        current_options.append(vote_option)
        logging.debug("New vote options: %s" % current_options)
        return [SlotSet("vote_options", current_options)]        


class ActionUtterVoteStatus(Action):

    def name(self):
        return 'action_utter_vote_status'

    def run(self, dispatcher, tracker, domain):
        group_name, member_count = get_group_name(tracker.get_slot("group_uid"), tracker.sender_id)
        vote_options_list = tracker.get_slot("vote_options")
        vote_options = ''
        for i in range(len(vote_options_list)):
            if i != len(vote_options_list) - 1:
                vote_options = vote_options + str(vote_options_list[i]) + ', '
            else:
                vote_options = vote_options + 'and ' + str(vote_options_list[i])
        template = [
                    "You have chosen %s as your subject of your vote",
                    "and want the %s member(s) of %s to vote between %s",
                    "by *%s*."
                   ]
        vote_status = ' '.join(template) % (tracker.get_slot("subject"),
                                            member_count, group_name,
                                            vote_options, human_readable_time(formalize(tracker.get_slot("datetime"))))
        dispatcher.utter_message(vote_status)
        return []


class SendVoteToServer(Action):

    def name(self):
        return 'action_send_vote_to_server'

    def run(self, dispatcher, tracker, domain):
        groupUid = tracker.get_slot("group_uid")
        url = BASE_URL + VOTE_PATH + '%s/%s' % (parentType, groupUid)
        response = requests.post(url, headers={'Authorization': 'Bearer ' + get_token(tracker.sender_id)},
                                 params={
                                         'title': tracker.get_slot("subject"),
                                         'time': epoch(formalize(tracker.get_slot("datetime"))),
                                         'voteOptions': json.dumps(tracker.get_slot("vote_options")),
                                        })
        logging.info('Contructed url for create vote: %s' % response.url)
        logging.info('Received response from platform: %s' % response.text)
        if response.status_code == 200:
            dispatcher.utter_message('We are making it happen for you. Thank you for using our service.')
        else:
            dispatcher.utter_message('I seem to have trouble processing your request. Please try again later.')
        return []


class ActionAcquireInfoTodoDetails(FormAction):

    @staticmethod
    def required_slots(tracker: Tracker) -> List[Text]:
        """A list of required slots that the form has to fill"""

        return [
                "subject",
                "datetime",
                "response_tag"
               ]

    def name(self):
        return 'action_todo_info_routine'

    def submit(self, dispatcher, tracker, domain):
        group_name, member_count = get_group_name(tracker.get_slot("group_uid"), tracker.sender_id)
        responses = [
                     "You have chosen %s as the subject of this todo." % tracker.get_slot("subject"),
                     "You would like participant responses to be tagged with a '%s'" % tracker.get_slot("response_tag"),
                     "Participants may respond until *%s*" % human_readable_time(formalize(tracker.get_slot("datetime"))),
                     "You have chosen %s as your group which has %s members." % (group_name, member_count)
                    ]
        dispatcher.utter_message(' '.join(responses))
        return []


class SendInfoTodoToServer(Action):

    def name(self):
        return 'action_send_info_todo_to_server'

    def run(self, dispatcher, tracker, domain):
        groupUid = tracker.get_slot("group_uid")
        url = BASE_URL + INFO_TODO_PATH + '%s/%s' % (parentType, groupUid)
        response = requests.post(url, headers={'Authorization': 'Bearer ' + get_token(tracker.sender_id)},
                                 params={
                                         'subject': tracker.get_slot("subject"),
                                         'dueDateTime': epoch(formalize(tracker.get_slot("datetime"))),
                                         'responseTag': tracker.get_slot("response_tag")
                                        })
        logging.info('Contructed url for create information todo: %s' % response.url)
        logging.info('Received response from platform: %s' % response.text)
        if response.status_code == 200:
            dispatcher.utter_message('We are making it happen for you. Thank you for using our service.')
        else:
            dispatcher.utter_message('I seem to have trouble processing your request. Please try again later.')
        return []        


class ActionAcquireVolunteerDetails(FormAction):

    @staticmethod
    def required_slots(tracker: Tracker) -> List[Text]:
        """A list of required slots that the form has to fill"""

        return [
                "subject",
                "datetime"
               ]

    def name(self):
        return 'action_todo_volunteer_routine'

    def submit(self, dispatcher, tracker, domain):
        group_name, member_count = get_group_name(tracker.get_slot("group_uid"), tracker.sender_id)
        responses = [
                     "You have chosen %s the subject of this volunteer task." % tracker.get_slot("subject"),
                     "You want this to happen *%s*" % human_readable_time(formalize(tracker.get_slot("datetime"))),
                     "You have chosen %s as your group which has %s members." % (group_name, member_count)
                    ]
        dispatcher.utter_message(' '.join(responses))
        return []


class ActionSendVolunteerTodoToServer(Action):

    def name(self):
        return 'action_send_volunteer_todo_to_server'

    def run(self, dispatcher, tracker, domain):
        groupUid = tracker.get_slot("group_uid")
        url = BASE_URL + VOLUNTEER_TODO_PATH + '%s/%s' % (parentType, groupUid)
        response = requests.post(url, headers={'Authorization': 'Bearer ' + get_token(tracker.sender_id)},
                                 params={
                                         'subject': tracker.get_slot("subject"),
                                         'dueDateTime': epoch(formalize(tracker.get_slot("datetime")))
                                        })
        logging.info('Contructed url for create volunteer todo: %s' % response.url)
        logging.info('Received response from platform: %s' % response.text)
        if response.status_code == 200:
            dispatcher.utter_message('We are making it happen for you. Thank you for using our service.')
        else:
            dispatcher.utter_message('I seem to have trouble processing your request. Please try again later.')
        return []


class ActionAcquireValidationDetails(FormAction):

    @staticmethod
    def required_slots(tracker: Tracker) -> List[Text]:
        """A list of required slots that the form has to fill"""

        return [
                "subject",
                "datetime"
               ]

    def name(self):
        return 'action_todo_validation_routine'

    def submit(self, dispatcher, tracker, domain):
        group_name, member_count = get_group_name(tracker.get_slot("group_uid"), tracker.sender_id)
        responses = [
                     "You have chosen %s as subject of validation." % tracker.get_slot("subject"),
                     "You want everyone to have responded by *%s*." % human_readable_time(formalize(tracker.get_slot("datetime"))),
                     "You have chosen %s as your group which has %s members." % (group_name, member_count)
                    ]
        dispatcher.utter_message(' '.join(responses))
        return []


class ActionSendValidationToServer(Action):

    def name(self):
        return 'action_send_validation_todo_to_server'

    def run(self, dispatcher, tracker, domain):
        groupUid = tracker.get_slot("group_uid")
        url = BASE_URL + VALIDATION_TODO_PATH + '%s/%s' % (parentType, groupUid)
        response = requests.post(url, headers={'Authorization': 'Bearer ' + get_token(tracker.sender_id)},
                                 params={
                                         'subject': tracker.get_slot("subject"),
                                         'dueDateTime': epoch(formalize(tracker.get_slot("datetime")))
                                        })
        logging.info('Contructed url for create validation todo: %s' % response.url)
        logging.info('Received response from platform: %s' % response.text)
        if response.status_code == 200:
            dispatcher.utter_message('We are making it happen for you. Thank you for using our service.')
        else:
            dispatcher.utter_message('I seem to have trouble processing your request. Please try again later.')
        return []


class ActionAcquireActionTodoDetails(FormAction):

    @staticmethod
    def required_slots(tracker: Tracker) -> List[Text]:
        """A list of required slots that the form has to fill"""

        return [
                "subject",
                "datetime"
               ]

    def name(self):
        return 'action_todo_action_routine'

    def submit(self, dispatcher, tracker, domain):
        group_name, member_count = get_group_name(tracker.get_slot("group_uid"), tracker.sender_id)
        responses = [
                     "You have chosen %s as the subject for this action." % tracker.get_slot("subject"),
                     "You want this to happen *%s*" % human_readable_time(formalize(tracker.get_slot("datetime"))),
                     "You have chosen %s as your group which has %s members." % (group_name, member_count)
                   ]
        dispatcher.utter_message(' '.join(responses))
        return []


class ActionSendActionTodoToServer(Action):

    def name(self):
        return 'action_send_action_todo_to_server'

    def run(self, dispatcher, tracker, domain):
        groupUid = tracker.get_slot("group_uid")
        url = BASE_URL + ACTION_TODO_PATH + '%s/%s' % (parentType, groupUid)
        response = requests.post(url, headers={'Authorization': 'Bearer ' + get_token(tracker.sender_id)},
                                 params={
                                         'subject': tracker.get_slot("subject"),
                                         'dueDateTime': epoch(formalize(tracker.get_slot("datetime")))
                                         })
        logging.info('Contructed url for create action todo: %s' % response.url)
        logging.info('Received response from platform: %s' % response.text)
        if response.status_code == 200:
            dispatcher.utter_message('We are making it happen for you. Thank you for using our service.')
        else:
            dispatcher.utter_message('I seem to have trouble processing your request. Please try again later.')
        return []



class ActionAcquireLivewireDetails(FormAction):

    @staticmethod
    def required_slots(tracker: Tracker) -> List[Text]:
        """A list of required slots that the form has to fill"""

        return [
                "subject",
                "livewire_content",
                "contact_name",
                "contact_number"
               ]

    def name(self):
        return 'action_livewire_routine'

    def submit(self, dispatcher, tracker, domain):
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
        logging.debug("Media files now look like: %s" % tracker.get_slot("media_file_ids"))
        return [SlotSet("media_record_ids", current_media_files)]


class ActionUtterLivewireStatus(Action):

    def name(self):
        return 'action_utter_livewire_status'

    def run(self, dispatcher, tracker, domain):
        group_name, member_count = get_group_name(tracker.get_slot("group_uid"), tracker.sender_id)
        template = [
                     "You have chosen %s as the title.",
                     "You have entered '%s' as the content.",
                     "You have identified yourself as %s",
                     "and provided %s as your contact detail.",
                     "",
                     "You would like this to appear within the group %s which has %s member(s)."
                    ]
        media_files = tracker.get_slot("media_file_ids")
        if media_files != None:
            if len(media_files) > 1:
        	    template[4] = "You have also included %s media files." % len(media_files)
            else: 
                if len(media_files) == 1:
                    template[4] = "You have also included an image to this livewire."
        else:
        	template.pop(4)
        livewire_status = ' '.join(template) % (tracker.get_slot("subject"), snip(tracker.get_slot("livewire_content")),
                                                tracker.get_slot("contact_name"), tracker.get_slot("contact_number"),
                                                group_name, member_count)
        dispatcher.utter_message(livewire_status)
        return []


class ActionSendLivewireToServer(Action):

    def name(self):
        return 'action_send_livewire_to_server'

    def run(self, dispatcher, tracker, domain):
        headline = tracker.get_slot("subject")
        content = tracker.get_slot("livewire_content")
        contactName = tracker.get_slot("contact_name")
        contactNumber =  tracker.get_slot("contact_number")
        taskUid = tracker.get_slot("task_uid")
        livewire_type = 'INSTANT'
        addLocation = False
        mediaFileKeys = tracker.get_slot("media_file_ids")
        latitude = tracker.get_slot("latitude")
        longitude = tracker.get_slot("longitude")
        destUid = tracker.get_slot("destination_uid")
        groupUid = tracker.get_slot("group_uid")
        url = BASE_URL + LIVEWIRE_PATH + tracker.sender_id
        response = requests.post(url, headers={'Authorization': 'Bearer ' + get_token(tracker.sender_id)},
                                 params={
                                         'headline': headline,
                                         'description': content,
                                         'contactName': contactName,
                                         'contactNumber': contactNumber,
                                         'groupUid': groupUid,
                                         'taskUid': taskUid,
                                         'type': livewire_type,
                                         'addLocation': addLocation,
                                         'mediaFileKeys': mediaFileKeys,
                                         'latitude': latitude,
                                         'longitude': longitude,
                                         'destUid': destUid
                                         })
        logging.info('Contructed livewire url: %s' % response.url)
        logging.info('Received response from platform: %s' % response.text)
        if response.status_code == 200:
            dispatcher.utter_message('We are making it happen for you. Thank you for using our service.')
        else:
            dispatcher.utter_message('I seem to have trouble processing your request. Please try again later.')
        return []


class ActionRerouteMessage(Action):

    def name(self):
        return 'action_reroute_to_new_domain'

    def run(self, dispatcher, tracker, domain):
        dispatcher.utter_message('DUM_SPIRO_SPERO')
        return []


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
        error_alert(e, inspect.stack()[0][3])
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
        return formalized_datetime


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