from django.http import HttpResponse
from apiserver.models import *
from json_response import JsonResponse
import os
import json
import requests
import configparser
import logging

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def login(request):
    code = request.GET.get('code')
    nickName = request.GET.get('nickName')
    country = request.GET.get('country')

    cf = configparser.ConfigParser()
    cf.read(os.path.join(BASE_DIR, "wxapp.cnf"))
    app_id = cf.get('config','AppID')
    app_secret = cf.get('config', 'AppSecret')
    openid = ''
    try:
        # 调用微信接口
        # url = "https://api.weixin.qq.com/sns/jscode2session?appid=%s&secret=%s&js_code=%s&" \
        #       "grant_type=authorization_code" % (app_id, app_secret, code)
        # ret = requests.get(url)
        # data = json.loads(ret.text)
        #
        # # 获取返回值
        # openid = data.get("openid")
        # session_key = data.get("session_key")
        openid = '1'
        # session_key = 'ogjl35E-_XlppK5_TGof_8LLmaho'
        us = User.objects.filter(id=openid)
        print('========>>')
        if us.exists():
            u = us[0]
            u.nickName = nickName
            u.country = country
            # u.session_key = session_key
            u.save()
            print(2)
        else:
            User.objects.create(id=openid,nickName=nickName,country=country)
            print(3)

    except Exception as e:
        print(e)
        return JsonResponse({'error':'save error'})

    return JsonResponse({'openid':openid,'msg':'ok'})