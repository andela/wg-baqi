# Generated by Django 2.2 on 2019-06-03 16:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gym', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contract',
            name='payment',
            field=models.CharField(choices=[
                ('1', 'Yearly'),
                ('2', 'Half yearly'),
                ('3', 'Monthly'), ('4', 'Biweekly'),
                ('5', 'Weekly'),
                ('6', 'Daily')],
                default='3',
                help_text='How often the amount will be charged to the member',
                max_length=2, verbose_name='Payment type'),
        ),
        migrations.AlterField(
            model_name='gymconfig',
            name='weeks_inactive',
            field=models.PositiveIntegerField(
                default=4,
                 help_text='Number of weeks since the last time a user logged \
                 his presence to be considered inactive',
                 verbose_name='Reminder of inactive members'),
        ),
        migrations.AlterField(
            model_name='gymuserconfig',
            name='include_inactive',
            field=models.BooleanField(
                default=True,
                 help_text='Include this user in the email list with inactive \
                 members', verbose_name='Include in inactive overview'),
        ),
    ]
