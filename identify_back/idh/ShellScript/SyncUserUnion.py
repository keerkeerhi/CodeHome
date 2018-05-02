#!/usr/bin/env python
# -*- coding:utf-8 -*-
# 同步小程序和公众号用户一致性，并增加积分
import os
import sys
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)
from django.core.wsgi import get_wsgi_application
os.environ['DJANGO_SETTINGS_MODULE'] = "IDH.settings"
application = get_wsgi_application()
from UserManagement.models import *
import time


class SyncUser(object):
    """
    同步小程序和公众号用户一致性，并增加积分
    """
    def __init__(self):
        pass

    def run(self):
        """
        程序主入口
        :return:
        """
        task = TaskInfo.objects.get(tf="sub_pg")
        while True:
            # 获取已经完成的任务记录
            prs = PointRecord.objects.filter(task=task)
            if not prs.exists():
                time.sleep(60)

            # 获取还没有匹配到的公众号关注记录
            subs = WeChatSubscription.objects.all().exclude(openid__in=prs.values("user__userprofile__openid"))
            if not subs.exists():
                time.sleep(60)

            # 执行同步
            for sub in subs:
                unionid = sub.unionid
                ups = UserProfile.objects.filter(unionid=unionid)
                if ups.exists():
                    up = ups[0]
                    task = TaskInfo.objects.get(tf="sub_pg")
                    prs = PointRecord.objects.filter(task=task, user=up.user)
                    if not prs.exists():
                        # 记录积分记录
                        pr = PointRecord(user=up.user, task=task, point=task.point)
                        pr.save()

                        # 增加积分
                        up.base += task.point
                        up.balance = up.base * up.times
                        up.save()

                        print("Sync user:%s sub record!" % up.user_id)


def main():
    su = SyncUser()
    su.run()


if __name__ == "__main__":
    main()
    