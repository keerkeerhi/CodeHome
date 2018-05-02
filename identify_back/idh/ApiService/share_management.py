#!/usr/bin/env python
# -*- coding:utf-8 -*-
# 关于邀请的相关操作
from django.http import HttpResponse
import json
import arrow
from UserManagement.models import *


def invite_rank(user, t_date):
    """
    查找用户指定日期的邀请排名
    :param user: 用户
    :param t_date: 日期
    :return:
    """
    ivs = InviteRank.objects.filter(user=user, c_date=t_date)
    if ivs.exists():
        iv = ivs[0]
        rank = iv.rank
    else:
        rank = 0

    return rank


def query_share_code(request):
    """
    获取用户的邀请码。
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
        now = arrow.now()
        n_date = now.format("YYYY-MM-DD")
        y_date = now.shift(days=-1).format("YYYY-MM-DD")
    except Exception as msg:
        return HttpResponse(json.dumps({
            "code": -2, "msg": "Error openid! Msg:%s" % msg
        }))

    return HttpResponse(json.dumps({
        "code": 0, "msg": "ok", "data": {
            "share_code": up.share_code, "times": up.times, "y_rank": invite_rank(up.user, y_date),
            "n_rank": invite_rank(up.user, n_date)
        }
    }))


def query_share_record(request):
    """
    获取邀请记录，分页
    :param request:
    :return:
    """
    # 获取传入参数
    openid = request.GET.get("openid")
    num = request.GET.get("num")
    index = request.GET.get("index")
    if not openid:
        return HttpResponse(json.dumps({
            "code": -1, "msg": "Parameter is emtpy!"
        }))

    # 校验参数有效性
    try:
        up = UserProfile.objects.get(openid=openid)
        if not num:
            num = 10
        if not index:
            index = 0
        num, index = [int(i) for i in [num, index]]
    except Exception as msg:
        return HttpResponse(json.dumps({
            "code": -2, "msg": "Error openid! Msg:%s" % msg
        }))

    # 获取记录
    result = []
    start = num * index
    end = num * (index + 1)
    ups = UserProfile.objects.filter(invite_code=up.share_code).order_by("-c_time")
    if not ups.exists() or len(ups) <= start:
        return HttpResponse(json.dumps({
            "code": 0, "msg": "ok", "data": result
        }))

    for up in ups[start: end]:
        result.append({
            "avatar": up.avatar, "nickname": up.nickname, "c_time": up.c_time.strftime("%Y-%m-%d %H:%M:%S")
        })

    return HttpResponse(json.dumps({
        "code": 0, "msg": "ok", "data": result
    }))


def main():
    pass


if __name__ == "__main__":
    main()
    