# Generated by Django 2.2 on 2019-06-19 03:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('manager', '0006_merge_20190611_1757'),
    ]

    operations = [
        migrations.AddField(
            model_name='workout',
            name='imported',
            field=models.BooleanField(blank=True, default=False),
        ),
    ]