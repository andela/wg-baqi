# Generated by Django 2.2 on 2019-06-05 09:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gym', '0002_auto_20190603_1934'),
    ]

    operations = [
        migrations.AlterField(
            model_name='gymconfig',
            name='weeks_inactive',
            field=models.PositiveIntegerField(default=4, help_text='Number of weeks since the last time a user logged his presence to be considered inactive', verbose_name='Reminder of inactive members'),
        ),
        migrations.AlterField(
            model_name='gymuserconfig',
            name='include_inactive',
            field=models.BooleanField(default=True, help_text='Include this user in the email list with inactive members', verbose_name='Include in inactive overview'),
        ),
    ]
