# -*-coding:utf-8-*-
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
import string
import random


TOKEN_TYPE = (
    ("pb", u"公众号"),
    ("pg", u"小程序")
)


SEX = (
    (1, u"男"),
    (2, u"女"),
    (0, u"未知")
)


class WxConfig(models.Model):
    """
    微信基本信息配置。
    """
    app_id = models.CharField(max_length=25, verbose_name=u"AppId", help_text=u"小程序ID")
    app_secret = models.CharField(max_length=50, verbose_name=u"AppSecret", help_text=u"小程序密钥")
    t_type = models.CharField(max_length=10, verbose_name=u"类型", choices=TOKEN_TYPE, default="pg")

    def __str__(self):
        return str(self.id)

    class Meta:
        verbose_name = u"微信配置"
        verbose_name_plural = u"微信配置"


def create_share_code(num=8):
    """
    创建一个随机字符串，可以用来做邀请码、验证码等
    :param num: 字符串长度
    :return:
    """
    source = string.ascii_letters + string.digits
    code = ""
    for i in range(num):
        code += random.choice(source)

    return code


class UserProfile(models.Model):
    """
    扩展用户系统。
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    c_time = models.DateTimeField(auto_now_add=True, verbose_name=u"创建时间")
    openid = models.CharField(max_length=35, verbose_name=u"微信唯一标识")
    unionid = models.CharField(max_length=50, verbose_name=u"全局唯一标识", default="")
    session_key = models.CharField(max_length=50, verbose_name=u"会话密钥")
    nickname = models.CharField(max_length=50, verbose_name=u"昵称", blank=True)
    sex = models.IntegerField(choices=SEX, default=0, verbose_name=u"性别")
    avatar = models.TextField(verbose_name=u"用户头像", default="", blank=True, null=True)
    country = models.CharField(max_length=50, verbose_name=u"所在国家", blank=True)
    province = models.CharField(max_length=50, verbose_name=u"所在省份", blank=True)
    city = models.CharField(max_length=50, verbose_name=u"所在城市", blank=True)
    language = models.CharField(max_length=50, verbose_name=u"语言", blank=True)
    share_code = models.CharField(max_length=8, default=create_share_code, verbose_name=u"邀请码")
    invite_code = models.CharField(max_length=8, blank=True, null=True, verbose_name=u"邀请人")
    balance = models.IntegerField(default=0, verbose_name=u"积分")
    rank = models.IntegerField(default=0, verbose_name=u"积分排行")

    # 积分计算倍数
    base = models.IntegerField(default=0, verbose_name=u"基础积分")
    times = models.IntegerField(default=1, verbose_name=u"积分倍数")

    # 用户认证判断
    is_phone = models.BooleanField(default=False, verbose_name=u"手机号认证")
    phone = models.CharField(max_length=20, verbose_name=u"手机号码", blank=True, null=True)
    is_email = models.BooleanField(default=False, verbose_name=u"电子邮箱")
    is_real_name = models.BooleanField(default=False, verbose_name=u"实名认证")
    is_face = models.BooleanField(default=False, verbose_name=u"人脸识别")
    is_mp = models.BooleanField(default=False, verbose_name=u"公众号关注")

    # 授权
    is_wx_run = models.BooleanField(default=False, verbose_name=u"微信运动")

    def __str__(self):
        return self.nickname

    class Meta:
        verbose_name = u"用户额外信息"
        verbose_name_plural = u"用户额外信息"


class TaskInfo(models.Model):
    """
    任务活动信息
    """
    tf = models.CharField(max_length=20, verbose_name=u"唯一标识", unique=True)
    name = models.CharField(max_length=20, verbose_name=u"活动名称")
    point = models.IntegerField(verbose_name=u"积分点数")
    is_multi = models.BooleanField(default=False, verbose_name=u"是否可多次完成")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = u"任务基础信息"
        verbose_name_plural = u"任务基础信息"


class StatisticalData(models.Model):
    """
    系统数据统计
    """
    p_num = models.IntegerField(verbose_name=u"用户人数")
    balance = models.IntegerField(verbose_name=u"总积分")
    update_time = models.DateTimeField(auto_now=True, verbose_name=u"最后更新时间")

    def __str__(self):
        return str(self.id)

    class Meta:
        verbose_name = u"数据统计"
        verbose_name_plural = u"数据统计"


class SignRecord(models.Model):
    """
    每日签到记录
    """
    user = models.ForeignKey(User, verbose_name=u"用户", on_delete=models.CASCADE)
    c_time = models.DateTimeField(auto_now_add=True, verbose_name=u"签到时间")

    def __str__(self):
        return str(self.id)

    class Meta:
        verbose_name = u"签到记录"
        verbose_name_plural = u"签到记录"


class PointRecord(models.Model):
    """
    积分增加记录
    """
    c_time = models.DateTimeField(auto_now_add=True, verbose_name=u"创建时间")
    user = models.ForeignKey(User, verbose_name=u"用户", on_delete=models.CASCADE)
    task = models.ForeignKey(TaskInfo, verbose_name=u"任务", on_delete=models.CASCADE)
    point = models.IntegerField(verbose_name=u"增减点数")

    def __str__(self):
        return str(self.id)

    class Meta:
        verbose_name = u"积分记录"
        verbose_name_plural = u"积分记录"


class WxRunRecord(models.Model):
    """
    用户微信运动步数
    """
    c_time = models.DateTimeField(auto_now_add=True, verbose_name=u"创建时间")
    user = models.ForeignKey(User, verbose_name=u"用户", on_delete=models.CASCADE)
    c_date = models.DateField(verbose_name=u"日期")
    step = models.IntegerField(verbose_name=u"步数")

    def __str__(self):
        return str(self.id)

    class Meta:
        verbose_name = u"微信运动"
        verbose_name_plural = u"微信运动"
        unique_together = ["user", "c_date"]


class UploadFile(models.Model):
    """
    文件上传信息
    """
    c_time = models.DateTimeField(auto_now_add=True, verbose_name=u"创建时间")
    user = models.ForeignKey(User, verbose_name=u"用户", on_delete=models.CASCADE)
    name = models.TextField(verbose_name=u"文件名称")
    path = models.CharField(max_length=100, verbose_name=u"文件路径")
    is_delete = models.BooleanField(default=False, verbose_name=u"是否删除")

    def __str__(self):
        return str(self.id)

    class Meta:
        verbose_name = u"上传文件列表"
        verbose_name_plural = u"上传文件列表"


STATUS = (
    ("audit", u"审核中"),
    ("success", u"审核成功"),
    ("failed", u"审核失败"),
)


class EyeImage(models.Model):
    """
    用户的眼底照片
    状态分为：
        audit   审核中
        success 审核成功
        failed  审核失败
    只有审核失败的情况下，才可以重新上传提交审核
    """
    c_time = models.DateTimeField(auto_now_add=True, verbose_name=u"创建时间")
    user = models.ForeignKey(User, verbose_name=u"用户", on_delete=models.CASCADE)
    status = models.CharField(max_length=20, verbose_name=u"审核状态", choices=STATUS)
    ufs = models.ManyToManyField(UploadFile, verbose_name=u"待审核文件")

    def __str__(self):
        return str(self.id)

    class Meta:
        verbose_name = u"眼底片审核"
        verbose_name_plural = u"眼底片审核"


@receiver(post_save, sender=EyeImage)
def eye_image_audit(sender, instance, **kwargs):
    """
    在审核通过之后，执行相关操作
    :param sender: 需要保存的model，这里是EyeImage
    :param instance: EyeImage对象
    :param kwargs:
    :return:
    """
    if instance.status == "success":
        # 查询是否需要增加用户积分
        task = TaskInfo.objects.get(tf="eye_image")
        prs = PointRecord.objects.filter(user=instance.user, task=task)
        if prs.exists():
            # 不允许重复添加积分
            return

        # 增加积分记录
        pr = PointRecord(user=instance.user, task=task, point=task.point)
        pr.save()

        # 增加积分
        up = instance.user.userprofile
        up.base += task.point
        up.balance = up.base * up.times
        up.save()


class WXToken(models.Model):
    """
    微信小程序或公众号access token
    两小时有效期
    """
    c_time = models.DateTimeField(auto_now_add=True, verbose_name=u"创建时间")
    token = models.TextField(verbose_name=u"AccessToken")
    t_type = models.CharField(max_length=10, verbose_name=u"类型", choices=TOKEN_TYPE)

    def __str__(self):
        return str(self.id)

    class Meta:
        verbose_name = "AccessToken"
        verbose_name_plural = "AccessToken"


MSG_TYPE = (
    ("event", u"事件"),
    ("txt", u"文本消息"),
    ("image", u"图片消息"),
    ("voice", u"语音消息"),
    ("video", u"视频消息"),
    ("shortvideo", u"小视频消息"),
    ("location", u"地理位置"),
    ("link", u"链接")
)


SUBSCRIBE_SCENE = (
    ("ADD_SCENE_SEARCH", u"公众号搜索"),
    ("ADD_SCENE_ACCOUNT_MIGRATION", u"公众号迁移"),
    ("ADD_SCENE_PROFILE_CARD", u"名片分享"),
    ("ADD_SCENE_QR_CODE", u"扫描二维码"),
    ("ADD_SCENEPROFILE LINK", u"图文页内名称点击"),
    ("ADD_SCENE_PROFILE_ITEM", u"图文页右上角菜单"),
    ("ADD_SCENE_PAID", u"支付后关注"),
    ("ADD_SCENE_OTHERS", u"其他")
)


class WeChatSubscription(models.Model):
    """
    微信公众号关注信息。
    """
    c_time = models.DateTimeField(auto_now_add=True, verbose_name=u"创建时间")
    openid = models.CharField(max_length=35, verbose_name=u"微信唯一标识")
    unionid = models.CharField(max_length=50, verbose_name=u"全局唯一标识")
    msg_type = models.CharField(max_length=20, verbose_name=u"类型", choices=MSG_TYPE, default="event")
    nickname = models.CharField(max_length=100, verbose_name=u"昵称", blank=True, null=True)
    sex = models.IntegerField(choices=SEX, default=0, verbose_name=u"性别")
    avatar = models.TextField(verbose_name=u"用户头像", default="", blank=True, null=True)
    country = models.CharField(max_length=50, verbose_name=u"所在国家", blank=True)
    province = models.CharField(max_length=50, verbose_name=u"所在省份", blank=True)
    city = models.CharField(max_length=50, verbose_name=u"所在城市", blank=True)
    language = models.CharField(max_length=50, verbose_name=u"语言", blank=True)
    subscribe_scene = models.TextField(verbose_name=u"关注来源", choices=SUBSCRIBE_SCENE)
    s_time = models.DateTimeField(verbose_name=u"关注时间", help_text=u"多次关注，取最后一次关注时间")

    def __str__(self):
        return self.nickname

    class Meta:
        verbose_name = u"公众号关注"
        verbose_name_plural = u"公众号关注"
        unique_together = ["openid", "unionid"]


@receiver(post_save, sender=WeChatSubscription)
def check_sub(sender, instance, **kwargs):
    """
    在保存公众号关注信息以后，检查是否增加积分
    :param sender:
    :param instance:
    :param kwargs:
    :return:
    """
    unionid = instance.unionid
    ups = UserProfile.objects.filter(unionid=unionid)
    if ups.exists():
        up = ups[0]
        task = TaskInfo.objects.get(tf="sub_pg")
        prs = PointRecord.objects.filter(task=task, user=up.user)
        if not prs.exists():
            # 记录积分记录
            pr = PointRecord(user=up.user, task=task, point=task.point)
            pr.save()

            # 增加积分
            up.base += task.point
            up.balance = up.base * up.times
            up.save()


class InviteRank(models.Model):
    """
    邀请排行榜
    """
    c_date = models.DateField(verbose_name=u"统计日期")
    user = models.ForeignKey(User, verbose_name=u"用户", on_delete=models.CASCADE)
    num = models.IntegerField(verbose_name=u"邀请人数", help_text=u"当日邀请人数")
    rank = models.IntegerField(verbose_name=u"排名", help_text=u"当日排名")

    def __str__(self):
        return str(self.id)

    class Meta:
        verbose_name = u"邀请排行榜"
        verbose_name_plural = u"邀请排行榜"
        unique_together = ("c_date", "user")



