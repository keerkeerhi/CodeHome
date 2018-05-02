#!/usr/bin/env python
# -*- coding:utf-8 -*-
# 获取用户认证状态
from django.http import HttpResponse
import json
from UserManagement.models import *
import arrow


def auth_status(request):
    """
    获取用户各项信息的认证状态。
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
    except Exception as msg:
        return HttpResponse(json.dumps({
            "code": -2, "msg": "Error openid! Msg:%s" % msg
        }))

    return HttpResponse(json.dumps({
        "code": 0, "msg": "ok", "data": {
            "is_phone": up.is_phone, "is_email": up.is_email, "is_real_name": up.is_real_name, "is_face": up.is_face,
            "is_wx_run": up.is_wx_run
        }
    }))


def sign_status(request):
    """
    查询当日签到状态。
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
    except Exception as msg:
        return HttpResponse(json.dumps({
            "code": -2, "msg": "Error openid! Msg:%s" % msg
        }))

    # 查询签到状态
    t_date = arrow.now().format("YYYY-MM-DD")
    if SignRecord.objects.filter(user=up.user, c_time__gte=t_date).exists():
        is_sign = True
    else:
        is_sign = False

    return HttpResponse(json.dumps({
        "code": 0, "msg": "ok", "data": {
            "is_sign": is_sign
        }
    }))


def main():
    pass


if __name__ == "__main__":
    main()
    