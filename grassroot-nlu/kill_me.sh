#!/bin/bash  

ps -ef | grep flask | grep -v grep | awk '{print $2}' | xargs sudo kill
ps -ef | grep "python trainer.py" | awk '{print $2}' | xargs sudo kill
ps -ef | grep "python checker.py" | awk '{print $2}' | xargs sudo kill
fuser -k 5000/tcp