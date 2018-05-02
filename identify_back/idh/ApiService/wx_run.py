#!/usr/bin/env python
# -*- coding:utf-8 -*-
# 微信运动授权
from UserManagement.models import *
from django.http import HttpResponse
import json
import base64
import arrow
from Crypto.Cipher import AES


class WXBizDataCrypt(object):
    def __init__(self, app_id, session_key):
        self.appId = app_id
        self.sessionKey = session_key

    def decrypt(self, encrypted_data, iv):
        # base64 decode
        session_key = base64.b64decode(self.sessionKey)
        encrypted_data = base64.b64decode(encrypted_data)
        iv = base64.b64decode(iv)

        cipher = AES.new(session_key, AES.MODE_CBC, iv)

        decrypted = json.loads(self._unpad(cipher.decrypt(encrypted_data)))

        if decrypted['watermark']['appid'] != self.appId:
            raise Exception('Invalid Buffer')

        return decrypted

    def _unpad(self, s):
        return s[:-ord(s[len(s)-1:])]


def wx_run(request):
    """
    获取微信运动授权，并记录最近30天步数
    :param request:
    :return:
    """
    # 获取传入参数
    openid = request.POST.get("openid")
    encrypted_data = request.POST.get("encryptedData")
    iv = request.POST.get("iv")
    if not all([openid, encrypted_data, iv]):
        print(request.POST)
        print(request.GET)
        return HttpResponse(json.dumps({
            "code": -1, "msg": "Parameter is emtpy!"
        }))

    # 获取微信配置
    confs = WxConfig.objects.filter(t_type="pg")
    if not confs.exists():
        return HttpResponse(json.dumps({
            "code": -2, "msg": "WX conf is not exists!"
        }))
    conf = confs[0]
    app_id = conf.app_id

    # 校验参数有效性
    try:
        up = UserProfile.objects.get(openid=openid)
        task = TaskInfo.objects.get(tf="wx_run")
        if PointRecord.objects.filter(user=up.user, task=task).exists():
            return HttpResponse(json.dumps({
                "code": -3, "msg": "Only auth once!"
            }))
        if not up.session_key:
            return HttpResponse(json.dumps({
                "code": -3, "msg": "Error session key!"
            }))
    except Exception as msg:
        return HttpResponse(json.dumps({
            "code": -4, "msg": "Error openid! Msg:%s" % msg
        }))

    # 开始解密
    try:
        wc = WXBizDataCrypt(app_id, up.session_key)
        data = wc.decrypt(encrypted_data, iv)
        run_data = data.get("stepInfoList")
        if not run_data:
            return HttpResponse(json.dumps({
                "code": 0, "msg": "ok"
            }))

        # 保存微信运动步数
        user = up.user
        for one in run_data:
            t_date = arrow.get(one.get("timestamp")).format("YYYY-MM-DD")
            step = int(one.get("step", 0))
            if not WxRunRecord.objects.filter(user=user, c_date=t_date).exists():
                wr = WxRunRecord(user=user, c_date=t_date, step=step)
                wr.save()

        # 增加积分
        if not up.is_wx_run:
            up.base += task.point
            up.balance = up.base * up.times

            # 记录积分记录
            pr = PointRecord(user=user, task=task, point=task.point)
            pr.save()

        # 更新用户授权状态
        up.is_wx_run = True
        up.save()
    except Exception as msg:
        return HttpResponse(json.dumps({
            "code": -5, "msg": "Decrypt data failed! Msg:%s" % msg
        }))

    return HttpResponse(json.dumps({
        "code": 0, "msg": "ok"
    }))


def main():
    pass


if __name__ == "__main__":
    main()
    