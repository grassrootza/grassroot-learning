# training data maker
import json
import os
import time

intents = {"rasa_nlu_data": {"common_examples": []}}
meeting = {"rasa_nlu_data": {"common_examples": []}}
group = {"rasa_nlu_data": {"common_examples": []}}
todo = {"rasa_nlu_data": {"common_examples": []}}
vote = {"rasa_nlu_data": {"common_examples": []}}
update = {"rasa_nlu_data": {"common_examples": []}}


def convertTextToTD(text, intent, destination_file=1, *args):
    training_files = {
                      'intent_training_data.json': 1,
                      'meeting_training_data.json': 2,
                      'group_training_data.json': 5,
                      'todo_training_data.json': 4,
                      'vote_training_data.json': 3,
                      'update_training_data.json': 6
                      }

    keys = list(training_files)
    for key in keys:
        if training_files[key] == destination_file:
            print('%s is destined for %s' % (text, key))

    trainReady = {
                  "text": text,
                  "intent": intent,
                  "entities": []
        }
  
    if args:
        for arg in list(args[0]):
            start = text.lower().find(args[0][arg].lower())
            end = start+len(args[0][arg])
            print("Found arg: %s" % text[start:end])
            entity = {
                       "start": start,
                       "end": end,
                       "value": args[0][arg],
                       "entity": arg
            }
            trainReady["entities"].append(entity)

    print("Final json looks like this: %s" % json.dumps(trainReady))

    global intents
    global meeting
    global group
    global todo
    global vote
    global update

    if str(destination_file) == '1':
        print('writing to intent...\n\n')
        intents['rasa_nlu_data']['common_examples'].append(trainReady)
    elif str(destination_file) == '2':
        print('writing to meeting...\n\n')
        meeting['rasa_nlu_data']['common_examples'].append(trainReady)
    elif str(destination_file) == '3':
        print('writing to vote...\n\n')
        vote['rasa_nlu_data']['common_examples'].append(trainReady)
    elif str(destination_file) == '4':
        print('writing to todo...\n\n')
        todo['rasa_nlu_data']['common_examples'].append(trainReady)
    elif str(destination_file) == '5':
        print('writing to group...\n\n')
        group['rasa_nlu_data']['common_examples'].append(trainReady)
    else:
        if str(destination_file) == '6':
            print('writing to update...\n\n')
            update['rasa_nlu_data']['common_examples'].append(trainReady)


def compile():
    # write rooted files to their respective locations
    print('intents: %s' % intents)
    f = open('training_models/intent_training_data.json', 'w')
    f.write(json.dumps(intents))
    f.close() 
    print('\n\n')

    print('meeting: %s' % meeting)
    g = open('training_models/meeting_training_data.json', 'w')
    g.write(json.dumps(meeting)) 
    g.close()
    print('\n\n')

    print('vote: %s' % vote)
    h = open('training_models/vote_training_data.json', 'w')
    h.write(json.dumps(vote)) 
    h.close()    
    print('\n\n')

    print('todo: %s' % todo)
    i = open('training_models/todo_training_data.json', 'w')
    i.write(json.dumps(todo))
    i.close()     
    print('\n\n')

    print('group: %s' % group)
    j = open('training_models/group_training_data.json', 'w')
    j.write(json.dumps(group)) 
    j.close()
    print('\n\n')

    print('update: %s' % update)
    k = open('training_models/updates_training_data.json', 'w')
    k.write(json.dumps(update))
    k.close() 

