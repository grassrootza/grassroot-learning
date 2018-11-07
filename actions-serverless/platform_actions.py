from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from rasa_core_sdk import Action
from rasa_core_sdk.forms import FreeTextFormField, FormAction
from rasa_core_sdk.events import SlotSet
from datetime import datetime
from difflib import SequenceMatcher
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import requests
import logging
import json
import uuid
import os
import ast
import smtplib


logging.basicConfig(format="[NLULOGS] %(asctime)s [%(threadName)-12.12s] [%(levelname)-5.5s]  %(message)s", level=logging.DEBUG)

auth_token = os.getenv('TOKEN_X')

BASE_URL = os.getenv('PLATFORM_BASE_URL', 'https://staging.grassroot.org.za/v2/api')
DATETIME_URL = os.getenv('DATE_TIME_URL', 'http://learning.grassroot.cloud')

TOKEN_PATH = '/whatsapp/user/token'
GROUP_PATH = '/group/fetch/minimal/filtered'
GROUP_NAME_PATH = '/v2/api/group/fetch/minimal/filtered'

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
                               'payload': 'next_page'
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
            message = MIMEMultipart()
            message['From'] = os.getenv('ALERT_EMAIL', 'grassrootnlu@gmail.com')
            message['To'] = os.getenv('DEVELOPER', '')
            message['Subject'] = "Token Trouble"
            body = "Greetings.\n\nplatform_actions.py has failed to retrieve auth token.\n Details: %s\
                    \n\nThis may be due to an expired token.\n\nRegards\n\nCore-Actions" % request_token
            message.attach(MIMEText(
                                    body,
                                    'plain'
                                   ))
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login(
                         message['From'],
                         os.getenv('ALERT_PWD', '')
                        )
            text = message.as_string()
            server.sendmail(
                            message['From'],
                            message['To'], text
                           )
            server.quit()
            logging.debug('developer notified.')
            return ''
    return request_token


def get_group_name(groupUid):
    response = requests.get(BASE_URL + GROUP_NAME_PATH)
    logging.debug('Got this back from group name retrieval: %s' % response)
    return groupUid


class ActionEvaluateIntent(Action):

    def name(self):
        return 'action_evaluate_intent'

    def run(self, tracker, dispatcher, domain):
        user_input = tracker.get_slot("group_uid")
        dispatcher.utter_message("Users entered %s" % user_input)

        if user_input == 'load_more':
            pageNumber = tracker.get_slot("page")
            if pageNumber == None:
                pageNumber = 0
            next_page = pageNumber + 1
            SlotSet("page", next_page)
            SlotSet("group_uid", None)
            dispatcher.utter_message("loading more groups")
            group_extractor = ActionGetGroup()
            return group_extractor.run(dispatcher, tracker, domain)
        return []


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
                     "You have chosen %s as your group." % get_group_name(tracker.get_slot("group_uid"))
                    ]
        dispatcher.utter_message(' '.join(responses))
        return []


class CreateMeetingComplete(Action):

    def name(self):
        return 'action_create_meeting_complete'

    def run(self, dispatcher, tracker, domain):
        groupUid = tracker.get_slot("group_uid")
        meeting_path = '/task/create/meeting/%s/%s' % (parentType, groupUid)
        url = BASE_URL + meeting_path
        logging.info('Constructed url for create meeting: %s' % url)
        response = requests.post(url, headers={'Authorization': 'Bearer ' + get_token(tracker.sender_id)},
                                 params={
                                         'location': tracker.get_slot("location"),
                                         'dateTimeEpochMillis': epoch(formalize(tracker.get_slot("datetime"))),
                                         'subject': tracker.get_slot("subject"),
                                         'description': tracker.get_slot("description")
                                         })
        dispatcher.utter_message('We are making it happen for you. Thank you for using our service.')
        logging.info('Constructed url for create meeting: %s' % response.url)
        logging.info('Dispatched to platform, response: %s' % response)
        clean_session(tracker.sender_id)
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
        vote_options_list = tracker.get_slot("vote_options")
        vote_options = ''
        for i in range(len(vote_options_list)):
            if i != len(vote_options_list) - 1:
                vote_options = vote_options + str(vote_options_list[i]) + ', '
            else:
                vote_options = vote_options + 'and ' + str(vote_options_list[i])
        template = ["You have chosen %s as your subject of your vote.",
                      "You have described this vote as %s",
                      "and want members of %s to vote between %s",
                      "by %s."]
        vote_status = ' '.join(template) % (tracker.get_slot("subject"), tracker.get_slot("description"),
                                           get_group_name(tracker.get_slot("group_uid")),
                                           vote_options, tracker.get_slot("datetime"))
        dispatcher.utter_message(vote_status)
        return []


class CreateVoteComplete(Action):

    def name(self):
        return 'action_create_vote_complete'

    def run(self, dispatcher, tracker, domain):
        groupUid = tracker.get_slot("group_uid")
        vote_path = '/task/create/vote/%s/%s' % (parentType, groupUid)
        url = BASE_URL + vote_path
        response = requests.post(url, headers={'Authorization': 'Bearer ' + get_token(tracker.sender_id)},
                                 params={
                                         'title': tracker.get_slot("subject"),
                                         'time': epoch(formalize(tracker.get_slot("datetime"))),
                                         'voteOptions': json.dumps(tracker.get_slot("vote_options")),
                                         'description': tracker.get_slot("description")
                                        })
        dispatcher.utter_message('We are making it happen for you. Thank you for using our service.')
        logging.info('Contructed url for create vote: %s' % response.url)
        logging.info('Received response from platform: %s' % response)
        clean_session(tracker.sender_id)
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
                     "You have chosen %s as your group." % get_group_name(tracker.get_slot("group_uid"))
                    ]
        dispatcher.utter_message(' '.join(responses))
        return []


