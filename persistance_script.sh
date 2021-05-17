#!/bin/sh

source venv/bin/activate
python ./gestao_usuarios/persist_new_tweets.py

echo $(date '+%d/%m/%Y %H:%M:%S') >> ping_cronjob.txt