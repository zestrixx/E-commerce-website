# Generated by Django 3.1.2 on 2020-12-15 20:22

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0009_auto_20201216_0147'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderupdate',
            name='timestamp',
            field=models.DateTimeField(default=datetime.datetime(2020, 12, 15, 20, 22, 5, 348928, tzinfo=utc)),
        ),
    ]
