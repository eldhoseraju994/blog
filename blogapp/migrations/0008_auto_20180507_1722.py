# Generated by Django 2.0.5 on 2018-05-07 11:52

import datetime
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('blogapp', '0007_auto_20180507_1527'),
    ]

    operations = [
        migrations.CreateModel(
            name='Reply',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rply', models.TextField()),
                ('posted_date', models.DateField(default=django.utils.timezone.now)),
                ('comment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='get_comment_reply', to='blogapp.Comment')),
            ],
        ),
        migrations.AlterField(
            model_name='blog',
            name='published_date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2018, 5, 7, 11, 52, 42, 753957, tzinfo=utc), null=True),
        ),
    ]
