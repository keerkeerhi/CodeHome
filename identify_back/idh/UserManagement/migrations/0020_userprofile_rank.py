# Generated by Django 2.0.2 on 2018-03-29 19:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('UserManagement', '0019_auto_20180329_1751'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='rank',
            field=models.IntegerField(default=0, verbose_name='积分排行'),
        ),
    ]