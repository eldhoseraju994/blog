# Generated by Django 2.0.5 on 2018-05-08 06:47

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('blogapp', '0013_auto_20180508_1217'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blog',
            name='published_date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2018, 5, 8, 6, 47, 40, 306249, tzinfo=utc), null=True),
        ),
    ]