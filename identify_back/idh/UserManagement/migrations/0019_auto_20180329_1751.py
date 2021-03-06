# Generated by Django 2.0.2 on 2018-03-29 17:51

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('UserManagement', '0018_auto_20180328_1140'),
    ]

    operations = [
        migrations.CreateModel(
            name='InviteRank',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('c_date', models.DateField(verbose_name='统计日期')),
                ('num', models.IntegerField(help_text='当日邀请人数', verbose_name='邀请人数')),
                ('rank', models.IntegerField(help_text='当日排名', verbose_name='排名')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='用户')),
            ],
            options={
                'verbose_name': '邀请排行榜',
                'verbose_name_plural': '邀请排行榜',
            },
        ),
        migrations.AlterUniqueTogether(
            name='inviterank',
            unique_together={('c_date', 'user')},
        ),
    ]
