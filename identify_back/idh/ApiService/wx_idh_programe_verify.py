#!/usr/bin/env python
# -*- coding:utf-8 -*-
from django.http import HttpResponse
import hashlib
import xml.etree.ElementTree as ET
import requests
from UserManagement.models import WXToken, WxConfig
import arrow
import json


TOKEN = "jZaouCvzK3EjkCzTEQ5SSmRZdnszqBYi"
IMAGE = "z4GBKTOff-IB3mVnG3VWCsC629WODKB33xRJVZsY3epH5DRdgwaGYVPi3P6jODe3"


def wx_verify(request):
    """
    提供微信公众号服务器验证
    :param request:
    :return:
    """
    signature = request.GET.get("signature")
    echostr = request.GET.get("echostr")
    timestamp = request.GET.get("timestamp")
    nonce = request.GET.get("nonce")

    rl = [TOKEN, timestamp, nonce]
    rl.sort()
    rl2 = ''.join(rl)
    sha1 = hashlib.sha1()
    sha1.update(rl2.encode('utf-8'))
    hashcode = sha1.hexdigest()

    if hashcode == signature:
        return HttpResponse(echostr)
    else:
        return HttpResponse("error")


def query_access_token(t_type="pg"):
    """
    获取小程序或公众号access token
    两个小时有效
    :param t_type: pg表示小程序，pb表示公众号
    :return:
    """
    c_time = arrow.now().shift(hours=-1).format("YYYY-MM-DD HH:mm:ss")
    ats = WXToken.objects.filter(c_time__gt=c_time, t_type=t_type).order_by("-c_time")
    if ats.exists():
        at = ats[0]
        return at.token
    else:
        # 没有或者已经过去，重新生成一个
        if t_type == "pg":
            wc = WxConfig.objects.get(t_type="pg")
        else:
            wc = WxConfig.objects.get(t_type="pb")

        # 获取access token
        url = "https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=%s&secret=%s" % (
            wc.app_id, wc.app_secret
        )
        r = requests.get(url)
        data = r.json()
        token = data.get("access_token")
        wt = WXToken(token=token, t_type=t_type)
        wt.save()

        return token


def notice(openid, m_type):
    """
    发送客服消息
    :param openid: 用户openid
    :param m_type: txt表示文本，image表示图片
    :return:
    """
    # token = query_access_token("pg")
    # print(token)
    wc = WxConfig.objects.get(t_type="pg")
    url = "https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=%s&secret=%s" % (
        wc.app_id, wc.app_secret
    )
    r = requests.get(url)
    data = r.json()
    token = data.get("access_token")
    url = "https://api.weixin.qq.com/cgi-bin/message/custom/send?access_token=%s" % token
    if m_type == "image":
        data = {
            "touser": openid,
            "msgtype": "link",
            "link": {
                "title": "关注公众号任务",
                "description": "小手一抖，50积分到手~",
                "url": "http://mp.weixin.qq.com/s/4NTDMTJA1t38TvysPABIrA",
                "thumb_url": "https://wx.alpha-brick.com/static/img/sub.jpg"
            }
        }
    else:
        data = {
            "touser": openid,
            "msgtype": "link",
            "link": {
                "title": "关注公众号任务",
                "description": "小手一抖，50积分到手~",
                "url": "http://mp.weixin.qq.com/s/4NTDMTJA1t38TvysPABIrA",
                "thumb_url": "https://wx.alpha-brick.com/static/img/sub.jpg"
            }
        }
        # data = {
        #     "touser": openid,
        #     "msgtype": "text",
        #     "text":
        #         {
        #             "content": "您的消息我们已经收到，客服会尽快回复您。您也可以添加客服微信号: IDH_Chain"
        #         }
        # }
    requests.post(url, data=json.dumps(data, ensure_ascii=False).encode("utf-8"))


def wx_notice(request):
    """
    微信客服消息通知
    :param request:
    :return:
    """
    xml_str = request.body
    xml = ET.fromstring(xml_str)
    msg_type = xml.find("MsgType").text
    openid = xml.find("FromUserName").text
    if msg_type == "event":
        event = xml.find("Event").text
        if event == "user_enter_tempsession":
            to_user_name = xml.find("ToUserName").text
            session = xml.find("SessionFrom").text
            notice(openid, "image")
        else:
            notice(openid, "txt")
    else:
        notice(openid, "txt")
    return HttpResponse("")


def idh_message(request):
    """
    负责验证小程序消息通知和接口
    :param request:
    :return:
    """
    if request.method == "GET":
        return wx_verify(request)
    elif request.method == "POST":
        return wx_notice(request)
    else:
        pass


def main():
    pass


if __name__ == "__main__":
    main()
    