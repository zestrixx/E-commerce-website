# Generated by Django 3.1.2 on 2020-12-22 16:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0018_auto_20201222_1620'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderupdate',
            name='timestamp',
            field=models.DateField(default='datetime.now'),
        ),
    ]
