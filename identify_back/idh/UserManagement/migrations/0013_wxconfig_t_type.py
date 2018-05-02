# Generated by Django 2.0.2 on 2018-03-26 19:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('UserManagement', '0012_wxtoken'),
    ]

    operations = [
        migrations.AddField(
            model_name='wxconfig',
            name='t_type',
            field=models.CharField(choices=[('pb', '公众号'), ('pg', '小程序')], default='pg', max_length=10, verbose_name='类型'),
        ),
    ]