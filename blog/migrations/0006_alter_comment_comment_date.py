# Generated by Django 3.2.5 on 2022-07-12 15:08

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0005_auto_20220712_2307'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='comment_date',
            field=models.DateTimeField(default=datetime.datetime(2022, 7, 12, 23, 8, 32, 93281), verbose_name='评论日期'),
        ),
    ]