# Intent trainer
## meeting
convertTextToTD("call a meeting", "call_meeting", 1)
convertTextToTD("set a meeting this friday with Abahlali Community Group about housing permits", "call_meeting", 1)
convertTextToTD("Voice meeting variations", "call_meeting", 1)
convertTextToTD("Meeting , Jozihub, 2pm/o’clock, today, Feedback session", "call_meeting", 1)
convertTextToTD("Meet at Jozihub about Feedback session week at 2pm today", "call_meeting", 1)
convertTextToTD("Meeting, today at 2pm/o’clock about the Feedback session at Jozihub", "call_meeting", 1)
convertTextToTD("Meet at JoziHub today for Feedback session at 2pm/o’clock", "call_meeting", 1)
convertTextToTD("Meet about the Feedback session at JoziHub today at 2 in the afternoon", "call_meeting", 1)
convertTextToTD("Feedback session, today, 2pm/o’clock, JoziHub, meeting", "call_meeting", 1)
convertTextToTD("Meeting, Enkomponi, 5pm/o’clock, tomorrow, protest action", "call_meeting", 1)
convertTextToTD("Meeting at Enkomponi, about protest action at 5pm/o’clock, tomorrow", "call_meeting", 1)
convertTextToTD("Meeting, tomorrow at 5pm/o’clock about protest action at Enkomponi", "call_meeting", 1)
convertTextToTD("Meet at Enkomponi tomorrow for protest action at 5 pm/o’’clock", "call_meeting", 1)
convertTextToTD("Meet about protest action at Enkomponi tomorrow at 5 in the evening", "call_meeting", 1)
convertTextToTD("Protest action, tomorrow, 5pm/o’clock, Enkomponi, meeting", "call_meeting", 1)
convertTextToTD("Meeting, KYP, 9am/o’clock, Saturday, Discussion Group", "call_meeting", 1)
convertTextToTD("Meeting at KYP, about Discussion Group at 9am/o’clock, this Saturday", "call_meeting", 1)
convertTextToTD("Meeting, next Saturday at 9am/o’clock about the Discussion Group at KYP", "call_meeting", 1)
convertTextToTD("Meet at KYP, Saturday after next for Discussion Group at 9 in the morning ", "call_meeting", 1)
convertTextToTD("Feedback session, last Saturday of this month, 9am/o’clock, KYP, meeting", "call_meeting", 1)
convertTextToTD("I want a meeting at Enkomponi", "call_meeting", 1)
convertTextToTD("I would (I’d) like to request a meeting", "call_meeting", 1)
convertTextToTD("Urgent meeting about Electricity ", "call_meeting", 1)
convertTextToTD("Record a meeting ", "call_meeting", 1)
convertTextToTD("TCC has a meeting at Sports Complex", "call_meeting", 1)
convertTextToTD("We would like to meet at Paki for housing permits", "call_meeting", 1)
convertTextToTD("Let’s meet at KYP", "call_meeting", 1)
convertTextToTD("Schedule a meeting for 2pm on Monday", "call_meeting", 1)
convertTextToTD("Organize a meeting at The Containers", "call_meeting", 1)
convertTextToTD("Create a meeting at Walter Sisulu Square", "call_meeting", 1)
convertTextToTD("Let’s have a meeting at Freedom Park Primary", "call_meeting", 1)
convertTextToTD("Do a meeting request for tonight", "call_meeting", 1)
convertTextToTD("I want a meeting on the  13th of July", "call_meeting", 1)
convertTextToTD("Strat a meeting about housing today at 6pm", "call_meeting", 1)
convertTextToTD("Start meeting request for Kliptown community", "call_meeting", 1)
convertTextToTD("Arrange a meeting for Khotso House for 2pm", "call_meeting", 1)
convertTextToTD("Set up a meeting at 5pm for Sanitation", "call_meeting", 1)
convertTextToTD("Set a meeting up for today at Milpark", "call_meeting", 1)
convertTextToTD("Execute a meeting request for this evening at 7", "call_meeting", 1)
convertTextToTD("Send meeting request to Mnandini Community Group", "call_meeting", 1)
convertTextToTD("I would like to order a meeting for today at 5pm", "call_meeting", 1)
convertTextToTD("Greater Kliptown Leadership would like to meet this Saturday at 10am", "call_meeting", 1)
convertTextToTD("Generate meeting request for SOPA this Tuesday", "call_meeting", 1)
convertTextToTD("Carry out a meeting request on behalf of Abahlali Forum", "call_meeting", 1)

