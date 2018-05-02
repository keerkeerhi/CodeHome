from django.db import models
from django.contrib.auth.models import User

class UserBase(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # uid = models.CharField(max_length=25,verbose_name="uid",help_text="用户id")
    nickName = models.CharField(max_length=25, verbose_name="nickName", help_text="用户昵称")
    country = models.CharField(max_length=25, verbose_name="country", help_text="所属地区")

# Create your models here.
