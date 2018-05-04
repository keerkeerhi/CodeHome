from django.db import models
from django.contrib.auth.models import User

class UserBase(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    uid = models.CharField(max_length=100,verbose_name="uid",help_text="用户id",default='openid')
    nickName = models.CharField(max_length=25, verbose_name="nickName", help_text="用户昵称")
    country = models.CharField(max_length=25, verbose_name="country", help_text="所属地区")
    loginTime = models.CharField(max_length=25, verbose_name="loginTime",help_text="最后一次登录时间",default='default')

class ImgRecord(models.Model):
    openId = models.CharField(max_length=100,verbose_name="openId",help_text="用户id",default='openid')
    content = models.CharField(max_length=5000,verbose_name="content",help_text="记录内容",default='')
# Create your models here.