## vote 
convertTextToTD("call a vote within the Abahlali Comminity Group", "call_vote", 1)
convertTextToTD("call a vote for housing permits in Abahlali community group", "call_vote", 1)
convertTextToTD("I would like for people to vote between water electricity and roads", "call_vote", 1)
convertTextToTD("call a vote on water and electricity and roads", "call_vote", 1)
convertTextToTD("call a vote between water and electricity and roads", "call_vote", 1)
convertTextToTD("call vote, water, electricity, roads", "call_vote", 1)
convertTextToTD("call a vote between water and electricity and roads in Abahlali Community Group", "call_vote", 1)
convertTextToTD("Lets vote on water and electricity and roads", "call_vote", 1)
convertTextToTD("Lets vote between water, electricity and roads in Abahlali Community Group", "call_vote", 1)
convertTextToTD("I would like to vote between roads, electricity, and water in Abahlali Community Group", "call_vote", 1)
convertTextToTD("Create a vote fora new Abahlali Community Group leader between Jon Hopkins and Nils Frahm", "call_vote", 1)
convertTextToTD("Cast a vote between the mortals Jon Hopkins and Nils Frahm", "call_vote", 1)
convertTextToTD("call a vote", "call_vote", 1)
convertTextToTD("call a vote for a new venue. Members can choose between Soweto and Braamfontein", "call_vote", 1)
convertTextToTD("call a vote for a new local councillor", "call_vote", 1)
## todos
convertTextToTD("tell all members in Abahlali community group to send their id numbers", "create_info_todo", 1)
convertTextToTD("find me people who would like to volunteer for a protest this friday", "create_volunteer_todo", 1)
convertTextToTD("create a volunteer task", "create_volunteer_todo", 1)
convertTextToTD("Lets protest for better service delivery this friday", "create_action_todo", 1)
convertTextToTD("Who wants to volunteer for a protest this friday", "create_volunteer_todo", 1)
convertTextToTD("Did everytone get home safe yesterday?", "create_validation_todo", 1)
convertTextToTD("Has everyone voted on service delivery?", "create_validation_todo", 1)
convertTextToTD("Can everyone please send their physical address", "create_info_todo", 1)
convertTextToTD("Can everytone please send their id numbers", "create_info_todo", 1)
## group
convertTextToTD("create a new group called Abahlali Community Group", "create_group", 1)
convertTextToTD("create group Abahlali Community Group", "create_group", 1)
convertTextToTD("new group Abahlali Community Group", "create_group", 1)
## update
convertTextToTD("tomorrow", "update", 1)
convertTextToTD("tomorrow 9am", "update", 1)
convertTextToTD("Abahlali Community Group", "update", 1)
convertTextToTD("Abahlali", "update", 1)
## affirm
convertTextToTD("yes", "affirm", 1)
convertTextToTD("absolutely", "affirm", 1)
convertTextToTD("indeed", "affirm", 1)
convertTextToTD("yes thats what I want", "affirm", 1)
## negate
convertTextToTD("no", "negate", 1)
convertTextToTD("no thats not what I want", "negate", 1)
convertTextToTD("wtf", "negate", 1)

# Meeting
# add more instances
convertTextToTD("call a meeting", "call_meeting", 2)
convertTextToTD("call a meeting tomorrow", "call_meeting", 2, *[{'datetime': 'tomorrow'}])
convertTextToTD("call a meeting for housing permits this saturday at Kliptown Community Centre", "call_meeting",
                *[{'subject': 'housing permits',
                   'datetime': 'this saturday',
                   'location': 'Kliptown Community Centre'}])

convertTextToTD("set a meeting this friday with Abahlali Community Group about housing permits", "call_meeting", 2, *[{'datetime': 'this friday',
                                                                                                                      'group': 'Abahlali Community Group',
                                                                                                                      'subject': 'housing permits'}])

convertTextToTD("Meeting , Jozihub, 2pm/o’clock, today, Feedback session", "call_meeting", 2, *[{'location': 'Jozihub', 
                                                                                                 'datetime': '2pm/o’clock, today', 
                                                                                                 'subject': 'Feedback session'}])

convertTextToTD("Meet at Jozihub about Feedback session week at 2pm today", "call_meeting", 2, *[{'datetime': '2pm today', 
                                                                                                  'location': 'Jozihub', 
                                                                                                  'subject': 'Feedback session'}])

