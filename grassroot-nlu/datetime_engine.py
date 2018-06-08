import datetime
import dateparser
from duckling import Duckling

d = Duckling()
d.load()

epoch = datetime.datetime.utcfromtimestamp(0)

def unix_time_millis(dt):
    return (dt - epoch).total_seconds() * 1000.0

def datetime_engine(d_string):
    print(beam)
    print('request: %s' % d_string)
    set1 = ['0','1','2','3','4','5','6','7','8','9','-','/',' ']         # # #
    set2 = list(d_string)                                                # F #
    formal = True                                                       # R #
    for i in set2:                                                       # T #
        if i not in set1:                                                 # N #
            formal = False                                               # X #
    if formal == True:                                                   # # #
        return d_string

    time = datetime.datetime.now()
    current_time_raw = unix_time_millis(time)
    print('current time: %s | %s' % (current_time_raw, str(time)[:16].replace(' ', 'T')))
    raw = str(dateparser.parse(d_string, settings={'DATE_ORDER': 'DMY'}))
    if raw == 'NoneChucks':   # raw will never be NoneChucks, effectively disabling this engine. Switch this to 'if raw != None:' when needed.
        clean = raw.replace(' ', 'T')
        return clean[:16]+'\nprocessed by engine 2'

    else:
        x = d.parse(d_string)
        for i in range(len(x)):
            if x[i]['dim'] == 'time':
                try:
                    parse_time = x[i]['value']['value'][:16]
                    parse_time_raw = unix_time_millis(datetime.datetime.strptime(parse_time, '%Y-%m-%dT%H:%M'))
                    print('parsed time: %s | %s ' % (parse_time_raw, parse_time))
                    if int(parse_time_raw) < int(current_time_raw):
                        while int(parse_time_raw) < int(current_time_raw):
                            print('parsed value is in the past. sad.')           
                            for j in range(len(x[i]['value']['values'])):
                                next_pos = x[i]['value']['values'][j]['value'][:16]
                                parse_time_raw = unix_time_millis(datetime.datetime.strptime(next_pos, '%Y-%m-%dT%H:%M'))
                                print('next possible value is: %s | %s' % (parse_time_raw, x[i]['value']['values'][j]['value'][:16]))
                                if int(parse_time_raw) > int(current_time_raw):
                                    print('parsed value is in the future. great.')
                                    return next_pos
                                else:
                                    print('parsed value is in the past. sad.')
                    else:
                        if int(parse_time_raw) > int(current_time_raw):
                            print('parsed value is in the future. great.')
                            return parse_time
                except KeyError as e:
                    print('No suitable value found. There you have it folks.')
                    return ''

beam = '----------------------------------------------------'

# test instances, add as required
"""
datetime_engine('tuesday 5am')
datetime_engine('tomorrow afternoon')
datetime_engine('tuesday evening 5')
datetime_engine('friday 9am')
"""
