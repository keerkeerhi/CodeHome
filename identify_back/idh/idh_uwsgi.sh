#!/bin/bash
if [ ! -n "$1" ]
then
    echo "Usages: sh idh_uwsgi.sh [start|stop|restart]"
    exit 0
fi

if [ $1 = start ]
then
    psid=`ps aux | grep "idh_uwsgi.ini" | grep -v "grep" | wc -l`
    if [ $psid -gt 4 ]
    then
        echo "uwsgi is running!"
        exit 0
    else
        /opt/python3/bin/uwsgi --ini /var/www/idh/idh_uwsgi.ini &
        echo "Start uwsgi service [OK]"
    fi
    

elif [ $1 = stop ];then
    ps aux | grep "idh_uwsgi.ini" | grep -v "grep"|awk '{print $2}'|xargs kill -9
    echo "Stop uwsgi service [OK]"
elif [ $1 = restart ];then
    ps aux | grep "idh_uwsgi.ini" | grep -v "grep"|awk '{print $2}'|xargs kill -9
    sleep 1
    /opt/python3/bin/uwsgi --ini /var/www/idh/idh_uwsgi.ini &
    echo "Restart uwsgi service [OK]"

else
    echo "Usages: sh idh_uwsgi.sh [start|stop|restart]"
fi
