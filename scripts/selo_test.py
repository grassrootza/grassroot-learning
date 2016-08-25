#!/usr/bin/env python

import requests, time, psycopg2, csv, re, os
from slacker import Slacker

csv_filename = "../grassroot-resources/logs/ussd_date_entry_" + time.strftime('%b%d') + '.csv'

# handle jan/dec case
if int(time.strftime('%m')) - 1 != 0:
    last_month_filename= 'hist/selo_errors_' + str(int(time.strftime('%m')) - 1) + '.txt'
else: 
    last_month_filename= 'hist/selo_errors_' + str(12) + '.txt'    

this_month_filename = 'hist/selo_errors_' + str(int(time.strftime('%m'))) + '.txt'


def get_log_from_db(DB, USER, PWD, HOST, PORT):
    conn = psycopg2.connect(database=DB, user=USER, password=PWD, host=HOST, port=PORT)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM selo_read_only.date_time_logs')
    records = cursor.fetchall()

    with open(csv_filename, 'w') as f:
        writer = csv.writer(f, delimiter=',')
        for row in records:
            writer.writerow(row)


def parse_file(filename):
    with open(filename) as infile, open('tmp/parsed_logs.txt', 'w') as outfile:
        for line in infile:
            d = re.search('input: [[a-zA-Z0-9.-@ ]*]*', line)
            if d:
                d = d.group(0)
                date = d[7:]
                outfile.write(date)
                outfile.write('\n')
    return 'tmp/parsed_logs.txt'


def get_results_file(log_file):
    with open(log_file) as infile, open(this_month_filename, 'w') as outfile:
        for line in infile:
            url = 'http://localhost:9000/parse?phrase=' + line
            data = requests.get(url)

            if data.text == 'ERROR_PARSING':
                outfile.write(line)


def get_differences_from_last_month(this_month, last_month):
    with open(this_month, 'r') as file1:
        with open(last_month, 'r') as file2:
            diff = set(file2).difference(file1)
    diff.discard('\n')
    with open(this_month, 'a') as file1:
        file1.write('\n' + '***** NEW THIS MONTH *****' + '\n')
        file1.writelines(diff)


def main():
    resources = []
    with open('../grassroot-resources/test_config.properties') as f:
        for line in f:
            resources.append(re.search('=[a-zA-Z0-9.-@ -]*', line.strip()).group(0)[1:])
    
    slack = Slacker(resources[0])

    get_log_from_db(resources[1], resources[2], resources[3], resources[4], resources[5])
    get_results_file(parse_file(csv_filename))
    get_differences_from_last_month(this_month_filename, last_month_filename)

    slack.files.upload(this_month_filename, channels='#learning')


main()
