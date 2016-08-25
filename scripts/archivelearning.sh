#!/bin/bash
cp -r /var/grassroot-learning /var/grassroot-learning-`date +'%Y-%m-%d-%H-%M-%s'`
rm -rf /var/grassroot-learning/*
rm -f /var/grassroot-learning/.pid
echo "CLEAN"
