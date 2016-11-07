from random import randint
import csv


action_words = ['vote', 'vote', 'meet', 'meeting', 'todo', 'to do', 'action']
verbs = ['have', 'host', 'take', 'hold', 'record', 'call', 'schedule']
date = ['next tuesday', 'on friday', 'on saturday', 'next wednesday', 'on monday', 'on september 24', 'on aug 31']
time = ['noon', '10am', '14h00', '8pm', '7:00', 'at 4pm', '@ 6h00', 'at 9:00']

none_open = ['has anyone', 'hi everyone', 'does anyone', 'hey', 'hi', 'should we', 'we should', 'I think', 'what if we']
none_filler = ['lets talk about', 'lets discuss']
none_topics = ['water', 'unemployment', 'community', 'government', 'economy', 'business', 'living conditions',
               'townships', 'social movements', 'politics', 'housing', 'crime', 'roads', 'water supply', 'corruption',
               'education', 'schools']
none_endings = ['okay', 'sounds good', 'see you soon']

other = ['welcome', "let's chat", 'lets chat', 'nice to see you again', 'hows the', 'suhhh']
other_more = ['family', 'mom', 'dad', 'neighbor', 'animals', 'pets', 'politician', 'music']
other_even_more = ['I hope you are well', 'chillin', 'eat your veggies', 'cook dinner', 'whip it real good', 'nonsense']


def add_label(index):
    if index == 0 or index == 1:
        return '3' + '\t'
    elif 1 < index <= 3:
        return '2' + '\t'
    else:
        return '4' + '\t'


def add_datetime(s):
    return s + ' ' + date[randint(0, len(date) - 1)] + ' ' + time[randint(0, len(time) - 1)]


def generate_chat_file():
    with open('artificial_chat2.txt', 'w') as outfile:
        for x in range(0, 90):
            date_chance = randint(0, 1)
            action_index = randint(0, len(action_words) - 1)
            s = add_label(action_index)
            s += verbs[randint(0, len(verbs) - 1)] + ' a ' \
                + action_words[action_index]
            if date_chance == 0:
                s = add_datetime(s)
            outfile.write(s)
            outfile.write('\n')

        for x in range(0, 300):
            s = '1' + '\t' + none_open[randint(0, len(none_open) - 1)] + ' ' +\
                none_filler[randint(0, len(none_filler) - 1)] + ' ' + none_topics[randint(0, len(none_topics) - 1)]
            outfile.write(s)
            outfile.write('\n')

        for x in range(0, 50):
            s = '1' + '\t' + none_endings[randint(0, len(none_endings) - 1)]
            outfile.write(s)
            outfile.write('\n')

        for x in range(0, 100):
            action_index = randint(0, len(action_words) - 1)
            s = '1' + '\t'
            s += verbs[randint(0, len(verbs) - 1)] + ' a ' + action_words[action_index] + '?'
            outfile.write(s)
            outfile.write('\n')

# with open('chat.test', 'w') as outfile:
#     for x in range(0, 200):
#         s = '1' + '\t' + other[randint(0, len(other) - 1)] + ' ' + \
#             other_more[randint(0, len(other_more) - 1)] + ' ' + other_even_more[randint(0, len(other_even_more) - 1)]
#         outfile.write(s)
#         outfile.write('\n')


generate_chat_file()