class CreateInfoTodoComplete(Action):

    def name(self):
        return 'action_create_info_todo_complete'

    def run(self, dispatcher, tracker, domain):
        groupUid = tracker.get_slot("group_uid")
        todo_path = '/v2/api/task/create/todo/information/%s/%s' % (parentType, groupUid)
        url = BASE_URL + todo_path
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
                     "You have chosen %s as your group." % get_group_name(tracker.get_slot("group_uid"))
                    ]
        dispatcher.utter_message(' '.join(responses))
        return []


class CreateVolunteerTodoComplete(Action):

    def name(self):
        return 'action_create_volunteer_todo_complete'

    def run(self, dispatcher, tracker, domain):
        groupUid = tracker.get_slot("group_uid")
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
                     "You have chosen %s as your group." % get_group_name(tracker.get_slot("group_uid"))
                    ]
        dispatcher.utter_message(' '.join(responses))
        return []


class CreateValidationTodoComplete(Action):

    def name(self):
        return 'create_validation_todo_complete'

    def run(self, dispatcher, tracker, domain):
        groupUid = tracker.get_slot("group_uid")
        todo_path = '/v2/api/task/create/todo/confirmation/%s/%s' % (parentType, groupUid)
        url = BASE_URL + todo_path
        response = requests.post(url, headers={'Authorization': 'Bearer ' + get_token(tracker.sender_id)},
                                 params={
                                         'subject': tracker.get_slot("subject"),
                                         'dueDateTime': epoch(formalize(tracker.get_slot("datetime")))
                                        })
        dispatcher.utter_message('We are making it happen for you. Thank you for using our service.')
        logging.info('Contructed url for create validation todo: %s' % response.url)
        logging.info('Received response from platform: %s' % response)
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
                     "You have chosen %s as your group." % get_group_name(tracker.get_slot("group_uid"))
                   ]
        dispatcher.utter_message(' '.join(responses))
        return []


class CreateActionTodoComplete(Action):

    def name(self):
        return 'action_create_todo_action_complete'

    def run(self, dispatcher, tracker, domain):
        groupUid = tracker.get_slot("group_uid")
        todo_path = '/v2/api/task/create/todo/action/%s/%s' % (parentType, groupUid)
        url = BASE_URL + todo_path
        response = requests.post(url, headers={'Authorization': 'Bearer ' + get_token(tracker.sender_id)},
                                 params={
                                         'subject': tracker.get_slot("subject"),
                                         'dueDateTime': epoch(formalize(tracker.get_slot("datetime")))
                                         })
        dispatcher.utter_message('We are making it happen for you. Thank you for using our service.')
        logging.info('Contructed url for create action todo: %s' % response.url)
        logging.info('Received response from platform: %s' % response)
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
        return []


class ActionSaveMediaFile(Action):

    def name(self):
        return 'action_save_media_file_id'

    def run(self, dispatcher, tracker, domain):
        media_file = (tracker.latest_message)['text']
        logging.debug("Recieved media file: %s" % media_file)
        current_media_files = tracker.get_slot("media_file_ids")
        logging.debug("Current media files are: %s" % current_media_files)
        if current_media_files == None:
            current_media_files = []
        current_media_files.append(media_file)
        logging.debug("Media files now look like: %s" % tracker.get_slot("media_file_ids"))
        return [SlotSet("media_file_ids", current_media_files)]


class ActionUtterLivewireStatus(Action):

    def name(self):
        return 'action_utter_livewire_status'

    def run(self, dispatcher, tracker, domain):
        template = [
                     "You have chosen %s as the title.",
                     "You have entered '%s' as the content.",
                     "You have identified yourself as %s",
                     "and provided %s as your contact detail.",
                     "",
                     "You would like this to appear within the group %s."
                    ]
        media_files = tracker.get_slot("media_file_ids")
        if len(media_files) > 1:
        	template[4] = "You have also included %s media files." % len(media_files)
        elif len(media_files) == 1:
        	template[4] = "You have also included an image to this livewire."
        else:
        	template.pop(4)
        livewire_status = ' '.join(template) % (tracker.get_slot("subject"), tracker.get_slot("description"),
                                                tracker.get_slot("contact_name"), tracker.get_slot("contact_number"),
                                                get_group_name(tracker.get_slot("group_uid")))
        dispatcher.utter_message(livewire_status)
        return []


class CreateLivewireComplete(Action):

    def name(self):
        return 'action_create_livewire_complete'

    def run(self, dispatcher, tracker, domain):
        headline = tracker.get_slot("subject")
        description = tracker.get_slot("description")
        contactName = tracker.get_slot("contact_name")
        contactNumber =  tracker.get_slot("contact_number")
        taskUid = tracker.get_slot("task_uid")
        livewire_type = 'INSTANT'
        addLocation = False
        mediaFileKeys = get_session_data(tracker.sender_id, session_media_files)
        latitude = tracker.get_slot("latitude")
        longitude = tracker.get_slot("longitude")
        destUid = tracker.get_slot("destination_uid")
        groupUid = tracker.get_slot("group_uid")
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