convertTextToTD("Meeting, today at 2pm/o’clock about the Feedback session at Jozihub", "call_meeting", 2, *[{'location': 'Jozihub', 
                                                                                                             'datetime': 'today at 2pm/o’clock', 
                                                                                                             'subject': 'Feedback session'}])

convertTextToTD("Meet at JoziHub today for Feedback session at 2pm/o’clock", "call_meeting", 2, *[{'location': 'Jozihub', 
                                                                                                   'datetime': '2pm/o’clock', 
                                                                                                   'subject': 'Feedback session'}])

convertTextToTD("Meet about the Feedback session at JoziHub today at 2 in the afternoon", "call_meeting", 2, *[{'location': 'Jozihub', 
                                                                                                                'datetime': 'today at 2 in the afternoon', 
                                                                                                                'subject': 'Feedback session'}])

convertTextToTD("Feedback session, today, 2pm/o’clock, JoziHub, meeting", "call_meeting", 2, *[{'location': 'Jozihub', 
                                                                                                'datetime': 'today, 2pm/o’clock', 
                                                                                                'subject': 'Feedback session'}])

convertTextToTD("Meeting, Enkomponi, 5pm/o’clock, tomorrow, protest action", "call_meeting", 2, *[{'location': 'Enkomponi', 
                                                                                                   'datetime': '5pm/o’clock', 
                                                                                                   'subject': 'protest action'}])

convertTextToTD("Meeting at Enkomponi, about protest action at 5pm/o’clock, tomorrow", "call_meeting", 2, *[{'location': 'Enkomponi', 
                                                                                                             'datetime': '5pm/o’clock, tomorrow', 
                                                                                                             'subject': 'protest action'}])

convertTextToTD("Meeting, tomorrow at 5pm/o’clock about protest action at Enkomponi", "call_meeting", 2, *[{'location': 'Enkomponi',
                                                                                                              'datetime': 'tomorrow at 5pm/o’clock', 
                                                                                                              'subject': 'protest action'}])

convertTextToTD("Meet at Enkomponi tomorrow for protest action at 5 pm/o’’clock", "call_meeting", 2, *[{'location': 'Enkomponi', 
                                                                                                        'datetime': '5 pm/o’’clock',
                                                                                                        'subject': 'protest action'}])

convertTextToTD("Meet about protest action at Enkomponi tomorrow at 5 in the evening", "call_meeting", 2, *[{'location': 'Enkomponi', 
                                                                                                             'datetime': 'tomorrow', 
                                                                                                             'subject': 'protest action'}])

convertTextToTD("Protest action, tomorrow, 5pm/o’clock, Enkomponi, meeting", "call_meeting", 2, *[{'location': 'Enkomponi', 
                                                                                                   'datetime': 'tomorrow, 5pm/o’clock', 
                                                                                                   'subject': 'Protest action'}])

convertTextToTD("Meeting, KYP, 9am/o’clock, Saturday, Discussion Group", "call_meeting", 2, *[{'location': 'KYP',
                                                                                               'datetime': '9am/o’clock, Saturday',
                                                                                               'subject': 'Discussion Group'}])

convertTextToTD("Meeting at KYP, about Discussion Group at 9am/o’clock, this Saturday", "call_meeting", 2, *[{'location': 'KYP',
                                                                                               'datetime': '9am/o’clock, this Saturday',
                                                                                               'subject': 'Discussion Group'}])

convertTextToTD("Meeting, next Saturday at 9am/o’clock about the Discussion Group at KYP", "call_meeting", 2, *[{'location': 'KYP',
                                                                                               'datetime': 'next Saturday at 9am/o’clock',
                                                                                               'subject': 'Discussion Group'}])

convertTextToTD("Meet at KYP, Saturday after next for Discussion Group at 9 in the morning ", "call_meeting", 2, *[{'location': 'KYP',
                                                                                               'datetime': 'Saturday after next',
                                                                                               'subject': 'Discussion Group'}])

convertTextToTD("Feedback session, last Saturday of this month, 9am/o’clock, KYP, meeting", "call_meeting", 2, *[{'location': 'KYP',
                                                                                               'datetime': 'last Saturday of this month, 9am/o’clock',
                                                                                               'subject': 'Feedback session'}])
