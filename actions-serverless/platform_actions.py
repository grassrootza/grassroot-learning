from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from rasa_core_sdk import Action
from rasa_core_sdk.forms import FreeTextFormField, FormAction
from rasa_core_sdk.events import SlotSet
from datetime import datetime
from difflib import SequenceMatcher

import requests
import logging
import json
import uuid
import os

logging.basicConfig(format="[NLULOGS] %(asctime)s [%(threadName)-12.12s] [%(levelname)-5.5s]  %(message)s", level=logging.DEBUG)

auth_token = os.getenv('TOKEN_X')

BASE_URL = os.getenv('BASE_URL', 'https://staging.grassroot.org.za/v2/api')
DATETIME_URL = os.getenv('DATE_TIME_URL', 'http://learning.grassroot.cloud')

TOKEN_PATH = '/whatsapp/user/token'
GROUP_PATH = '/group/fetch/minimal/filtered'
MEETING_PATH = 

parentType = 'GROUP'
session_vote_options = {'user_id': []}
session_media_files = {'user_id': []}

permissionsMap = {
    'default': 'GROUP_PERMISSION_UPDATE_GROUP_DETAILS',
    'create_meeting': 'GROUP_PERMISSION_CREATE_GROUP_MEETING',
    'call_vote': 'GROUP_PERMISSION_CREATE_GROUP_VOTE'
}

class ActionGetGroup(Action):

    def name(self):
        return 'action_get_group'

    def run(self, dispatcher, tracker, domain):
        current_action = tracker.get_slot("action")
        if current_action is None: 
            current_action = "default"
        logging.info("Fetching groups, action = %s, required permission = %s" % (current_action, permissionsMap[current_action]))
        dispatcher.utter_button_message("Choose a group", get_group_menu_items(tracker.sender_id, permissionsMap[current_action]))
        return []


def get_group_menu_items(sender_id, required_permission = permissionsMap['default']):
    full_url = BASE_URL + GROUP_PATH + "?requiredPermission=" + required_permission 
    raw_json = json.loads(requests.get(full_url, headers={'Authorization': 'Bearer ' + get_token(sender_id)}).text)
    page_content = raw_json['content']
    logging.info('Page content: %s' % page_content)
    menu_items = []
    try:
        logging.info('How many groups do we have? %d' % len(page_content))
        for group in range(len(page_content)):
            menu_items.append({'title': page_content[group]['name'], 'payload': 'group::' + page_content[group]['groupUid']})
    except KeyError as e:
        logging.error('GAAAH! The child of Fort Knox sprang a leak and is dying. platform_actions.py: get_group_menu_items(): %s' % str(e))
        return []
    return menu_items


class ActionSaveGroup(Action):

    def name(self):
        return 'action_utter_save_selected_group'

    def run(self, dispatcher, tracker, domain):
        group = (tracker.latest_message)['text']
        return [SlotSet("group", group)]


class ActionCreateMeetingRoutine(FormAction):

    RANDOMIZE = False

    @staticmethod
    def required_fields():
        return [
            FreeTextFormField("location"),
            FreeTextFormField("subject"),
            FreeTextFormField("description"),
            FreeTextFormField("datetime")
        ]

    def name(self):
        return 'action_create_meeting_routine'

    def submit(self, dispatcher, tracker, domain):
        responses = [
                     "You have chosen %s as your location." % tracker.get_slot("location"),
                     "You have chosen %s as your subject." % tracker.get_slot("subject"),
                     "You have described this meeting as %s." % tracker.get_slot("description"),
                     "You want this to happen %s." % tracker.get_slot("datetime"),
                     "You have chosen %s as your group." % tracker.get_slot("group")
                    ]
        dispatcher.utter_message(' '.join(responses))
        return []


