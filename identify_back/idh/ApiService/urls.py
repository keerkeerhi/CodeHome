#!/usr/bin/env python
# -*- coding:utf-8 -*-
from django.urls import path
from ApiService.login import login
from ApiService.update_user_info import update
from ApiService import point_management, share_management, wallet_management
from ApiService.wx_run import wx_run
from ApiService.query_status import auth_status, sign_status
from ApiService.wx_phone import wx_phone
from ApiService.mp_verify import mp
from ApiService.upload_file import upload
from ApiService.audit_management import apply_audit
from ApiService.wx_idh_programe_verify import idh_message
from ApiService.rank_list import rank_by_balance
from ApiService.sync_invite_rank import receive_invite_rank

urlpatterns = [
    # 微信公众号设置
    path("mp/", mp),

    # 同步邀请排行
    path("receive_invite_rank/", receive_invite_rank),

    path("login/", login),
    path("update/", update),
    path("query_balance/", point_management.query_balance),
    path("sign/", point_management.sign),
    path("query_share_code/", share_management.query_share_code),
    path("query_share_record/", share_management.query_share_record),
    path("query_point_record/", wallet_management.query_point_record),
    path("wx_run/", wx_run),
    path("auth_status/", auth_status),
    path("wx_phone/", wx_phone),
    path("sign_status/", sign_status),
    path("upload/", upload),
    path("apply_audit/", apply_audit),
    path("idh_message/", idh_message),
    path("rank_by_balance/", rank_by_balance),
]
