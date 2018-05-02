#!/usr/bin/env python
# -*- coding:utf-8 -*-
# 用来接收排行信息
from django.http import HttpResponse
import json
import arrow


def receive_invite_rank(request):
    """
    接收邀请排行数据
    :param request:
    :return:
    """
    t_date = arrow.now().format('YYYY-MM-DD')
    result = request.POST.get(t_date)
    if result:
        print(result)
        print(type(result))


def main():
    pass


if __name__ == "__main__":
    main()
    