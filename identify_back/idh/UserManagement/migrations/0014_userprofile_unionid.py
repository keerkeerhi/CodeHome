# Generated by Django 2.0.2 on 2018-03-27 13:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('UserManagement', '0013_wxconfig_t_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='unionid',
            field=models.CharField(default='', max_length=50, verbose_name='全局唯一标识'),
        ),
    ]
