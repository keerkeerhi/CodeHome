#!/usr/bin/env python
# -*- coding:utf-8 -*-
from django.http import HttpResponse
import hashlib
import xml.etree.ElementTree as ET
from UserManagement.models import WxConfig, WXToken, UserProfile, WeChatSubscription
import requests
import arrow
import time


TOKEN = "9O8NtIou2nCTVMzAoAUR2BXkX8EQivta"


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


def query_user_info(openid):
    """
    获取公众号关注用户的基本信息
    :param openid: 微信openid
    :return:
    """
    # 获取access token
    wc = WxConfig.objects.get(t_type="pb")
    url = "https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=%s&secret=%s" % (
        wc.app_id, wc.app_secret
    )
    r = requests.get(url)
    data = r.json()
    token = data.get("access_token")

    # 获取user info
    url = "https://api.weixin.qq.com/cgi-bin/user/info?access_token=%s&openid=%s&lang=zh_CN" % (token, openid)
    r = requests.get(url)
    infos = r.json()

    return infos


def notice_deal(request):
    """
    处理微信推送消息处理，目前仅处理扫描带参数的二维码关注事件
    :param request:
    :return:
    """
    xml_str = request.body
    xml = ET.fromstring(xml_str)
    msg_type = xml.find("MsgType").text
    openid = xml.find("FromUserName").text
    from_user = xml.find("ToUserName").text
    try:
        if not WeChatSubscription.objects.filter(openid=openid).exists():
            # 更新用户信息
            infos = query_user_info(openid)
            if not infos.get("subscribe"):
                with open("/var/www/idh/log/mp.log", "a") as fp:
                    fp.write(
                        "%s\t%s is not subscribe!\n" % (arrow.now().format("YYYY-MM-DD HH:mm:ss"), openid)
                    )
                return HttpResponse("")

            # 保存公众号关注信息
            ws = WeChatSubscription(
                openid=openid, unionid=infos.get("unionid"), msg_type=msg_type,
                sex=infos.get("sex"), avatar=infos.get("headimgurl"), country=infos.get("country"),
                province=infos.get("province"), city=infos.get("city"), language=infos.get("language"),
                subscribe_scene=infos.get("subscribe_scene"),
                s_time=arrow.get(infos.get("subscribe_time")).format("YYYY-MM-DD HH:mm:ss")
            )
            ws.save()
            try:
                ws.nickname = infos.get("nickname")
                ws.save()
            except Exception as msg:
                ws.nickname = "-"
                ws.save()
                with open("/var/www/idh/log/mp.log", "a") as fp:
                    fp.write(
                        "%s\tWeChat PB %s ERROR! MSG:%s\n" % (arrow.now().format("YYYY-MM-DD HH:mm:ss"), openid, msg)
                    )
            reply = """<xml>
                <ToUserName>%s</ToUserName>
                <FromUserName>%s</FromUserName>
                <CreateTime>%s</CreateTime>
                <MsgType>news</MsgType>
                <ArticleCount>3</ArticleCount>
                    <Articles>
                        <item>
                            <Title>IDH小程序 | ALL IN 你准备好了吗？</Title> 
                            <Description>AI+区块链，一起ALL IN！</Description>
                            <PicUrl>https://wx.alpha-brick.com/static/img/1.jpg</PicUrl>
                            <Url>https://mp.weixin.qq.com/s/glmxH6XHR-yhk5p-yojo2w</Url>
                        </item>
                        <item>
                            <Title>IDH客服 | 进门右转关注小姐姐</Title>
                            <Description>来都来了，不加下小姐姐入群领个分儿？</Description>
                            <PicUrl>https://wx.alpha-brick.com/static/img/2.jpg</PicUrl>
                            <Url>https://mp.weixin.qq.com/s/ZnUNM-3F2twruO_nbEWiCA</Url>
                        </item>
                        <item>
                            <Title>IDH官网 | 人工智能医疗能否玩转区块链？</Title>
                            <Description>IDH官网及介绍</Description>
                            <PicUrl>https://wx.alpha-brick.com/static/img/3.jpg</PicUrl>
                            <Url>https://mp.weixin.qq.com/s/tMP171hGqOJLBXD8zbSLEw</Url>
                        </item>
                    </Articles>
                </xml>""" % (openid, from_user, int(time.time()))
        else:
            image = "8sBmFiZn0gJQTBQDNxCgzhmVaxQVePyJdUjVqQOE1gg"
            reply = """<xml>
                <ToUserName>%s</ToUserName>
                <FromUserName>%s</FromUserName>
                <CreateTime>%s</CreateTime>
                <MsgType>image</MsgType>
                <Image>
                    <MediaId>%s</MediaId>
                </Image>
            </xml>""" % (openid, from_user, int(time.time()), image)
        return HttpResponse(reply)
    except Exception as msg:
        with open("/var/www/idh/log/mp.log", "a") as fp:
            fp.write(
                "%s\tWeChat PB %s ERROR! MSG:%s\n" % (arrow.now().format("YYYY-MM-DD HH:mm:ss"), openid, msg)
            )
        print("WeChat PB ERROR! MSG:%s" % msg, xml)
        return HttpResponse("")


def mp(request):
    """
    在访问方式是GET时，提供微信公众号服务器验证
    在访问方式是POST时，目前仅提供关注事件的处理
    :param request:
    :return:
    """
    if request.method == "GET":
        return wx_verify(request)
    elif request.method == "POST":
        return notice_deal(request)
    else:
        pass


def main():
    pass


if __name__ == "__main__":
    main()
    