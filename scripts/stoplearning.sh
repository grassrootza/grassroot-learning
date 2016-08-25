#!/bin/bash

if [[ -f /var/grassroot-learning/.pid ]]; then
        #kill -TERM `cat /var/grassroot-learning/.pid`;
        kill `cat /var/grassroot-learning/.pid`;
	mypid=`cat /var/grassroot-learning/.pid`;
	while [[ `ps -p $mypid > /dev/null;echo $?` -eq '0' ]]; do 
		echo -n '.'; 
		sleep 1; 
	done
        rm -f  /var/grassroot-learning/.pid;
fi

echo STOPPING DONE