class ActionCreateVoteRoutine(FormAction):

    RANDOMIZE = False

    @staticmethod
    def required_fields():
        return [
            FreeTextFormField("subject"),
            FreeTextFormField("description"),
            FreeTextFormField("datetime")
        ]
        # voteOptions are acquired through a different Action

    def name(self):
        return 'action_create_vote_routine'

    def submit(self, dispatcher, tracker, domain):
        responses = [
                     "You have chosen %s as your subject of your vote." % tracker.get_slot("subject"),
                     "You have described this vote as %s" % tracker.get_slot("description"),
                     "You want this to happen %s" % tracker.get_slot("datetime"),
                     "You have chosen %s as your group." % tracker.get_slot("group")
                    ]
        dispatcher.utter_message(' '.join(responses))
        return []


class ActionTodoInfoRoutine(FormAction):

    RANDOMIZE = False

    @staticmethod
    def required_fields():
        return [
            FreeTextFormField("subject"),
            FreeTextFormField("description"),
            FreeTextFormField("response_tag"),
            FreeTextFormField("datetime")
        ]

    def name(self):
        return 'action_todo_info_routine'

    def submit(self, dispatcher, tracker, domain):
        responses = [
                     "You have chosen %s as the subject of this todo." % tracker.get_slot("subject"),
                     "You have described this todo as %s" % tracker.get_slot("description"),
                     "You would like participant responses to be tagged with a '%s'" % tracker.get_slot("response_tag"),
                     "Participants may respond until %s" % tracker.get_slot("datetime"),
                     "You have chosen %s as your group." % tracker.get_slot("group")
                    ]
        dispatcher.utter_message(' '.join(responses))
        return []


class ActionTodoVolunteerRoutine(FormAction):

    RANDOMIZE = False

    @staticmethod
    def required_fields():
        return [
            FreeTextFormField("subject"),
            FreeTextFormField("description"),
            FreeTextFormField("datetime")
        ]

    def name(self):
        return 'action_todo_volunteer_routine'

    def submit(self, dispatcher, tracker, domain):
        responses = [
                     "You have chosen %s the subject of this volunteer task." % tracker.get_slot("subject"),
                     "You have described this volunteer task as %s" % tracker.get_slot("description"),
                     "You want this to happen %s" % tracker.get_slot("datetime"),
                     "You have chosen %s as your group." % tracker.get_slot("group")
                    ]
        dispatcher.utter_message(' '.join(responses))
        return []


class ActionTodoValidationRoutine(FormAction):

    RANDOMIZE = False

    @staticmethod
    def required_fields():
        return [
            FreeTextFormField("subject"),
            FreeTextFormField("description"),
            FreeTextFormField("datetime")
        ]

    def name(self):
        return 'action_todo_validation_routine'

    def submit(self, dispatcher, tracker, domain):
        responses = [
                     "You have chosen %s as subject of validation." % tracker.get_slot("subject"),
                     "You have described this validation as %s." % tracker.get_slot("description"),
                     "You want everyone to have responded by %s." % tracker.get_slot("datetime"),
                     "You have chosen %s as your group." % tracker.get_slot("group")
                    ]
        dispatcher.utter_message(' '.join(responses))
        return []


class ActionTodoActionRoutine(FormAction):

    RANDOMIZE = False

    @staticmethod
    def required_fields():
        return [
            FreeTextFormField("subject"),
            FreeTextFormField("description"),
            FreeTextFormField("datetime")
        ]

    def name(self):
        return 'action_todo_action_routine'

    def submit(self, dispatcher, tracker, domain):
        responses = [
                    "You have chosen %s as the subject for this action." % tracker.get_slot("subject"),
                    "You have described this action as %s" % tracker.get_slot("description"),
                    "You want this to happen %s" % tracker.get_slot("datetime"),
                     "You have chosen %s as your group." % tracker.get_slot("group")
                   ]
        dispatcher.utter_message(' '.join(responses))
        return []


