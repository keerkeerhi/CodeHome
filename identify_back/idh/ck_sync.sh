#!/bin/bash
#ps aux | grep "SyncInvitePhoneAuto.py" | grep -v "grep"|awk '{print $2}'|xargs kill -9
#sleep 1
#cd /var/www/idh/ShellScript && nohup /opt/python3/bin/python3 SyncInvitePhoneAuto.py &
#echo "Restart sync invite phone!"

ps aux | grep "SyncUserUnion.py" | grep -v "grep"|awk '{print $2}'|xargs kill -9
sleep 1
cd /var/www/idh/ShellScript && nohup /opt/python3/bin/python3 SyncUserUnion.py &
echo "Restart sync user unionid!"

