from django.contrib import admin
from UserManagement.models import *
from django.contrib.auth.admin import UserAdmin
from django.utils.safestring import mark_safe
from django.contrib import messages


class WxConfigAdmin(admin.ModelAdmin):
    """
    微信配置
    """
    list_display = ("id", "app_id", "app_secret", "t_type")


class ProfileInline(admin.StackedInline):
    model = UserProfile
    max_num = 1
    can_delete = False


class UserProfileAdmin(UserAdmin):
    """
    用户信息
    """
    list_display = (
        "id", "get_openid", "get_unionid", "get_c_time", "get_nickname", "get_sex", "get_avatar", "get_address",
        "get_language", "get_share_code", "get_invite", "get_balance", "get_rank", "get_base", "get_times",
        "get_is_phone", "get_phone", "get_is_email", "get_is_real_name", "get_is_face", "get_is_wx_run",
        "get_is_mp"
    )
    inlines = [ProfileInline, ]
    search_fields = (
        "id", "userprofile__openid", "userprofile__share_code", "userprofile__phone", "userprofile__nickname",
        "username", "userprofile__invite_code"
    )
    list_filter = (
        "is_active", "userprofile__sex", "userprofile__is_phone", "userprofile__is_email",
        "userprofile__is_real_name", "userprofile__is_face", "userprofile__is_mp", "userprofile__is_wx_run"
    )
    ordering = ("-userprofile__balance", )
    date_hierarchy = "userprofile__c_time"
    empty_value_display = "-"
    list_display_links = ("id", "get_openid", "get_nickname")

    # 获取用户openID
    def get_openid(self, obj):
        # return mark_safe('<a href="/admin/auth/user/%s/">%s</a>' % (obj.id, obj.userprofile.openid[:4]))
        return obj.userprofile.openid[:4]
    get_openid.short_description = u"用户标识"
    get_openid.allow_tags = True

    # 获取用户openID
    def get_unionid(self, obj):
        # return mark_safe('<a href="/admin/auth/user/%s/">%s</a>' % (obj.id, obj.userprofile.openid[:4]))
        return obj.userprofile.unionid[:4]
    get_unionid.short_description = u"全局标识"
    get_unionid.allow_tags = True

    # 获取会话密匙
    def get_session_key(self, obj):
        return obj.userprofile.session_key
    get_session_key.short_description = u"会话密钥"
    get_session_key.allow_tags = True

    # 获取用户昵称
    def get_nickname(self, obj):
        return obj.userprofile.nickname
    get_nickname.short_description = u"昵称"
    get_nickname.allow_tags = True

    # 获取性别
    def get_sex(self, obj):
        sex = obj.userprofile.sex
        if sex == 0:
            sex = u"未知"
        elif sex == 1:
            sex = u"男"
        else:
            sex = u"女"
        return sex
    get_sex.short_description = u"性别"
    get_sex.allow_tags = True

    # 获取用户头像
    def get_avatar(self, obj):
        return mark_safe('<img src="%s" alt="%s" width="60" style="border-radius:30px"/>' % (obj.userprofile.avatar, obj.userprofile.nickname))
    get_avatar.short_description = u"头像"
    get_avatar.allow_tags = True

    # 获取地理未知
    def get_address(self, obj):
        return "%s-%s-%s" % (obj.userprofile.country, obj.userprofile.province, obj.userprofile.city)
    get_address.short_description = u"所在城市"
    get_address.allow_tags = True

    # 获取语言
    def get_language(self, obj):
        return obj.userprofile.language
    get_language.short_description = u"语言"
    get_language.allow_tags = True

    # 获取邀请码
    def get_share_code(self, obj):
        return obj.userprofile.share_code
    get_share_code.short_description = u"邀请码"
    get_share_code.allow_tags = True

    # 获取邀请人信息
    def get_invite(self, obj):
        invite_code = obj.userprofile.invite_code
        if not invite_code:
            return "-"
        else:
            # 超找对应的邀请人
            ups = UserProfile.objects.filter(share_code=invite_code)
            if ups.exists():
                up = ups[0]
                return mark_safe('<a href="/admin/auth/user/%s/">%s</a>' % (up.user.id, up.user.userprofile.nickname))
            else:
                return invite_code
    get_invite.short_description = u"邀请人"
    get_invite.allow_tags = True

    # 获取积分
    def get_balance(self, obj):
        return obj.userprofile.balance
    get_balance.short_description = u"积分"
    get_balance.allow_tags = True

    # 获取积分排行
    def get_rank(self, obj):
        return obj.userprofile.rank
    get_rank.short_description = u"排行"
    get_rank.allow_tags = True

    # 获取基础积分
    def get_base(self, obj):
        return obj.userprofile.base
    get_base.short_description = u"基础积分"
    get_base.allow_tags = True

    # 获取积分倍数
    def get_times(self, obj):
        return obj.userprofile.times
    get_times.short_description = u"积分倍数"
    get_times.allow_tags = True

    # 查询手机号码
    def get_phone(self, obj):
        return obj.userprofile.phone
    get_phone.short_description = u"手机号码"
    get_phone.allow_tags = True

    # 公共函数-显示对号还是叉号
    @staticmethod
    def ck(is_ck):
        if is_ck:
            return mark_safe('<img src="/static/admin/img/icon-yes.svg" />')
        else:
            return mark_safe('<img src="/static/admin/img/icon-no.svg" />')

    # 获取是否认证手机号码
    def get_is_phone(self, obj):
        return self.ck(obj.userprofile.is_phone)
    get_is_phone.short_description = u"手机认证"
    get_is_phone.allow_tags = True

    # 获取是否邮箱认证
    def get_is_email(self, obj):
        return self.ck(obj.userprofile.is_email)
    get_is_email.short_description = u"邮件认证"
    get_is_email.allow_tags = True

    # 获取是否实名认证
    def get_is_real_name(self, obj):
        return self.ck(obj.userprofile.is_real_name)
    get_is_real_name.short_description = u"实名认证"
    get_is_real_name.allow_tags = True

    # 获取是否人脸认证
    def get_is_face(self, obj):
        return self.ck(obj.userprofile.is_face)
    get_is_face.short_description = u"人脸认证"
    get_is_face.allow_tags = True

    # 获取微信授权
    def get_is_wx_run(self, obj):
        return self.ck(obj.userprofile.is_wx_run)
    get_is_wx_run.short_description = u"微信运动"
    get_is_wx_run.allow_tags = True

    # 获取是否公众号关联
    def get_is_mp(self, obj):
        return self.ck(obj.userprofile.is_wx_run)
    get_is_mp.short_description = u"关联公众号"
    get_is_mp.allow_tags = True

    # 获取创建时间
    def get_c_time(self, obj):
        return obj.userprofile.c_time
    get_c_time.short_description = u"注册时间"
    get_c_time.allow_tags = True


