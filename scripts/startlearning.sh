#!/bin/bash
. /etc/environment

CURR=$PWD
cd /var/grassroot-learning
nohup java -jar build/libs/gs-rest-service-0.1.0.jar > grassroot-learning.log 2>&1 &
echo $! > .pid
cd $CURR
