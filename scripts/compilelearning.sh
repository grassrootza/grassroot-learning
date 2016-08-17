#!/bin/bash
#yum -y install httpd > /var/log/installapache.out 2>&1
. /etc/environment
cd /var/grassroot
gradle build