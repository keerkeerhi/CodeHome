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


class SyncBalanceRank(object):
    """
    更新积分排名
    """
    def __init__(self):
        pass

    def run(self):
        """
        程序入口
        :return:
        """
        ups = UserProfile.objects.all().order_by("-balance")
        n = 1
        for up in ups:
            up.rank = n
            up.save()
            n += 1


def main():
    sb = SyncBalanceRank()
    sb.run()


if __name__ == "__main__":
    main()
    