#!/usr/bin/env python
# -*- coding:utf-8 -*-
# 关于积分的相关操作
from django.http import HttpResponse
from UserManagement.models import *
import json
import arrow


def query_balance(request):
    """
    获取用户剩余积分，包括全部人数和人均积分。
    :param request:
    :return:
    """
    sds = StatisticalData.objects.all()
    if sds.exists():
        sd = sds[0]
        p_num = sd.p_num
        avg_balance = float("%.2f" % (float(sd.balance) / p_num))
    else:
        p_num = avg_balance = 0

    # 获取传入参数
    openid = request.GET.get("openid")
    if not openid:
        return HttpResponse(json.dumps({
            "code": 0, "msg": "ok", "data": {
                "p_num": p_num, "avg_balance": avg_balance
            }
        }))

    # 校验参数有效性
    try:
        up = UserProfile.objects.get(openid=openid)
    except Exception as msg:
        return HttpResponse(json.dumps({
            "code": -2, "msg": "Error openid! Msg:%s" % msg
        }))

    return HttpResponse(json.dumps({
        "code": 0, "msg": "ok", "data": {
            "balance": up.balance, "p_num": p_num, "avg_balance": avg_balance
        }
    }))


def sign(request):
    """
    每日签到，每天仅能签到一次。
    :param request:
    :return:
    """
    # 获取传入参数
    openid = request.POST.get("openid")
    if not openid:
        return HttpResponse(json.dumps({
            "code": -1, "msg": "Parameter is emtpy!"
        }))

    # 校验参数有效性
    try:
        up = UserProfile.objects.get(openid=openid)
        t_date = arrow.now().format("YYYY-MM-DD")
        records = SignRecord.objects.filter(user=up.user, c_time__gte=t_date)
        if records.exists():
            return HttpResponse(json.dumps({
                "code": -2, "msg": "Only sign once!"
            }))
    except Exception as msg:
        return HttpResponse(json.dumps({
            "code": -3, "msg": "Error openid! Msg:%s" % msg
        }))

    # 增加签到记录和增加积分
    try:
        # 签到
        sr = SignRecord(user=up.user)
        sr.save()

        # 增加积分
        task = TaskInfo.objects.get(tf="sign")
        pr = PointRecord(user=up.user, task=task, point=task.point)
        pr.save()

        # 更新积分
        up.base += task.point
        up.balance = up.base * up.times
        up.save()

        # 更新统计
        sds = StatisticalData.objects.all()
        if sds.exists():
            sd = sds[0]
            sd.balance += up.balance
        else:
            num = len(UserProfile.objects.all())
            sd = StatisticalData(p_num=num, balance=up.balance, update_time=arrow.now())
            sd.save()
    except Exception as msg:
        return HttpResponse(json.dumps({
            "code": -4, "msg": "Record failed! Msg:%s" % msg
        }))

    return HttpResponse(json.dumps({
        "code": 0, "msg": "ok"
    }))


def main():
    pass


if __name__ == "__main__":
    main()
    