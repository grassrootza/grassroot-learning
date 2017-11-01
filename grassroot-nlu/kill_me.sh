#!/bin/bash  

ps -ef | grep flask | grep -v grep | awk '{print $2}' | xargs kill
kill $(ps aux | grep python checker.py | awk '{ print $2 }')
kill $(ps aux | grep python trainer.py | awk '{ print $2 }')