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

BASE_URL = 'https://staging.grassroot.org.za'
TOKEN_URL = 'https://staging.grassroot.org.za/v2/api/whatsapp/user/token'
DATETIME_URL = 'http://learning.grassroot.cloud'
PRE_TOK_URL = 'https://staging.grassroot.org.za/v2/api/whatsapp/user/id'
GROUP_URL = 'https://staging.grassroot.org.za/v2/api/group/fetch/list'

auth_token = os.getenv("TOKEN_X")
parentType = 'GROUP'
session_vote_options = {'user_id': []}
session_media_files = {'user_id': []}


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


# class ActionCreateGroupRoutine(FormAction):
#
#     RANDOMIZE = False
#
#     @staticmethod
#     def required_fields():
#         return [
#             FreeTextFormField("group"),
#             FreeTextFormField("description"),
#             FreeTextFormField("reminderMinutes")
#         ]
#
#     def name(self):
#         return 'action_create_group_routine'
#
#     def submit(self, dispatcher, tracker, domain):
#         responses = [
#                      "You have named this group %s" % tracker.get_slot("group_name"),
#                      "You have described this group as %s" % tracker.get_slot("description"),
#                      "You would like reminders to be sent to users %s" % tracker.get_slot("reminderMinutes")
#                     ]
#         responses.utter_message(' '.join(responses))
#         return []


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
        responses.utter_message(' '.join(responses))
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


class ActionGetGroup(Action):

    def name(self):
        return 'action_get_group'

    def run(self, dispatcher, tracker, domain):
        dispatcher.utter_button_message("Choose a group", get_group_menu_items(tracker.sender_id))
        return []


class ActionSaveGroup(Action):

    def name(self):
        return 'action_utter_save_selected_group'

    def run(self, dispatcher, tracker, domain):
        group = (tracker.latest_message)['text']
        return [SlotSet("group", group)]


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


class CreateMeetingUrl(Action):

    def name(self):
        return 'action_create_meeting_url'

    def run(self, dispatcher, tracker, domain):
        groupUid = get_group_uid(tracker.get_slot("group"), tracker.sender_id)
        if groupUid == '':
            dispatcher.utter_message('Could not find %s within registered groups.' % tracker.get_slot("group"))
            return []
        meeting_path = '/v2/api/task/create/meeting/%s/%s' % (parentType, groupUid)
        query_params = '?location=%s&dateTimeEpochMillis=%s&subject=%s&description=%s' % (\
                       tracker.get_slot('location'), epoch(formalize(tracker.get_slot("datetime"))), \
                       tracker.get_slot('subject'), tracker.get_slot('description'))
        url = BASE_URL+meeting_path+query_params.replace(' ', '%20')
        dispatcher.utter_message('We are making it happen for you. Thank you for using our service.')
        dispatcher.utter_message('Constructed url: %s' % url)
        # response = requests.post(url, headers={'Authorization': 'Bearer ' + get_token(tracker.sender_id)}))
        return []


class CreateVoteUrl(Action):

    def name(self):
        return 'action_create_vote_url'

    def run(self, dispatcher, tracker, domain):
        groupUid = get_group_uid(tracker.get_slot("group"), tracker.sender_id)
        if groupUid == '':
            dispatcher.utter_message('Could not find %s within registered groups.' % tracker.get_slot("group"))
            return []
        vote_path = '/v2/api/task/create/vote/%s/%s' % (parentType, groupUid)
        query_params = '?title=%s&time=%s&voteOptions=[%s]&description=%s' % (\
                       tracker.get_slot('subject'), epoch(formalize(tracker.get_slot("datetime"))),
                       get_session_data(tracker.sender_id, session_vote_options), tracker.get_slot('description'))
        url = BASE_URL+vote_path+query_params.replace(' ', '%20')
        dispatcher.utter_message('We are making it happen for you. Thank you for using our service.')
        dispatcher.utter_message('Contructed url: %s' % url)
        # response = requests.post(url, headers={'Authorization': 'Bearer ' + get_token(tracker.sender_id)}))
        clean_session(tracker.sender_id)
        return []


# class CreateGroupUrl(Action):
#
#     def name(self):
#         return 'action_create_group_url'
#
#     def run(self, dispatcher, tracker, domain):
#         group_path = '/v2/api/group/modify/create'
#         query_params = '?name=%s&description=%s&reminderMinutes=%s' % (tracker.get_slot('group'), \
#                        tracker.get_slot('description'), tracker.get_slot('reminderMinutes'))
#         url = BASE_URL+group_path+query_params.replace(' ', '%20')
#         dispatcher.utter_message('Constructed url: %s' % url)
#         # response = requests.post(url, headers={'Authorization': 'Bearer ' + get_token(tracker.sender_id)}))
#        return []


class CreateVolunteerTodoUrl(Action):

    def name(self):
        return 'action_create_volunteer_todo_url'

    def run(self, dispatcher, tracker, domain):
        groupUid = get_group_uid(tracker.get_slot("group"), tracker.sender_id)
        if groupUid == '':
            dispatcher.utter_message('Could not find %s within registered groups.' % tracker.get_slot("group"))
            return []
        todo_path = '/v2/api/task/create/todo/volunteer/%s/%s' % (parentType, groupUid)
        query_params = '?subject=%s&dueDateTime=%s' % (tracker.get_slot("subject"),
                        formalize(tracker.get_slot("datetime")))
        url = BASE_URL+todo_path+query_params.replace(' ', '%20')
        dispatcher.utter_message('We are making it happen for you. Thank you for using our service.')
        dispatcher.utter_message('Constructed url: %s' % url)
        # response = requests.post(url, headers={'Authorization': 'Bearer ' + get_token(tracker.sender_id)}))
        return []


