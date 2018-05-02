#!/usr/bin/env python
# -*- coding:utf-8 -*-
import os
import sys
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)
from django.core.wsgi import get_wsgi_application
os.environ['DJANGO_SETTINGS_MODULE'] = "IDH.settings"
application = get_wsgi_application()
from UserManagement.models import *
from django.db.models import Sum
import arrow


class SyncBalance(object):
    """
    同步用户积分。根据交易记录。
    """
    def __init__(self):
        pass

    def sync(self):
        """
        程序主入口
        :return:
        """
        ups = UserProfile.objects.all()
        n = 0
        for up in ups:
            base = PointRecord.objects.filter(user=up.user).aggregate(balance=Sum("point")).get("balance")
            if not base:
                base = 0
            up.base = base
            up.balance = base * up.times
            up.save()

            if n % 100 == 0:
                print("Sync %s user!" % n)
            n += 1
            
        print(arrow.now())


def main():
    sb = SyncBalance()
    sb.sync()


if __name__ == "__main__":
    main()
    