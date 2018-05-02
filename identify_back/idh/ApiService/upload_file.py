#!/usr/bin/env python
# -*- coding:utf-8 -*-
from django.http import HttpResponse
import json
from UserManagement.models import *
import os
import time


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = "/static/upload/eye_image"
ABS_OUT = os.path.join(BASE_DIR, OUT[1:])


def upload(request):
    """
    上传文件
    :param request:
    :return:
    """
    # 获取上传数据
    openid = request.POST.get("openid")
    image = request.FILES.get("image")
    if not all([openid, image]):
        return HttpResponse(json.dumps({
            "code": -1, "msg": "Parameter is empty!"
        }))

    # 验证参数有效性
    try:
        up = UserProfile.objects.get(openid=openid)
    except Exception as msg:
        return HttpResponse(json.dumps({
            "code": -2, "msg": "Error openid! Msg:%s" % msg
        }))

    try:
        # 存储文件
        file_name = "%s-%s.png" % (up.user.id, time.time() * 1000)
        web_path = os.path.join(OUT, file_name)
        abs_path = os.path.join(ABS_OUT, file_name)
        with open(abs_path, "wb") as fp:
            for chunk in image.chunks():
                fp.write(chunk)

        # 存储数据库记录
        uf = UploadFile(user=up.user, name=image.name, path=web_path)
        uf.save()
    except Exception as msg:
        return HttpResponse(json.dumps({
            "code": -3, "msg": "Upload filed! Msg:%s" % msg
        }))

    return HttpResponse(json.dumps({
        "code": 0, "msg": "ok", "data": {
            "id": uf.id
        }
    }))




def main():
    pass


if __name__ == "__main__":
    main()
    