class ActionLivewireRoutine(FormAction):

    RANDOMIZE = False

    @staticmethod
    def required_fields():
        return [
            FreeTextFormField("subject"),
            FreeTextFormField("description"),
            FreeTextFormField("contact_name"),
            FreeTextFormField("contact_number")
        ]

    def name(self):
        return 'action_livewire_routine'

    def submit(self, dispatcher, tracker, domain):
        responses = [
                     "You have chosen %s as the title." % tracker.get_slot("subject"),
                     "You have entered '%s' as the content." % tracker.get_slot("description"),
                     "You have identified yourself as %s" % tracker.get_slot("contact_name"),
                     "and provided %s as your contact detail." % tracker.get_slot("contact_number"),
                     # "you have also included %s media file." % traker.get_slot("session_media_keys"),
                     "You would like this to appear within the group %s." % tracker.get_slot("group"),
                    ]
        dispatcher.utter_message(' '.join(responses))
        return []


class ActionGetVoteOption(Action):

    def name(self):
        return 'action_get_vote_option'

    def run(self, dispatcher, tracker, domain):
        dispatcher.utter_message("What are your vote options?")
        return []


class ActionStoreVoteOption(Action):

    def name(self):
        return 'action_store_vote_option'

    def run(self, dispatcher, tracker, domain):
        vote_option = (tracker.latest_message)['text']

        user_id = tracker.sender_id
        if user_id in list(session_vote_options):
            session_vote_options[user_id].append(vote_option)
        else:
            session_vote_options[user_id] = [vote_option]
        return []


class CreateMeetingComplete(Action):

    def name(self):
        return 'action_create_meeting_complete'

    def run(self, dispatcher, tracker, domain):
        groupUid = get_group_uid(tracker.get_slot("group"), tracker.sender_id)
        if groupUid == '':
            dispatcher.utter_message('Could not find %s within registered groups.' % tracker.get_slot("group"))
            return []
        meeting_path = '/task/create/meeting/%s/%s' % (parentType, groupUid)
        url = BASE_URL + meeting_path
        logging.info('Constructed url for create meeting: %s' % url)
        response = requests.post(url, headers={'Authorization': 'Bearer ' + get_token(tracker.sender_id)},
                                 params={
                                         'location': tracker.get_slot("location"),
                                         'dateTimeEpochMillis': epoch(formalize(tracker.get_slot("datetime"))),
                                         'subject': tracker.get_slot("subject"),
                                         'description': tracker.get_slot("description")
                                         }
                                )
        dispatcher.utter_message('We are making it happen for you. Thank you for using our service.')
        logging.info('Constructed url for create meeting: %s' % response.url)
        logging.info('Dispatched to platform, response: %s' % response)
        clean_session(tracker.sender_id)
        return []


class CreateVoteComplete(Action):

    def name(self):
        return 'action_create_vote_complete'

    def run(self, dispatcher, tracker, domain):
        groupUid = get_group_uid(tracker.get_slot("group"), tracker.sender_id)
        if groupUid == '':
            dispatcher.utter_message('Could not find %s within registered groups.' % tracker.get_slot("group"))
            return []
        vote_path = '/task/create/vote/%s/%s' % (parentType, groupUid)
        url = BASE_URL + vote_path
        response = requests.post(url, headers={'Authorization': 'Bearer ' + get_token(tracker.sender_id)},
                                 params={
                                         'title': tracker.get_slot("subject"),
                                         'time': epoch(formalize(tracker.get_slot("datetime"))),
                                         'voteOptions': get_session_data(tracker.sender_id, session_vote_options),
                                         'description': tracker.get_slot("description")
                                         })
        dispatcher.utter_message('We are making it happen for you. Thank you for using our service.')
        logging.info('Contructed url for create vote: %s' % response.url)
        logging.info('Received response from platform: %s' % response)
        clean_session(tracker.sender_id)
        return []


