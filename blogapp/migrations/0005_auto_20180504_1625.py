# Generated by Django 2.0.5 on 2018-05-04 10:55

import datetime
from django.db import migrations, models
import django.db.models.deletion
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('blogapp', '0004_auto_20180504_1204'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blog',
            name='published_date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2018, 5, 4, 10, 55, 36, 833980, tzinfo=utc), null=True),
        ),
        migrations.AlterField(
            model_name='comment',
            name='blog',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='get_blog_comment', to='blogapp.Blog'),
        ),
    ]