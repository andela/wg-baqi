# Generated by Django 2.2 on 2019-06-10 07:40

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_merge_20190605_1804'),
    ]

    operations = [
        migrations.AlterField(
            model_name='license',
            name='full_name',
            field=models.CharField(help_text='If a license has been localized, e.g. the Creative Commons licenses for the different countries, add them as separate entries here.', max_length=60, verbose_name='Full name'),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='notification_language',
            field=models.ForeignKey(default=2, help_text='Language to use when sending you email notifications, e.g. email reminders for workouts. This does not affect the language used on the website.', on_delete=django.db.models.deletion.CASCADE, to='core.Language', verbose_name='Notification language'),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='num_days_weight_reminder',
            field=models.IntegerField(default=0, help_text='Number of days after the last weight entry (enter 0 to deactivate)', validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(30)], verbose_name='Automatic reminders for weight entries'),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='ro_access',
            field=models.BooleanField(default=False, help_text='Allow external users to access your workouts and logs in a read-only mode. You need to set this before you can share links e.g. to social media.', verbose_name='Allow external access'),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='show_comments',
            field=models.BooleanField(default=True, help_text='Check to show exercise comments on the workout view', verbose_name='Show exercise comments'),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='show_english_ingredients',
            field=models.BooleanField(default=True, help_text='Check to also show ingredients in English while creating\na nutritional plan. These ingredients are extracted from a list provided\nby the US Department of Agriculture. It is extremely complete, with around\n7000 entries, but can be somewhat overwhelming and make the search\ndifficult.', verbose_name='Also use ingredients in English'),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='timer_pause',
            field=models.IntegerField(default=90, help_text='Default duration in seconds of pauses used by the timer in the gym mode.', validators=[django.core.validators.MinValueValidator(10), django.core.validators.MaxValueValidator(400)], verbose_name='Default duration of workout pauses'),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='workout_duration',
            field=models.IntegerField(default=12, help_text='Default duration in weeks of workouts not in a schedule. Used for email workout reminders.', validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(30)], verbose_name='Default duration of workouts'),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='workout_reminder',
            field=models.IntegerField(default=14, help_text='The number of days you want to be reminded before a workout expires.', validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(30)], verbose_name='Remind before expiration'),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='workout_reminder_active',
            field=models.BooleanField(default=False, help_text='Check to activate automatic reminders for workouts. You need to provide a valid email for this to work.', verbose_name='Activate workout reminders'),
        ),
    ]
