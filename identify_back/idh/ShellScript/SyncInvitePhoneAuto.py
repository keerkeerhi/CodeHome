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
import requests
import time


URL = "http://ref.idhchain.com/query_invite_num/"
TOKEN = "v0ZnlqAE5uzqSqFpcMuOIP5TkBOBbMHl"


class AutoSync(object):
    """
    自动同步web端的邀请人数到小程序
    """
    def __init__(self):
        pass

    def sync(self, up):
        """
        同步指定用户倍数信息
        :param up: UserProfile对象
        :return:
        """
        try:
            # if up.phone:
            url = URL + "?token=%s&phone=%s" % (TOKEN, up.phone)
            r = requests.get(url)
            if r.status_code != 200:
                # print("1111111111111")
                return

            data = r.json()
            code = data.get("code")
            if code != 0:
                print(data.get("msg"))
                return

            num = int(data.get("num", 0))
            # else:
            #     num = 0
            # if num == 0:
            #     return

            # 更新用户信息
            invite_num = len(UserProfile.objects.filter(invite_code=up.share_code)) + num
            if invite_num < 3:
                times = 1
            elif invite_num < 6:
                times = 3
            elif invite_num < 9:
                times = 6
            else:
                times = 10

            # 更新用户积分
            up.times = times
            up.balance = up.base * times
            up.save()
            # print("Sync phone:%s times:%s num:%s balance:%s" % (up.phone, times, invite_num, up.balance))
        except Exception as msg:
            print(msg)

    def run(self):
        """
        程序主入口
        :return:
        """
        # while True:
        # 查询所有需要同步的用户，倍数上限是10，超过10的不再进行同步
        ups = UserProfile.objects.filter(is_phone=True, times__lt=10).order_by("id")
        if not ups.exists():
            # print("222222222222")
            # time.sleep(60 * 5)
            # continue
            return

        # 遍历进行同步
        for up in ups:
            # if up.nickname == "天天IDH客服":
            # print(up.nickname)
            self.sync(up)

        # time.sleep(60 * 5)
        import arrow
        print("Sync invite phone done!", arrow.now())


def main():
    auto = AutoSync()
    auto.run()


if __name__ == "__main__":
    main()
    