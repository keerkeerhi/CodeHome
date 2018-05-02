#!/usr/bin/env python
# -*- coding:utf-8 -*-
from django.http import HttpResponse
import json
from UserManagement.models import *
import requests
import datetime


def login(request):
    """
    微信用户登录接口，使用code获取 session_key 和 openid
    根据openID选择创建或更新用户
    :param request:
    :return:
    """
    # 获取传入参数
    code = request.GET.get("code")
    invite = request.GET.get("invite")
    if not code:
        return HttpResponse(json.dumps({
            "code": -1, "msg": "Parameter is empty!"
        }))

    # 获取微信配置
    confs = WxConfig.objects.filter(t_type="pg")
    if not confs.exists():
        return HttpResponse(json.dumps({
            "code": -2, "msg": "WX conf is not exists!"
        }))
    conf = confs[0]
    app_id = conf.app_id
    app_secret = conf.app_secret

    try:
        # 调用微信接口
        url = "https://api.weixin.qq.com/sns/jscode2session?appid=%s&secret=%s&js_code=%s&" \
              "grant_type=authorization_code" % (app_id, app_secret, code)
        ret = requests.get(url)
        data = json.loads(ret.text)

        # 获取返回值
        openid = data.get("openid")
        session_key = data.get("session_key")
    except Exception as msg:
        print(msg)
        return HttpResponse(json.dumps({
            "code": -3, "msg": "Get openid failed!"
        }))

    # 检查是否需要创建用户
    users = UserProfile.objects.filter(openid=openid)
    if users.exists():
        # 用户已经存在
        up = users[0]
        if not all([up.nickname, up.avatar, up.unionid]):
            is_new = True
        else:
            is_new = False
        profile = users[0]
        profile.session_key = session_key
        profile.save()
    else:
        # 用户不存在，创建之
        is_new = True
        try:
            user = User.objects.create_user(username=openid, password=create_share_code(10), is_active=True)
            user.save()
            up = UserProfile(
                user=user, openid=openid, session_key=session_key
            )
            up.save()

            # 更新数据统计
            sds = StatisticalData.objects.all()
            if not sds.exists():
                num = len(UserProfile.objects.all())
                sd = StatisticalData(p_num=num, balance=0, update_time=datetime.datetime.now())
                sd.save()
            else:
                sd = sds[0]
                sd.p_num += 1
                sd.save()

            # 更新邀请人
            ivs = UserProfile.objects.filter(share_code=invite)
            if invite and ivs.exists():
                up.invite_code = invite
                up.save()

                # 计算此用户的倍数
                iv = ivs[0]
                num = len(UserProfile.objects.filter(invite_code=invite))
                if num < 3:
                    times = 1
                elif num < 6:
                    times = 3
                elif num < 10:
                    times = 6
                else:
                    times = 10

                iv.times = times
                iv.balance = iv.base * times
                iv.save()
        except Exception as msg:
            return HttpResponse(json.dumps({
                "code": -4, "msg": "Create user failed! Msg:%s" % msg
            }))

    return HttpResponse(json.dumps({
        "code": 0, "msg": "ok", "data": {
            "openid": openid, "is_new": is_new
        }
    }))


def main():
    pass


if __name__ == "__main__":
    main()
    