class TaskInfoAdmin(admin.ModelAdmin):
    """
    任务活动基础信息
    """
    list_display = ("id", "tf", "name", "point", "is_multi")
    search_fields = ("id", "tf", "name")
    list_filter = ("is_multi", )
    ordering = ("id", "name")


class StatisticalDataAdmin(admin.ModelAdmin):
    """
    数据统计
    """
    list_display = ("id", "p_num", "balance", "update_time")


class SignRecordAdmin(admin.ModelAdmin):
    """
    每日签到记录
    """
    list_display = ("id", "get_user", "c_time")
    search_fields = ("id", "user__userprofile__nickname", "user__userprofile__openid")
    ordering = ("-c_time", )
    list_display_links = ("get_user", )

    # 获取用户
    def get_user(self, obj):
        return obj.user.userprofile.nickname
    get_user.short_description = u"签到用户"
    get_user.allow_tags = True


class PointRecordAdmin(admin.ModelAdmin):
    """
    积分增加记录
    """
    list_display = ("id", "c_time", "get_user", "task", "point")
    search_fields = ("id", "user__userprofile__nickname", "user__userprofile__openid")
    list_filter = ("task", )
    ordering = ("-c_time", )
    list_display_links = ("get_user", )

    # 获取用户
    def get_user(self, obj):
        # return mark_safe('<a href="/admin/auth/user/%s/">%s</a>' % (obj.user.id, obj.user.userprofile.nickname))
        return obj.user.userprofile.nickname
    get_user.short_description = u"签到用户"
    get_user.allow_tags = True


