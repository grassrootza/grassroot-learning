import psutil
import time
import os
import datetime
import requests
import json
import re


def test_engines():

    for i in range(10):
        test_text1 = 'i would like to set a meeting'
        dict_val = json.loads(requests.get('http://0.0.0.0:4000/parse?text=%s' % test_text1).content.decode('ascii'))
        try:
            if dict_val['parsed']['text'] == test_text1:
                state = 'passed'
            else:
                state = 'failed'
        except Exception as e:
            print('Test failed:')
            print(str(e))


        dict_val = json.loads(requests.get('http://0.0.0.0:4000/distance?text=Water ').content.decode('ascii'))

        if type(dict_val) == dict:
            hlvlstate = 'passed'
        else:
            hlvlstate = 'failed'
   

        z = requests.get('http://0.0.0.0:4000/datetime?date_string=tomorrow at 7 in the evening').content.decode('ascii')
        match = re.search(r'(\d+-\d+-\d+T)', z)
        if match:
            ret_val = 'passed'
        else:
            ret_val = 'failed'


    test_result = True
    engines = ['NLU engine ', 'Word distance engine ', 'Date-Time formalizer engine ']
    status = [state, hlvlstate, ret_val]
    for i in range(0,3):
        print(engines[i]+status[i])
        if status[i] == 'failed':
            test_result = False
    return test_result


def testCentre():
    #time.sleep(600)
    keep = []
    all_proc = psutil.net_connections()
    for i in all_proc:
        keep.append(i[3])

    if ('::', 4000) not in keep:
        print("System down at [%s]. Manual restart required" % str(datetime.datetime.now()))
        time.sleep(30)

    else:

        print("All's well. System up at %s" % str(datetime.datetime.now()))
        print('Sarting tests...')
        try:
            status = test_engines()
            if status == True:
                print('Test passed.')
            else:
                print('Test failed')
            return status
        except Exception as e:
            time.sleep(30)
            pass

testCentre()