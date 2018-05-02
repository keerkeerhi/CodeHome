#!/usr/bin/env python
# -*- coding:utf-8 -*-
# 按照积分多少进行排行
from django.http import HttpResponse
import json
from UserManagement.models import UserProfile


def rank_by_balance(request):
    """
    获取积分最多的top 10
    :param request:
    :return:
    """
    # 获取传入参数
    openid = request.GET.get("openid")
    if not openid:
        return HttpResponse(json.dumps({
            "code": -1, "msg": "Parameter is emtpy!"
        }))

    # 校验参数有效性
    try:
        up = UserProfile.objects.get(openid=openid)
        rank = up.rank
    except Exception as msg:
        return HttpResponse(json.dumps({
            "code": -2, "msg": "Error openid! Msg:%s" % msg
        }))

    ups = UserProfile.objects.all().order_by("-balance")
    result = []
    n = 1
    for up in ups:
        if n > 10:
            break
        result.append([n, up.nickname, up.avatar, up.balance])
        n += 1

    return HttpResponse(json.dumps({
        "code": 0, "msg": "ok", "data": result, "rank": rank
    }))


def main():
    pass


if __name__ == "__main__":
    main()
    