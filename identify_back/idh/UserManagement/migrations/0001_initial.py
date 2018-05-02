# Generated by Django 2.0.2 on 2018-03-05 17:21

import UserManagement.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('c_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('openid', models.CharField(max_length=35, verbose_name='微信唯一标识')),
                ('nickname', models.CharField(blank=True, max_length=50, verbose_name='昵称')),
                ('sex', models.IntegerField(choices=[(1, '男'), (2, '女'), (0, '未知')], default=0, verbose_name='性别')),
                ('avatar', models.TextField(default='', verbose_name='用户头像')),
                ('country', models.CharField(blank=True, max_length=50, verbose_name='所在国家')),
                ('province', models.CharField(blank=True, max_length=50, verbose_name='所在省份')),
                ('city', models.CharField(blank=True, max_length=50, verbose_name='所在城市')),
                ('language', models.CharField(blank=True, max_length=50, verbose_name='语言')),
                ('share_code', models.CharField(default=UserManagement.models.create_share_code, max_length=8, verbose_name='邀请码')),
                ('balance', models.IntegerField(default=0, verbose_name='积分')),
                ('is_phone', models.BooleanField(default=False, verbose_name='手机号认证')),
                ('phone', models.CharField(blank=True, max_length=20, null=True, verbose_name='手机号码')),
                ('is_email', models.BooleanField(default=False, verbose_name='电子邮箱')),
                ('is_real_name', models.BooleanField(default=False, verbose_name='实名认证')),
                ('is_face', models.BooleanField(default=False, verbose_name='人脸识别')),
                ('is_wx_run', models.BooleanField(default=False, verbose_name='微信运动')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': '用户额外信息',
                'verbose_name_plural': '用户额外信息',
            },
        ),
        migrations.CreateModel(
            name='WxConfig',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('app_id', models.CharField(help_text='小程序ID', max_length=25, verbose_name='AppId')),
                ('app_secret', models.CharField(help_text='小程序密钥', max_length=50, verbose_name='AppSecret')),
            ],
            options={
                'verbose_name': '微信配置',
                'verbose_name_plural': '微信配置',
            },
        ),
    ]
