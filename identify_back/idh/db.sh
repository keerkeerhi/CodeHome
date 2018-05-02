#!/usr/bin/env bash
/opt/python3/bin/python3 manage.py makemigrations
/opt/python3/bin/python3 manage.py migrate

/etc/init.d/nginx restart
nohup bash idh_uwsgi.sh restart &
bash ck_sync.sh