convertTextToTD("I want a meeting at Enkomponi", "call_meeting", 2, *[{'location': 'Enkomponi'}])
convertTextToTD("I would (I’d) like to request a meeting", "call_meeting", 2)
convertTextToTD("Urgent meeting about Electricity ", "call_meeting", 2, *[{'subject': 'Electricity'}])
convertTextToTD("Record a meeting ", "call_meeting", 2)
convertTextToTD("TCC has a meeting at Sports Complex", "call_meeting", 2, *[{'location': 'Sports Complex', 'group': 'TCC'}])
convertTextToTD("We would like to meet at Paki for housing permits", "call_meeting", 2, *[{'subject': 'housing permits', 'location': 'Paki'}])
convertTextToTD("Let’s meet at KYP", "call_meeting", 2, *[{'location': 'KYP'}])
convertTextToTD("Schedule a meeting for 2pm on Monday", "call_meeting", 2, *[{'datetime': '2pm on Monday'}])
convertTextToTD("Organize a meeting at The Containers", "call_meeting", 2, *[{'location': 'The Containers'}])
convertTextToTD("Create a meeting at Walter Sisulu Square", "call_meeting", 2, *[{'location': 'Walter Sisulu Square'}])
convertTextToTD("Let’s have a meeting at Freedom Park Primary", "call_meeting", 2, *[{'location': 'Freedom Park Primary'}])
convertTextToTD(" Do a meeting request for tonight", "call_meeting", 2, *[{'datetime': 'tonight'}])
convertTextToTD("I want a meeting on the  13th of July", "call_meeting", 2, *[{'datetime': '13th of July'}])
convertTextToTD("Start a meeting about housing today at 6pm", "call_meeting", 2, *[{'subject': 'housing', 'datetime': 'today at 6pm'}])
convertTextToTD("Start meeting request for Kliptown community", "call_meeting", 2, *[{'group': 'Kliptown community'}])
convertTextToTD("Arrange a meeting for Khotso House for 2pm", "call_meeting", 2, *[{'group': 'Khotso House', 'datetime': '2pm'}])
convertTextToTD("Set up a meeting at 5pm for Sanitation", "call_meeting", 2, *[{'datetime': '5pm', 'subject': 'Sanitation'}])
convertTextToTD("Set a meeting up for today at Milpark", "call_meeting", 2, *[{'location': 'Milpark'}])
convertTextToTD("Execute a meeting request for this evening at 7", "call_meeting", 2, *[{'datetime': 'this evening at 7'}])
convertTextToTD("Send meeting request to Mnandini Community Group", "call_meeting", 2, *[{'group': 'Mnandini Community Group'}])
convertTextToTD("I would like to order a meeting for today at 5pm", "call_meeting", 2, *[{'datetime': 'today at 5pm'}])
convertTextToTD("Greater Kliptown Leadership would like to meet this Saturday at 10am", "call_meeting", 2)
convertTextToTD("Plan a meeting for next Tuesday at 5pm", "call_meeting", 2, *[{'datetime': 'next Tuesday at 5pm'}])
convertTextToTD("Generate meeting request for SOPA this Tuesday", "call_meeting", 2, *[{'group': 'SOPA', 'datetime': 'this Tuesday'}])
convertTextToTD("Carry out a meeting request on behalf of Abahlali Forum", "call_meeting", 2)

