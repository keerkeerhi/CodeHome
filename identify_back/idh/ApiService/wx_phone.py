#!/usr/bin/env python
# -*- coding:utf-8 -*-
# 微信手机认证
from django.http import HttpResponse
import json
from UserManagement.models import *
from ApiService.wx_run import WXBizDataCrypt
import arrow


def log(openid, msg):
    """
    记录认证失败的信息
    :param openid: openid
    :param msg: 失败内容
    :return:
    """
    with open("/var/log/idh/wx_phone.log", "a") as fp:
        fp.write("%s\t%s\t%s\n" % (arrow.now().format("YYYY-MM-DD HH:mm:ss"), openid, msg))


def wx_phone(request):
    """
    进行微信手机认证。
    :param request:
    :return:
    """
    # 获取传入参数
    openid = request.POST.get("openid")
    encrypted_data = request.POST.get("encryptedData")
    iv = request.POST.get("iv")
    if not all([openid, encrypted_data, iv]):
        msg = "Parameter is emtpy!"
        log(openid, msg)
        return HttpResponse(json.dumps({
            "code": -1, "msg": msg
        }))

    # 获取微信配置
    confs = WxConfig.objects.filter(t_type="pg")
    if not confs.exists():
        msg = "WX conf is not exists!"
        log(openid, msg)
        return HttpResponse(json.dumps({
            "code": -2, "msg": msg
        }))
    conf = confs[0]
    app_id = conf.app_id

    # 校验参数有效性
    try:
        up = UserProfile.objects.get(openid=openid)
        task = TaskInfo.objects.get(tf="verify_phone")
        if PointRecord.objects.filter(user=up.user, task=task).exists():
            return HttpResponse(json.dumps({
                "code": -3, "msg": "Only auth phone once!"
            }))
        if up.is_phone:
            msg = "Only auth phone once!"
            log(openid, msg)
            return HttpResponse(json.dumps({
                "code": -3, "msg": msg
            }))
        if not up.session_key:
            msg = "Error session key!"
            log(openid, msg)
            return HttpResponse(json.dumps({
                "code": -4, "msg": msg
            }))
    except Exception as msg:
        msg = "Error openid! Msg:%s" % msg
        log(openid, msg)
        return HttpResponse(json.dumps({
            "code": -5, "msg": msg
        }))

    # 解析数据
    try:
        wc = WXBizDataCrypt(app_id, up.session_key)
        data = wc.decrypt(encrypted_data, iv)
        phone = data.get("phoneNumber")
        if not phone:
            msg = "User has not phone!"
            log(openid, msg)
            return HttpResponse(json.dumps({
                "code": -6, "msg": msg
            }))

        # 增加积分
        up.base += task.point
        up.balance = up.base * up.times
        up.is_phone = True
        up.phone = phone
        up.save()

        # 记录积分记录
        user = up.user
        pr = PointRecord(user=user, task=task, point=task.point)
        pr.save()
    except Exception as msg:
        msg = "Decrypt data failed! Msg:%s" % msg
        log(openid, msg)
        return HttpResponse(json.dumps({
            "code": -7, "msg": msg
        }))

    return HttpResponse(json.dumps({
        "code": 0, "msg": "ok"
    }))


def main():
    pass


if __name__ == "__main__":
    main()
    