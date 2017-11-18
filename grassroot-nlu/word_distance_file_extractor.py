import os
import boto3

client = boto3.client('s3')
s3 = boto3.resource('s3')


current_files = os.listdir('./')

word_distance_files = ["vocab.txt", "vectors.txt"]

for file in word_distance_files:
    if file not in current_files:
        s3.Bucket('grassroot-nlu').download_file('word_distance/%s' % file, 
                                                 '%s' % file)