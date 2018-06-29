import datetime
import dateparser
import time
from googletrans import Translator
from duckling import Duckling

translator = Translator()
d = Duckling()
d.load()

epoch = datetime.datetime.utcfromtimestamp(0)

def unix_time_millis(dt):
    return (dt - epoch).total_seconds() * 1000.0

def datetime_engine(d_string):
    print(beam)
    print('request: %s' % d_string)
    set1 = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '-', '/', ' ', '.', '_']
    set2 = list(d_string)
    formal = True
    for i in set2:
        if i not in set1:
            formal = False
    if formal == True:
        new_time = verify_format(transform(d_string).strip().replace(' ', '-').replace('/', '-').replace('.','-').replace('_','-'))+'T00:00'
        try:
            datetime.datetime.strptime(new_time, "%d-%m-%YT00:00")
            print('returning: %s' % new_time)
            return new_time
        except ValueError as e:
            print('could not parse request.\nreturning: %s' % d_string)
            return d_string

    time = datetime.datetime.now()
    current_time_raw = unix_time_millis(time)
    print('current time: %s | %s' % (current_time_raw, str(time)[:16].replace(' ', 'T')))
    raw = str(dateparser.parse(d_string, settings={'DATE_ORDER': 'DMY'}))
    if raw == 'NoneChucks':   # raw will never be NoneChucks, effectively disabling this engine. Switch this to 'if raw != None:' when needed.
        clean = raw.replace(' ', 'T')
        return clean[:16]

    else:
        d_string = translate(d_string)
        x = d.parse(d_string)
        for i in range(len(x)):
            if x[i]['dim'] == 'time':
                try:
                    parse_time = x[i]['value']['value'][:16]
                    parse_time_raw = unix_time_millis(datetime.datetime.strptime(parse_time, '%Y-%m-%dT%H:%M'))
                    print('parsed time: %s | %s ' % (parse_time_raw, parse_time))
                    if int(parse_time_raw) < int(current_time_raw):
                        cycle = 0
                        cycle2 = 0
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
                                    cycle += 1
                                    if cycle == 8:
                                        print('No suitable value found. There you have it folks.')
                                        return ''
                            if cycle2 == 8:
                                print('No suitable value found. There you have it folks.')
                                return ''
                            else:
                                cycle2 += 1
                    else:
                        if int(parse_time_raw) > int(current_time_raw):
                            print('parsed value is in the future. great.')
                            return parse_time
                except KeyError as e:
                    print('No suitable value found. There you have it folks.')
                    return ''


def verify_format(ds):
    x = ds.split('-')
    fmtd = []
    for i in x:
        if len(i) == 1:
            prefix = '0'
            fmtd.append(prefix+i)
        else:
            fmtd.append(i)
    return '-'.join(fmtd)


def transform(dst):
    ds = dst.strip().replace('/', '').replace('.', '').replace('_','').replace('-','').replace(' ','')
    if len(ds) == 6 or len(ds) == 8:
        if ' ' not in ds:
            dd = ds[:2]
            mm = ds[2:4]
            yy = ds[4:]
            if len(yy) == 2:
                prefix = '20'
                this_year = datetime.datetime.now().year
                if prefix+yy == this_year:
                    yy = this_year
                else:
                    yy = prefix+yy
            raw = [dd,mm,yy]
            return '-'.join(raw)
        else:
            return dst
    else:
        return dst

def translate(ds):
    try:
        translated = translator.translate(ds)
        trans_json = translated.__dict__
        trans_text = trans_json['text']
        print('translater recieved: %s \ntranslated to: %s' % (ds, trans_text))
        return trans_text
    except Exception as e:
        print(str(e))
        return ds


beam = '----------------------------------------------------'


def test_engine(*csv):
    if not csv:
        datetime_engine('tuesday 5am')
        datetime_engine('tomorrow afternoon')
        datetime_engine('tuesday evening 5')
        datetime_engine('friday 9am')
        datetime_engine('today')
        datetime_engine('today at 9pm')
        datetime_engine('29 06 2018')
        datetime_engine('26/01/2019')
        datetime_engine('27.08.2018')
        datetime_engine('tuesday  August 2018')
        datetime_engine('26 6 2018')
        datetime_engine('200618')
        datetime_engine('20062018')
        datetime_engine('2606 430') # unsupported
        datetime_engine('2606 4300') # unsupported
        datetime_engine('2606') # unsupported
        datetime_engine('20/06/18')
        datetime_engine('20/06/2018')
        datetime_engine('20.06.08')
        datetime_engine('20.06.2018')
        datetime_engine('20_06_08')
        datetime_engine('20_06_2018')
        datetime_engine('20-6-2018')
        datetime_engine('20-06-18')
        datetime_engine('ngomso at 5pm')
        datetime_engine('kusasa ngo 11pm')
    else:
        test_file = open('time_inputs.csv', 'r')
        raw_data = test_file.read()
        split_data = raw_data.split('\n')
        print(split_data)

        for line in split_data:
            # print('line: %s' % line)
            try:
                start = line.find("input:")+7
                datetime_engine(line[start:].replace('"',''))
                # time.sleep(3)
            except:
                pass


# test_engine()
# test_engine(*['csv_mode'])