class CreateVolunteerTodoUrl(Action):

    def name(self):
        return 'action_create_volunteer_todo_complete'

    def run(self, dispatcher, tracker, domain):
        groupUid = get_group_uid(tracker.get_slot("group"), tracker.sender_id)
        if groupUid == '':
            dispatcher.utter_message('Could not find %s within registered groups.' % tracker.get_slot("group"))
            return []
        todo_path = '/v2/api/task/create/todo/volunteer/%s/%s' % (parentType, groupUid)
        url = BASE_URL + todo_path
        response = requests.post(url, headers={'Authorization': 'Bearer ' + get_token(tracker.sender_id)},
                                 params={
                                         'subject': tracker.get_slot("subject"),
                                         'dueDateTime': epoch(formalize(tracker.get_slot("datetime")))
                                         })
        dispatcher.utter_message('We are making it happen for you. Thank you for using our service.')
        logging.info('Contructed url for create volunteer todo: %s' % response.url)
        logging.info('Received response from platform: %s' % response)
        return []


class CreateValidationTodoUrl(Action):

    def name(self):
        return 'create_validation_todo_complete'

    def run(self, dispatcher, tracker, domain):
        groupUid = get_group_uid(tracker.get_slot("group"), tracker.sender_id)
        if groupUid == '':
            dispatcher.utter_message('Could not find %s within registered groups.' % tracker.get_slot("group"))
            return []
        todo_path = '/v2/api/task/create/todo/confirmation/%s/%s' % (parentType, groupUid)
        response = requests.post(url, headers={'Authorization': 'Bearer ' + get_token(tracker.sender_id)},
                                 params={
                                         'subject': tracker.get_slot("subject"),
                                         'dueDateTime': epoch(formalize(tracker.get_slot("datetime")))
                                         })
        dispatcher.utter_message('We are making it happen for you. Thank you for using our service.')
        logging.info('Contructed url for create validation todo: %s' % response.url)
        logging.info('Received response from platform: %s' % response)
        return []


class CreateInfoTodoUrl(Action):

    def name(self):
        return 'action_create_info_todo_complete'

    def run(self, dispatcher, tracker, domain):
        groupUid = get_group_uid(tracker.get_slot("group"), tracker.sender_id)
        if groupUid == '':
            dispatcher.utter_message('Could not find %s within registered groups.' % tracker.get_slot("group"))
            return []
        todo_path = '/v2/api/task/create/todo/information/%s/%s' % (parentType, groupUid)
        response = requests.post(url, headers={'Authorization': 'Bearer ' + get_token(tracker.sender_id)},
                                 params={
                                         'subject': tracker.get_slot("subject"),
                                         'dueDateTime': epoch(formalize(tracker.get_slot("datetime"))),
                                         'responseTag': tracker.get_slot("response_tag")
                                         })
        dispatcher.utter_message('We are making it happen for you. Thank you for using our service.')
        logging.info('Contructed url for create information todo: %s' % response.url)
        logging.info('Received response from platform: %s' % response)
        return []


class CreateActionTodoUrl(Action):

    def name(self):
        return 'action_create_todo_action_complete'

    def run(self, dispatcher, tracker, domain):
        groupUid = get_group_uid(tracker.get_slot("group"), tracker.sender_id)
        if groupUid == '':
            dispatcher.utter_message('Could not find %s within registered groups.' % tracker.get_slot("group"))
            return []
        todo_path = '/v2/api/task/create/todo/action/%s/%s' % (parentType, groupUid)
        response = requests.post(url, headers={'Authorization': 'Bearer ' + get_token(tracker.sender_id)},
                                 params={
                                         'subject': tracker.get_slot("subject"),
                                         'dueDateTime': epoch(formalize(tracker.get_slot("datetime")))
                                         })
        dispatcher.utter_message('We are making it happen for you. Thank you for using our service.')
        logging.info('Contructed url for create action todo: %s' % response.url)
        logging.info('Received response from platform: %s' % response)
        return []


