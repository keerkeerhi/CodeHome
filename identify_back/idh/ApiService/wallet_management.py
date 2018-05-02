#!/usr/bin/env python
# -*- coding:utf-8 -*-
# 钱包的相关操作
from django.http import HttpResponse
import json
from UserManagement.models import *


def query_point_record(request):
    """
    获取积分收入记录，包括分页。
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
    start = index * num
    end = (index + 1) * num
    prs = PointRecord.objects.filter(user=up.user).order_by("-c_time")
    if not prs.exists() or len(prs) <= start:
        return HttpResponse(json.dumps({
            "code": 0, "msg": "ok", "data": result
        }))
    for pr in prs[start: end]:
        result.append({
            "name": pr.task.name, "c_time": pr.c_time.strftime("%Y-%m-%d %H:%M:%S"), "point": pr.point * up.times
        })

    return HttpResponse(json.dumps({
        "code": 0, "msg": "ok", "data": result
    }))


def main():
    pass


if __name__ == "__main__":
    main()
    