#!/usr/bin/env python
# -*- coding:utf-8 -*-
import os
import sys
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)
from django.core.wsgi import get_wsgi_application
os.environ['DJANGO_SETTINGS_MODULE'] = "IDH.settings"
application = get_wsgi_application()
from UserManagement.models import UserProfile


class SyncInvite(object):
    """
    从文件中同步所有人员的邀请数量
    最大倍数是10，超过的不再处理
    仅同步有手机号码的
    """
    def __init__(self, invite_record):
        self.invite_record = invite_record

    def run(self):
        """
        程序主入口
        :return:
        """
        # 读取记录
        records = {}
        with open(self.invite_record) as fp:
            data = fp.readlines()
        for line in data:
            phone, num = line.strip().split()
            records[phone] = int(num)
        print("Records len:%s" % len(records))

        # 更新数据
        n = 0
        ups = UserProfile.objects.filter(is_phone=True, times__lt=10)
        for up in ups:
            num = records.get(up.phone, 0)
            if not num:
                continue

            # 累加邀请次数，并计算出倍数
            invite_num = len(UserProfile.objects.filter(invite_code=up.share_code)) + num
            if invite_num < 3:
                    times = 1
            elif invite_num < 6:
                times = 3
            elif invite_num < 10:
                times = 6
            else:
                times = 10

            # 更新用户积分
            up.times = times
            up.balance = up.base * times
            up.save()
            n += 1
            print("Update user:%s times:%s base:%s balance:%s" % (up.phone, times, up.base, up.balance))

        print("Update num:%s" % n)


def main():
    invite_record = sys.argv[1]
    sync = SyncInvite(invite_record)
    sync.run()


if __name__ == "__main__":
    main()
    