class WxRunRecordAdmin(admin.ModelAdmin):
    """
    微信运动步数
    """
    list_display = ("id", "get_user", "c_time", "c_date", "step")
    search_fields = ("id", "user__userprofile__nickname", "user__userprofile__openid")
    ordering = ("-c_date", "-c_time")
    list_display_links = ("get_user", )

    # 获取用户
    def get_user(self, obj):
        return obj.user.userprofile.nickname
    get_user.short_description = u"微信用户"
    get_user.allow_tags = True


@admin.register(UploadFile)
class UploadFileAdmin(admin.ModelAdmin):
    """
    上传文件信息
    """
    list_display = ("id", "c_time", "user", "name", "get_path", "is_delete")
    search_fields = ("id", "user__userprofile__nickname", "name")
    ordering = ("-c_time", )
    date_hierarchy = "c_time"
    list_filter = ("is_delete", )

    def get_path(self, obj):
        return mark_safe('<img src="%s" alt="%s" width="60" style="border-radius:30px"/>' % (obj.path, obj.name))
    get_path.short_description = u"上传图片"
    get_path.allow_tags = True


class UploadFileInline(admin.TabularInline):
    model = EyeImage.ufs.through


@admin.register(EyeImage)
class EyeImageAdmin(admin.ModelAdmin):
    """
    眼底片审核
    """
    list_display = ("id", "c_time", "get_nickname", "get_avatar", "status", "get_ufs")
    list_filter = ("status", )
    inlines = [UploadFileInline, ]
    search_fields = ("id", "user__userprofile__nickname")
    ordering = ("-c_time", )
    date_hierarchy = "c_time"
    actions = ["audit_pass", "audit_reject"]
    filter_horizontal = ["ufs", ]

    def get_avatar(self, obj):
        return mark_safe('<img src="%s" alt="%s" width="60" style="border-radius:30px"/>' % (
            obj.user.userprofile.avatar, obj.user.userprofile.nickname))
    get_avatar.short_description = u"头像"
    get_avatar.allow_tags = True

    def get_nickname(self, obj):
        return mark_safe('<a href="/admin/auth/user/%s/">%s</a>' % (obj.user.id, obj.user.userprofile.nickname))
    get_nickname.short_description = u"用户昵称"
    get_nickname.allow_tags = True

    def get_ufs(self, obj):
        """
        将审核需要的图片返回出来
        :param obj:
        :return:
        """
        html = ""
        for uf in obj.ufs.all():
            img = '<a href="%s" target="_blank"><img src="%s" width="60"/></a>' % (uf.path, uf.path)
            html += img
        return mark_safe(html)
    get_ufs.short_description = u"待审核图片"
    get_ufs.allow_tags = True

    def audit_pass(self, request, queryset):
        """
        审核通过
        :param request:
        :param queryset:
        :return:
        """
        for ei in queryset:
            if ei.status == "audit":
                # 执行审核操作
                ei.status = "success"
                ei.save()
                msg = "记录：%s 通过审核" % ei.id
                self.message_user(request, msg)
            else:
                # 不执行审核操作
                msg = "记录：%s 不需要审核，仅审核中的可以审核" % ei.id
                messages.add_message(request, messages.WARNING, msg)
    audit_pass.short_description = u"审核通过"

    def audit_reject(self, request, queryset):
        """
        审核不通过
        :param request:
        :param queryset:
        :return:
        """
        for ei in queryset:
            if ei.status == "audit":
                # 执行审核操作
                ei.status = "failed"
                ei.save()
                msg = "记录：%s 审核拒绝已经完成" % ei.id
                self.message_user(request, msg)
            else:
                # 不执行审核操作
                msg = "记录：%s 不需要审核，仅审核中的可以审核" % ei.id
                messages.add_message(request, messages.WARNING, msg)
    audit_reject.short_description = u"审核不通过"


