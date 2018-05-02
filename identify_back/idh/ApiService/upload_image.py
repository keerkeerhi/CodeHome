#!/usr/bin/env python
# -*-coding:utf-8-*-
__author__ = 'YuXiaoWen'

# Name: 
# Description: 
# version: 1.0.0

from django.http import HttpResponse
import hashlib
import xml.etree.ElementTree as ET
import requests
import os
import os
import sys
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)
from django.core.wsgi import get_wsgi_application
os.environ['DJANGO_SETTINGS_MODULE'] = "IDH.settings"
application = get_wsgi_application()
from UserManagement.models import WXToken, WxConfig
import arrow
import json


def upload_image(image_path):
    wc = WxConfig.objects.get(t_type="pg")
    url = "https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=%s&secret=%s" % (
        wc.app_id, wc.app_secret
    )
    r = requests.get(url)
    data = r.json()
    token = data.get("access_token")
    print(token)
    payload_img={
        'access_token':token,
        'type':'image'
    }
    img_url='https://api.weixin.qq.com/cgi-bin/material/add_material'
    data ={'media':open(image_path,'rb')}
    r=requests.post(url=img_url,params=payload_img,files=data)
    dict =r.json()
    return dict

print(upload_image("/home/diana/erweima.jpg"))
