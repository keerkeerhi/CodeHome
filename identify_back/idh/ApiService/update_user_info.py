#!/usr/bin/env python
# -*- coding:utf-8 -*-
# 更新用户基本信息
from django.http import HttpResponse
import json
from UserManagement.models import *
from ApiService.wx_run import WXBizDataCrypt


def update(request):
    """
    更新用户信息
    :param request:
    :return:
    """
    # 获取传入参数
    openid = request.POST.get("openid")
    nickname = request.POST.get("nickname")
    sex = str(request.POST.get("sex"))
    avatar = request.POST.get("avatar")
    country = request.POST.get("country")
    province = request.POST.get("province")
    city = request.POST.get("city")
    language = request.POST.get("language")
    iv = request.POST.get("iv")
    encrypted_data = request.POST.get("encryptedData")
    if not all([openid, nickname, avatar, language]):
        return HttpResponse(json.dumps({
            "code": -1, "msg": "Parameter is empty!"
        }))

    # 验证参数有效性
    try:
        up = UserProfile.objects.get(openid=openid)
        sex = int(sex)
        if sex not in [0, 1, 2]:
            return HttpResponse(json.dumps({
                "code": -2, "msg": "Error sex!"
            }))
    except Exception as msg:
        return HttpResponse(json.dumps({
            "code": -3, "msg": "Error openid! Msg:%s" % msg
        }))

    # 执行更新操作
    try:
        try:
            up.nickname = nickname.replace("\\x", "")
            up.save()
        except:
            up.nickname = u"-"
        up.sex = sex
        up.avatar = avatar
        up.country = country
        up.province = province
        up.city = city
        up.language = language
        up.save()

        # 获取微信配置
        confs = WxConfig.objects.filter(t_type="pg")
        if not confs.exists():
            msg = "WX conf is not exists!"
            return HttpResponse(json.dumps({
                "code": -5, "msg": msg
            }))
        conf = confs[0]
        app_id = conf.app_id

        # 尝试更新用户unionid
        if iv and encrypted_data:
            wc = WXBizDataCrypt(app_id, up.session_key)
            data = wc.decrypt(encrypted_data, iv)
            up.unionid = data.get("unionId")
            up.save()
    except Exception as msg:
        with open("/var/www/idh/log/update.log", "a") as fp:
            fp.write("Update user failed! User:%s Msg:%s\n" % (up.user_id, msg))
        return HttpResponse(json.dumps({
            "code": -4, "msg": "Update failed! Msg:%s" % msg
        }))

    return HttpResponse(json.dumps({
        "code": 0, "msg": "ok"
    }))


def main():
    pass


if __name__ == "__main__":
    main()
    