@admin.register(WXToken)
class WXTokenAdmin(admin.ModelAdmin):
    """
    微信小程序和公众号AccessToken
    """
    list_display = ("id", "c_time", "token", "t_type")
    list_filter = ("t_type", )
    ordering = ("-c_time", )


@admin.register(WeChatSubscription)
class WeChatSubscriptionAdmin(admin.ModelAdmin):
    """
    公众号关注列表
    """
    list_display = (
        "id", "c_time", "openid", "unionid", "msg_type", "nickname", "sex", "get_avatar", "get_address",
        "language", "subscribe_scene", "s_time"
    )
    list_filter = ("msg_type", "sex", "subscribe_scene")
    search_fields = ("id", "openid", "unionid", "nickname")
    ordering = ("-c_time", )
    date_hierarchy = "c_time"
    list_display_links = ("id", "openid", "unionid")

    def get_avatar(self, obj):
        return mark_safe('<img src="%s" alt="%s" width="60" style="border-radius:30px"/>' % (
            obj.avatar, obj.nickname))
    get_avatar.short_description = u"头像"
    get_avatar.allow_tags = True

    # 获取地理位置
    def get_address(self, obj):
        return "%s-%s-%s" % (obj.country, obj.province, obj.city)
    get_address.short_description = u"所在城市"
    get_address.allow_tags = True


