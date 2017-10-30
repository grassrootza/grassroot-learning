#!/bin/bash  

ps -ef | grep flask | grep -v grep | awk '{print $2}' | xargs kill