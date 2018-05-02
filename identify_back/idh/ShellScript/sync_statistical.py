#!/usr/bin/env python
# -*- coding:utf-8 -*-
# 同步统计信息，包括：当前全部用户数量、当前总积分数
import os
import sys
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)
from django.core.wsgi import get_wsgi_application
os.environ['DJANGO_SETTINGS_MODULE'] = "IDH.settings"
application = get_wsgi_application()
import datetime
from UserManagement.models import UserProfile, StatisticalData
from django.db.models import Sum
import time


class SyncStatistical(object):
    """
    同步当前用户数量、当前总积分数
    """
    def __init__(self):
        pass

    def run(self):
        """
        程序主入口。
        :return:
        """
        # 获取最新数据
        p_num = len(UserProfile.objects.all())
        balance = UserProfile.objects.all().aggregate(Sum("balance")).get("balance__sum", 0)

        # 更新或创建
        sds = StatisticalData.objects.all()
        if sds.exists():
            sd = sds[0]
            sd.p_num = p_num
            sd.balance = balance
            sd.save()
        else:
            sd = StatisticalData(p_num=p_num, balance=balance, update_time=datetime.datetime.now())
            sd.save()
        print("Update complete! num:%s balance:%s" % (p_num, balance))


def main():
    sync = SyncStatistical()
    # while True:
    sync.run()
        # time.sleep(60)


if __name__ == "__main__":
    main()
    