@admin.register(InviteRank)
class InviteRankAdmin(admin.ModelAdmin):
    """
    邀请人数排行榜
    """
    list_display = ("id", "c_date", "get_nickname", "get_phone", "get_avatar", "num", "rank")
    list_display_links = ("id", "c_date")
    date_hierarchy = "c_date"
    ordering = ("-c_date", "rank")
    actions = [
        "iv_1", "iv_2", "iv_3", "iv_4", "iv_7", "iv_10",
        "ip_10", "ip_20", "ip_30", "ip_40", "ip_50", "ip_60", "ip_70", "ip_80", "ip_90", "ip_100", "ip_110",
        "ip_120", "ip_130", "ip_140", "ip_150", "ip_160", "ip_170", "ip_180", "ip_190", "hg_15000"
    ]
    search_fields = ("user__userprofile__nickname", )

    def get_phone(self, obj):
        return obj.user.userprofile.phone
    get_phone.short_description = u"手机号码"
    get_phone.allow_tags = True

    def get_nickname(self, obj):
        return mark_safe('<a href="/admin/auth/user/%s/">%s</a>' % (obj.user.id, obj.user.userprofile.nickname))
    get_nickname.short_description = u"用户昵称"
    get_nickname.allow_tags = True

    def get_avatar(self, obj):
        return mark_safe('<img src="%s" alt="%s" width="60" style="border-radius:30px"/>' % (
            obj.user.userprofile.avatar, obj.user.userprofile.nickname))
    get_avatar.short_description = u"头像"
    get_avatar.allow_tags = True

    def send_point(self, user, tf):
        """
        因为活动赠送积分
        :param tf: 活动唯一标识
        :param user: 对象
        :return:
        """
        task = TaskInfo.objects.get(tf=tf)

        # 增加积分记录
        pr = PointRecord(user=user, task=task, point=task.point)
        pr.save()

        # 增加积分
        user.userprofile.base += task.point
        user.userprofile.balance = user.userprofile.base * user.userprofile.times
        user.userprofile.save()

    def iv_1(self, request, queryset):
        """
        赠送1000积分
        :return:
        """
        for qs in queryset:
            self.send_point(qs.user, "iv_1")
            self.message_user(request, "用户：%s赠送的1000积分已经到账" % qs.user.userprofile.nickname)
    iv_1.short_description = u"赠送1000积分"

    def iv_2(self, request, queryset):
        """
        赠送500积分
        :return:
        """
        for qs in queryset:
            self.send_point(qs.user, "iv_2")
            self.message_user(request, "用户：%s赠送的500积分已经到账" % qs.user.userprofile.nickname)
    iv_2.short_description = u"赠送500积分"

    def iv_3(self, request, queryset):
        """
        赠送300积分
        :return:
        """
        for qs in queryset:
            self.send_point(qs.user, "iv_3")
            self.message_user(request, "用户：%s赠送的300积分已经到账" % qs.user.userprofile.nickname)
    iv_3.short_description = u"赠送300积分"

    def iv_4(self, request, queryset):
        """
        赠送400积分
        :return:
        """
        for qs in queryset:
            self.send_point(qs.user, "iv_4")
            self.message_user(request, "用户：%s赠送的400积分已经到账" % qs.user.userprofile.nickname)
    iv_4.short_description = u"赠送400积分"

    def iv_7(self, request, queryset):
        """
        赠送300积分
        :return:
        """
        for qs in queryset:
            self.send_point(qs.user, "iv_7")
            self.message_user(request, "用户：%s赠送的200积分已经到账" % qs.user.userprofile.nickname)
    iv_7.short_description = u"赠送200积分"

    def iv_10(self, request, queryset):
        """
        赠送300积分
        :return:
        """
        for qs in queryset:
            self.send_point(qs.user, "iv_10")
            self.message_user(request, "用户：%s赠送的100积分已经到账" % qs.user.userprofile.nickname)
    iv_10.short_description = u"赠送100积分"

    def ip_10(self, request, queryset):
        """
        赠送300积分
        :return:
        """
        for qs in queryset:
            self.send_point(qs.user, "ip_10")
            self.message_user(request, "用户：%s赠送的10积分已经到账" % qs.user.userprofile.nickname)
    ip_10.short_description = u"单人邀请赠送10积分"

    def ip_20(self, request, queryset):
        """
        赠送300积分
        :return:
        """
        for qs in queryset:
            self.send_point(qs.user, "ip_20")
            self.message_user(request, "用户：%s赠送的20积分已经到账" % qs.user.userprofile.nickname)
    ip_20.short_description = u"单人邀请赠送20积分"

    def ip_30(self, request, queryset):
        """
        赠送300积分
        :return:
        """
        for qs in queryset:
            self.send_point(qs.user, "ip_30")
            self.message_user(request, "用户：%s赠送的30积分已经到账" % qs.user.userprofile.nickname)
    ip_30.short_description = u"单人邀请赠送30积分"

    def ip_40(self, request, queryset):
        """
        赠送300积分
        :return:
        """
        for qs in queryset:
            self.send_point(qs.user, "ip_40")
            self.message_user(request, "用户：%s赠送的40积分已经到账" % qs.user.userprofile.nickname)
    ip_40.short_description = u"单人邀请赠送40积分"

    def ip_50(self, request, queryset):
        """
        赠送300积分
        :return:
        """
        for qs in queryset:
            self.send_point(qs.user, "ip_50")
            self.message_user(request, "用户：%s赠送的50积分已经到账" % qs.user.userprofile.nickname)
    ip_50.short_description = u"单人邀请赠送50积分"

    def ip_60(self, request, queryset):
        """
        赠送300积分
        :return:
        """
        for qs in queryset:
            self.send_point(qs.user, "ip_60")
            self.message_user(request, "用户：%s赠送的60积分已经到账" % qs.user.userprofile.nickname)
    ip_60.short_description = u"单人邀请赠送60积分"

    def ip_70(self, request, queryset):
        """
        赠送300积分
        :return:
        """
        for qs in queryset:
            self.send_point(qs.user, "ip_70")
            self.message_user(request, "用户：%s赠送的70积分已经到账" % qs.user.userprofile.nickname)
    ip_70.short_description = u"单人邀请赠送70积分"

    def ip_80(self, request, queryset):
        """
        赠送300积分
        :return:
        """
        for qs in queryset:
            self.send_point(qs.user, "ip_80")
            self.message_user(request, "用户：%s赠送的80积分已经到账" % qs.user.userprofile.nickname)
    ip_80.short_description = u"单人邀请赠送80积分"

    def ip_90(self, request, queryset):
        """
        赠送300积分
        :return:
        """
        for qs in queryset:
            self.send_point(qs.user, "ip_90")
            self.message_user(request, "用户：%s赠送的90积分已经到账" % qs.user.userprofile.nickname)
    ip_90.short_description = u"单人邀请赠送90积分"

    def ip_100(self, request, queryset):
        """
        赠送300积分
        :return:
        """
        for qs in queryset:
            self.send_point(qs.user, "ip_100")
            self.message_user(request, "用户：%s赠送的100积分已经到账" % qs.user.userprofile.nickname)
    ip_100.short_description = u"单人邀请赠送100积分"

    def ip_110(self, request, queryset):
        """
        赠送300积分
        :return:
        """
        for qs in queryset:
            self.send_point(qs.user, "ip_110")
            self.message_user(request, "用户：%s赠送的110积分已经到账" % qs.user.userprofile.nickname)
    ip_110.short_description = u"单人邀请赠送110积分"

    def ip_120(self, request, queryset):
        """
        赠送300积分
        :return:
        """
        for qs in queryset:
            self.send_point(qs.user, "ip_120")
            self.message_user(request, "用户：%s赠送的120积分已经到账" % qs.user.userprofile.nickname)
    ip_120.short_description = u"单人邀请赠送120积分"

    def ip_130(self, request, queryset):
        """
        赠送300积分
        :return:
        """
        for qs in queryset:
            self.send_point(qs.user, "ip_130")
            self.message_user(request, "用户：%s赠送的130积分已经到账" % qs.user.userprofile.nickname)
    ip_130.short_description = u"单人邀请赠送130积分"

    def ip_140(self, request, queryset):
        """
        赠送300积分
        :return:
        """
        for qs in queryset:
            self.send_point(qs.user, "ip_140")
            self.message_user(request, "用户：%s赠送的140积分已经到账" % qs.user.userprofile.nickname)
    ip_140.short_description = u"单人邀请赠送140积分"

    def ip_150(self, request, queryset):
        """
        赠送300积分
        :return:
        """
        for qs in queryset:
            self.send_point(qs.user, "ip_150")
            self.message_user(request, "用户：%s赠送的150积分已经到账" % qs.user.userprofile.nickname)
    ip_150.short_description = u"单人邀请赠送150积分"

    def ip_160(self, request, queryset):
        """
        赠送300积分
        :return:
        """
        for qs in queryset:
            self.send_point(qs.user, "ip_160")
            self.message_user(request, "用户：%s赠送的160积分已经到账" % qs.user.userprofile.nickname)
    ip_160.short_description = u"单人邀请赠送160积分"

    def ip_170(self, request, queryset):
        """
        赠送300积分
        :return:
        """
        for qs in queryset:
            self.send_point(qs.user, "ip_170")
            self.message_user(request, "用户：%s赠送的170积分已经到账" % qs.user.userprofile.nickname)
    ip_170.short_description = u"单人邀请赠送170积分"

    def ip_180(self, request, queryset):
        """
        赠送300积分
        :return:
        """
        for qs in queryset:
            self.send_point(qs.user, "ip_180")
            self.message_user(request, "用户：%s赠送的180积分已经到账" % qs.user.userprofile.nickname)
    ip_180.short_description = u"单人邀请赠送180积分"

    def ip_190(self, request, queryset):
        """
        赠送300积分
        :return:
        """
        for qs in queryset:
            self.send_point(qs.user, "ip_190")
            self.message_user(request, "用户：%s赠送的190积分已经到账" % qs.user.userprofile.nickname)
    ip_190.short_description = u"单人邀请赠送190积分"

    def hg_15000(self, request, queryset):
        """
        赠送300积分
        :return:
        """
        for qs in queryset:
            self.send_point(qs.user, "hg_15000")
            self.message_user(request, "用户：%s扣除积分15000" % qs.user.userprofile.nickname)
    hg_15000.short_description = u"扣除积分15000"


admin.site.unregister(User)
admin.site.register(User, UserProfileAdmin)
admin.site.register(WxConfig, WxConfigAdmin)
admin.site.register(TaskInfo, TaskInfoAdmin)
admin.site.register(StatisticalData, StatisticalDataAdmin)
admin.site.register(SignRecord, SignRecordAdmin)
admin.site.register(PointRecord, PointRecordAdmin)
admin.site.register(WxRunRecord, WxRunRecordAdmin)
