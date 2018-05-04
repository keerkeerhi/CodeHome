from django.http import HttpResponse
from django.contrib.auth import authenticate,login,logout
from apiserver.models import *
from json_response import JsonResponse
import os
import json
import requests
import configparser
import logging
import datetime
import arrow

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def loginfun(request):
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
        url = "https://api.weixin.qq.com/sns/jscode2session?appid=%s&secret=%s&js_code=%s&" \
              "grant_type=authorization_code" % (app_id, app_secret, code)
        ret = requests.get(url)
        data = json.loads(ret.text)
        #
        # # 获取返回值
        openid = data.get("openid")
        # session_key = data.get("session_key")
        # session_key = 'ogjl35E-_XlppK5_TGof_8LLmaho'
        us2 = UserBase.objects.filter(uid=openid)
        if us2.exists():
            u = us2[0]
            u.nickName = nickName
            u.country = country
            u.loginTime = str(arrow.now().to('Asia/Shanghai').format("YYYY-MM-DD HH:mm:ss"))
            # u.session_key = session_key
            u.save()
        else:
            user = User.objects.create(username=openid,email=nickName)
            ub = UserBase(user=user,uid=openid, nickName=nickName, country=country)
            ub.save()

    except Exception as e:
        print(e)
        return JsonResponse({'error':'save error'})

    return JsonResponse({'code':0,'openid':openid,'msg':'ok','time':arrow.now().to('Asia/Shanghai').format("YYYY-MM-DD HH:mm:ss")})

def login_ses(request):
    return JsonResponse({'code':0})
    username = request.GET.get('username')
    password = request.GET.get('password')

    # 一般方法
    # ls = User.objects.filter(username=username)
    # if ls.exists():
    #     request.session['isLogin'] = True
    #     request.session['username'] = username
    # else:
    #     return JsonResponse({'code':-1})
    user = authenticate(username=username,password=password)
    if user is not None:
        login(request, user)
    else:
        return JsonResponse({'code': -1})
    return JsonResponse({'code':0,'msg':'ok'})

def login_out(request):
    # request.session['isLogin'] = False
    # request.session['username'] = None
    logout(request)
    return JsonResponse({'code':0})

def saveUser(request):
    print('-'*222)
    print(request.user.is_authenticated)
    if __is_login(request):
        return JsonResponse({'code':-1,'msg':'isLogined'})

    # return JsonResponse({'code':-1})
    dic = json.loads(request.body)
    username = dic.get('username')
    password = dic.get('password')

    if not all([username,password]):
        return JsonResponse({'code':-1})
    try:
        User.objects.create_user(username=username,password=password)
    except Exception as e:
        return JsonResponse({'code':-1})

    return JsonResponse({'code':0})

def __is_login(request):
    # return request.session.get('isLogin',False)
    return request.user.is_authenticated