# Generated by Django 3.1.2 on 2020-12-16 19:22

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0011_auto_20201216_1404'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderupdate',
            name='timestamp',
            field=models.DateTimeField(verbose_name=datetime.datetime(2020, 12, 16, 19, 22, 58, 131215, tzinfo=utc)),
        ),
    ]
