#!/usr/bin/env python
# -*- coding:utf-8 -*-
# 同步邀请人当日邀请排行榜
import os
import sys
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)
from django.core.wsgi import get_wsgi_application
os.environ['DJANGO_SETTINGS_MODULE'] = "IDH.settings"
application = get_wsgi_application()
from UserManagement.models import *
import arrow
import operator
import requests
import json


class SyncInviteRank(object):
    """
    统计当日邀请排行榜
    """
    def __init__(self, t_date=""):
        # 同步请求web邀请人数
        if not t_date:
            self.t_date = arrow.now().format("YYYY-MM-DD")
        else:
            self.t_date = t_date
        with open("/var/www/idhchain/IDH_WEB/static/invite_rank.json") as fp:
            data = json.loads(fp.read())

        self.ivs = data.get(self.t_date, {})
        print(self.ivs)

    def run(self):
        """
        程序主入口
        :param t_date: 指定日期，如果没有，就选当日
        :return:
        """
        # if not self.t_date:
        #     t_date = arrow.now().format("YYYY-MM-DD")
        # next_date = arrow.get(t_date).shift(days=1).format("YYYY-MM-DD")
        next_date = "%s 23:59:59" % self.t_date

        # 遍历统计
        print(self.t_date)
        print("Start to count!")
        ups = UserProfile.objects.all().order_by("-balance")
        result = {}
        n = 1
        for up in ups:
            # # 更新积分排行榜
            up.rank = n
            up.save()
            n += 1

            num = len(UserProfile.objects.filter(invite_code=up.share_code, c_time__range=[self.t_date, next_date]))
            # 添加web邀请人数
            if up.is_phone:
                num += self.ivs.get(up.phone, 0)
            result[up.user] = num
        print("Count done:%s" % len(result))

        # 保存或更新到数据库
        ranks = []
        rank = 1
        for user, num in sorted(result.items(), key=operator.itemgetter(1), reverse=True):
            if rank % 50 == 0:
                print("Now rank:%s" % rank)

            ivs = InviteRank.objects.filter(c_date=self.t_date, user=user)
            if ivs.exists():
                ivs.update(num=num, rank=rank)
            else:
                iv = InviteRank(c_date=self.t_date, user=user, num=num, rank=rank)
                ranks.append(iv)

            rank += 1

        print("Calc done!")
        # 批量添加到数据库
        if ranks:
            InviteRank.objects.bulk_create(ranks)
        print("Over!", arrow.now())


def main():
    try:
        t_date = sys.argv[1]
    except:
        t_date = ""

    # url = "http://ref.idhchain.com/query_invite_num_by_date/"
    sr = SyncInviteRank(t_date)
    sr.run()


if __name__ == "__main__":
    main()
    