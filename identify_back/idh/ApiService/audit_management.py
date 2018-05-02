#!/usr/bin/env python
# -*- coding:utf-8 -*-
from django.http import HttpResponse
import json
from UserManagement.models import *


def apply_audit(request):
    """
    请求审核
    :param request:
    :return:
    """
    # 获取上传数据
    openid = request.POST.get("openid")
    files = request.POST.get("files")
    if not all([openid, files]):
        return HttpResponse(json.dumps({
            "code": -1, "msg": "Parameter is empty!"
        }))

    # 验证参数有效性
    try:
        up = UserProfile.objects.get(openid=openid)
        # 检查是否可以提交审核
        audits = EyeImage.objects.filter(user=up.user, status__in=["audit", "success"])
        if audits.exists():
            return HttpResponse(json.dumps({
                "code": -3, "msg": "Only one audit can be apply!"
            }))

        # 解析需要审核文件id列表
        files = json.loads(files)
        ufs = []
        for f in files:
            uf = UploadFile.objects.get(id=int(f), user=up.user)
            ufs.append(uf)
        if not ufs or len(ufs) > 6:
            return HttpResponse(json.dumps({
                "code": -4, "msg": "files can not be empty!"
            }))
    except Exception as msg:
        return HttpResponse(json.dumps({
            "code": -2, "msg": "Error parameter! Msg:%s" % msg
        }))

    try:
        # 提交审核
        audit = EyeImage(user=up.user, status="audit")
        audit.save()
        for uf in ufs:
            audit.ufs.add(uf)
        audit.save()

        return HttpResponse(json.dumps({
            "code": 0, "msg": "ok"
        }))
    except Exception as msg:
        return HttpResponse(json.dumps({
            "code": -5, "msg": "Apply audit failed! Msg:%s" % msg
        }))


def main():
    pass


if __name__ == "__main__":
    main()
    