class CreateValidationTodoUrl(Action):

    def name(self):
        return 'create_validation_todo_url'

    def run(self, dispatcher, tracker, domain):
        groupUid = get_group_uid(tracker.get_slot("group"), tracker.sender_id)
        if groupUid == '':
            dispatcher.utter_message('Could not find %s within registered groups.' % tracker.get_slot("group"))
            return []
        todo_path = '/v2/api/task/create/todo/confirmation/%s/%s' % (parentType, groupUid)
        query_params = '?subject=%s&dueDateTime=%s' % (tracker.get_slot("subject"),
                        epoch(formalize(tracker.get_slot("datetime"))))
        url = BASE_URL+todo_path+query_params.replace(' ', '%20')
        dispatcher.utter_message('We are making it happen for you. Thank you for using our service.')
        dispatcher.utter_message('Constructed url: %s' % url)
        # response = requests.post(url, headers={'Authorization': 'Bearer ' + get_token(tracker.sender_id)}))
        return []


class CreateInfoTodoUrl(Action):

    def name(self):
        return 'action_create_info_todo_url'

    def run(self, dispatcher, tracker, domain):
        groupUid = get_group_uid(tracker.get_slot("group"), tracker.sender_id)
        if groupUid == '':
            dispatcher.utter_message('Could not find %s within registered groups.' % tracker.get_slot("group"))
            return []
        todo_path = '/v2/api/task/create/todo/information/%s/%s' % (parentType, groupUid)
        query_params = '?subject=%s&dueDateTime=%s&responseTag=%s' % (tracker.get_slot("subject"),
                        epoch(formalize(tracker.get_slot("datetime"))), tracker.get_slot("response_tag"))
        url = BASE_URL+todo_path+query_params.replace(' ', '%20')
        dispatcher.utter_message('We are making it happen for you. Thank you for using our service.')
        dispatcher.utter_message('Constructed url: %s' % url)
        # response = requests.post(url, auth=(user, headers={'Authorization': 'Bearer ' + get_token(tracker.sender_id)}))
        return []


class CreateActionTodoUrl(Action):

    def name(self):
        return 'action_create_todo_action_url'

    def run(self, dispatcher, tracker, domain):
        groupUid = get_group_uid(tracker.get_slot("group"), tracker.sender_id)
        if groupUid == '':
            dispatcher.utter_message('Could not find %s within registered groups.' % tracker.get_slot("group"))
            return []
        todo_path = '/v2/api/task/create/todo/action/%s/%s' % (testParentType, groupUid)
        query_params = '?subject=%s&dueDateTime=%s&' % (tracker.get_slot("subject"),
                        epoch(formalize(tracker.get_slot("datetime"))))
        url = BASE_URL+todo_path+query_params.replace(' ', '%20')
        dispatcher.utter_message('We are making it happen for you. Thank you for using our service.')
        dispatcher.utter_message('Constructed url: %s' % url)
        # response = requests.post(url, headers={'Authorization': 'Bearer ' + get_token(tracker.sender_id)}))
        return []


class CreateLivewireUrl(Action):

    def name(self):
        return 'action_create_livewire_url'

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
        query_params = '?headline=%s&description=%s&contactName=%s&contactNumber=%s&groupUid=%s&taskUid=%s&type=%s&addLocation=%s&mediaFileKeys=%s&latitude=%s&longitude=%s&destUid=%s' % \
                       (headline, description, contactName, contactNumber, groupUid, taskUid, livewire_type, addLocation, mediaFileKeys, latitude, longitude, destUid)
        url = BASE_URL+livewire_path+query_params
        dispatcher.utter_message('We are making it happen for you. Thank you for using our service.')
        dispatcher.utter_message("Contructed url: %s" % url)
        # response = requests.post(url, headers={'Authorization': 'Bearer ' + get_token(tracker.sender_id)}))
        clean_session(tracker.sender_id)
        return []


class ActionSaveMediaFile(Action):

    def name(self):
        return 'action_save_media_file'

    def run(self, dispatcher, tracker, domain):
        media_file = tracker.get_slot("media_file_id")
        if media_file != None:
            if tracker.sender_id in list(session_media_files):
                session_media_files[sender_id].append(media_file)
                return [SlotSet('media_file_keys', session_media_files[tracker.sender_id])]
            else:
                session_media_files[sender_id] = [media_file]
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
    server_user_id = requests.post(PRE_TOK_URL, headers={'Authorization': 'Bearer ' \
                                   + auth_token}, params={'msisdn': '%s' % sender_id}).text
    logging.debug('resp: %s' % server_user_id)
    request_token = requests.post(TOKEN_URL, headers={'Authorization': 'Bearer ' + auth_token},\
                                  params={'userId': server_user_id}).text
    logging.debug('request_token: %s' % request_token)
    return request_token


def get_group_menu_items(sender_id):
    raw_json = json.loads(requests.get(GROUP_URL, headers={'Authorization': 'Bearer ' + get_token(sender_id)}).text)
    menu_items = []
    for group in range(len(raw_json)):
        menu_items.append({'title': raw_json[group]['name'], 'payload': raw_json[group]['groupUid']})
    return menu_items


def get_group_uid(selected_group, sender_id):
    try:
        match = ''
        raw = get_group_menu_items(sender_id)
        groups = {}
        for i in range(len(raw)):
            groups = {**groups, **{raw[i]['title']: i}}
        threshold = 0.8
        for group in list(groups):
            sim_ratio = SequenceMatcher(None, group.lower(), selected_group.lower()).ratio()
            if sim_ratio > threshold:
                match = group
        return raw[groups[match]]['payload']
    except KeyError as e:
        logging.error(e)
        return ''


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