class CreateLivewireUrl(Action):

    def name(self):
        return 'action_create_livewire_complete'

    def run(self, dispatcher, tracker, domain):
        headline = tracker.get_slot("subject")
        description = tracker.get_slot("description")
        contactName = tracker.get_slot("contact_name")
        contactNumber =  tracker.get_slot("contact_number")
        groupUid = get_group_uid(tracker.get_slot("group"), tracker.sender_id)
        taskUid = tracker.get_slot("task_uid")
        livewire_type = 'INSTANT'
        addLocation = False
        mediaFileKeys = get_session_data(tracker.sender_id, session_media_files)
        latitude = tracker.get_slot("latitude")
        longitude = tracker.get_slot("longitude")
        destUid = tracker.get_slot("destination_uid")
        groupUid = get_group_uid(tracker.get_slot("group"), tracker.sender_id)
        if groupUid == '':
            dispatcher.utter_message('Could not find %s within registered groups.' % tracker.get_slot("group"))
            return []
        livewire_path = '/v2/api/livewire/create/%s' % tracker.sender_id
        url = BASE_URL + livewire_path
        response = requests.post(url, headers={'Authorization': 'Bearer ' + get_token(tracker.sender_id)},
                                 params={
                                         'headline': tracker.get_slot("subject"),
                                         'description': description,
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
        dispatcher.utter_message('We are making it happen for you. Thank you for using our service.')
        logging.info('Contructed livewire url: %s' % response.url)
        logging.info('Received response from platform: %s' % response)
        clean_session(tracker.sender_id)
        return []


class ActionSaveMediaFile(Action):

    def name(self):
        return 'action_save_media_file'

    def run(self, dispatcher, tracker, domain):
        media_file = tracker.get_slot("media_file_id")
        if media_file != None:
            if tracker.sender_id in list(session_media_files):
                session_media_files[tracker.sender_id].append(media_file)
                return [SlotSet('media_file_keys', session_media_files[tracker.sender_id])]
            else:
                session_media_files[tracker.sender_id] = [media_file]
                return [SlotSet('media_file_keys', session_media_files[tracker.sender_id])]
        return []


def formalize(datetime_str):
    response = requests.get('%s/datetime?date_string=%s' % (DATETIME_URL, datetime_str)).content.decode('ascii')
    logging.debug('datetime engine returned: %s' % response)
    return response


def epoch(formalized_datetime):
    try:
        utc_time = datetime.strptime(formalized_datetime, '%Y-%m-%dT%H:%M')
        return int((utc_time - datetime(1970, 1, 1)).total_seconds() * 1000)
    except ValueError as e:
        logging.debug(e)
        utc_time = datetime.strptime(formalized_datetime, '%d-%m-%YT%H:%M')
        return int((utc_time - datetime(1970, 1, 1)).total_seconds() * 1000)


def get_token(sender_id):
    request_token = requests.post(BASE_URL + TOKEN_PATH, headers={'Authorization': 'Bearer ' + auth_token},\
                                  params={'userId': '%s' % sender_id}).text
    logging.debug('request_token: %s' % request_token)
    return request_token


def get_session_data(sender_id, data):
    if sender_id in list(data):
        return data[sender_id]
    else:
        return None


def clean_session(sender_id):
    data = [session_media_files, session_vote_options]
    for session_data in data:
        if sender_id in list(session_data):
            session_data.pop(sender_id)
    return


# Used in all subsequent
def get_group_uid(selected_group, sender_id):
    return selected_group
#     try:
#         match = ''
#         raw = get_group_menu_items(sender_id)
#         groups = {}
#         for i in range(len(raw)):
#             groups = {**groups, **{raw[i]['title']: i}}
#         threshold = 0.8
#         for group in list(groups):
#             sim_ratio = SequenceMatcher(None, group.lower(), selected_group.lower()).ratio()
#             if sim_ratio > threshold:
#                 match = group
#         return raw[groups[match]]['payload']
#     except KeyError as e:
#         logging.error(e)
#         return ''

# def intent(input):


# def restart_on_intent(intent):