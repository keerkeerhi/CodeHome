# Generated by Django 2.0.2 on 2018-03-06 16:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('UserManagement', '0005_taskinfo'),
    ]

    operations = [
        migrations.CreateModel(
            name='StatisticalData',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('p_num', models.IntegerField(verbose_name='用户人数')),
                ('balance', models.IntegerField(verbose_name='总积分')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='最后更新时间')),
            ],
            options={
                'verbose_name': '数据统计',
                'verbose_name_plural': '数据统计',
            },
        ),
    ]