# Vote
convertTextToTD("call a vote within the Abahlali Comminity Group", "call_vote", 3, *[{'group': 'Abahlali Community Group'}])
convertTextToTD("call a vote for housing permits in Abahlali community group", "call_vote", 3, *[{'group': 'Abahlali community group', 'subject': 'housing permits'}])
convertTextToTD("I would like for people to vote between water electricity and roads", "call_vote", 3, *[{'vote_option': 'water', 'vote_option': 'electricity', 'vote_option': 'roads'}])
convertTextToTD("call a vote on water and electricity and roads", "call_vote", 3, *[{'vote_option': 'water', 'vote_option': 'electricity', 'vote_option': 'roads'}])
convertTextToTD("call a vote between water and electricity and roads", "call_vote", 3, *[{'vote_option': 'water', 'vote_option': 'electricity', 'vote_option': 'roads'}])
convertTextToTD("call vote, water, electricity, roads", "call_vote", 3, *[{'vote_option': 'water', 'vote_option': 'electricity', 'vote_option': 'roads'}])
convertTextToTD("call a vote between water and electricity and roads in Abahlali Community Group", "call_vote", 3, *[{'group': 'Abahlali Community Group', 'vote_option': 'water', 'vote_option': 'electricity', 'vote_option': 'roads'}])
convertTextToTD("Lets vote on water and electricity and roads", "call_vote", 3, *[{'vote_option': 'water', 'vote_option': 'electricity', 'vote_option': 'roads'}])
convertTextToTD("Lets vote between water, electricity and roads in Abahlali Community Group", "call_vote", 3, *[{'group': 'Abahlali Community Group', 'vote_option': 'water', 'vote_option': 'electricity', 'vote_option': 'roads'}])
convertTextToTD("I would like to vote between roads, electricity, and water in Abahlali Community Group", "call_vote", 3, *[{'group': 'Abahlali Community Group', 'vote_option': 'water', 'vote_option': 'electricity', 'vote_option': 'roads'}])
convertTextToTD("Create a vote fora new Abahlali Community Group leader between Jon Hopkins and Nils Frahm", "call_vote", 3, *[{'group': 'Abahlali Community Group', 'vote_option': 'Jon Hopkins', 'vote_option': 'Nils Frahm'}])
convertTextToTD("Cast a vote between the mortals Jon Hopkins and Nils Frahm", "call_vote", 3, *[{'vote_option': 'Jon Hopkins', 'vote_option': 'Nils Frahm'}])

convertTextToTD("call a vote", "call_vote", 3)
convertTextToTD("call a vote for a new venue. Members can choose between Soweto and Braamfontein", "call_vote", 3, *[{'subject': 'new venue', 'vote_option': 'Soweto', 'vote_option': 'Braamfontein'}])
convertTextToTD("call a vote for a new local councillor", "call_vote", 3, *[{'subject': 'new local councillor'}])

# Todo
# support all four variations
convertTextToTD("tell all members in Abahlali community group to send their id numbers", "create_info_todo", 4, *[{'group': 'Abahlali Community Group', 'information_required': 'id numbers'}])
convertTextToTD("find me people who would like to volunteer for a protest this friday", "create_volunteer_todo", 4, *[{'volunteer_task': 'protest', 'datetime': 'this friday'}])

convertTextToTD("create a volunteer task", "create_volunteer_todo", 4)
convertTextToTD("Lets protest for better service delivery this friday", "create_action_todo", 4, *[{'subject': 'protest for better service delivery', 'datetime': 'this friday'}]) # action required
convertTextToTD("Who wants to volunteer for a protest this friday", "create_volunteer_todo", 4, *[{'subject': 'protest', 'datetime': 'this friday'}])
convertTextToTD("Did everytone get home safe yesterday?", "create_validation_todo", 4) # validation required
convertTextToTD("Has everyone voted on service delivery?", "create_validation_todo", 4) # validation required
convertTextToTD("Can everyone please send their physical address", "create_info_todo", 4, *[{'information_required': 'physical address'}])
convertTextToTD("Can everytone please send their id numbers", "create_info_todo", 4, *[{'information_required': 'id numbers'}])


# Group
convertTextToTD("create a new group called Abahlali Community Group", "create_group", 5, *[{'group': 'Abahlali Community Group'}])
convertTextToTD("create group Abahlali Community Group", "create_group", 5, *[{'group': 'Abahlali Community Group'}])
convertTextToTD("new group Abahlali Community Group", "create_group", 5, *[{'group': 'Abahlali Community Group'}])

# Update
convertTextToTD("tomorrow", "update", 6, *[{'datetime': 'tomorrow'}])
convertTextToTD("tomorrow 9am", "update", 6, *[{'datetime': 'tomorrow 9am'}])
convertTextToTD("Abahlali Community Group", "update", 6, *[{'group': 'Abahlali Community Group'}])
convertTextToTD("Abahlali", "update", 6, *[{'group': 'Abahlali'}])

compile()

os.system('python new_trainer.py')