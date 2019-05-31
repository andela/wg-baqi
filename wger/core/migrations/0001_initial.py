# Generated by Django 2.2.1 on 2019-05-28 12:17

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('gym', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='DaysOfWeek',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('day_of_week', models.CharField(max_length=9, verbose_name='Day of the week')),
            ],
            options={
                'ordering': ['pk'],
            },
        ),
        migrations.CreateModel(
            name='Language',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('short_name', models.CharField(max_length=2, verbose_name='Language short name')),
                ('full_name', models.CharField(max_length=30, verbose_name='Language full name')),
            ],
            options={
                'ordering': ['full_name'],
            },
        ),
        migrations.CreateModel(
            name='License',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_name', models.CharField(help_text='If a license has been localized, e.g. the Creative Commons licenses for the different countries, add them as separate entries here.', max_length=60, verbose_name='Full name')),
                ('short_name', models.CharField(max_length=15, verbose_name='Short name, e.g. CC-BY-SA 3')),
                ('url', models.URLField(blank=True, help_text='Link to license text or other information', null=True, verbose_name='Link')),
            ],
            options={
                'ordering': ['full_name'],
            },
        ),
        migrations.CreateModel(
            name='RepetitionUnit',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Name')),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='WeightUnit',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Name')),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_temporary', models.BooleanField(default=False, editable=False)),
                ('show_comments', models.BooleanField(default=True, help_text='Check to show exercise comments on the workout view', verbose_name='Show exercise comments')),
                ('show_english_ingredients', models.BooleanField(default=True, help_text='Check to also show ingredients in English while creating\na nutritional plan. These ingredients are extracted from a list provided\nby the US Department of Agriculture. It is extremely complete, with around\n7000 entries, but can be somewhat overwhelming and make the search difficult.', verbose_name='Also use ingredients in English')),
                ('workout_reminder_active', models.BooleanField(default=False, help_text='Check to activate automatic reminders for workouts. You need to provide a valid email for this to work.', verbose_name='Activate workout reminders')),
                ('workout_reminder', models.IntegerField(default=14, help_text='The number of days you want to be reminded before a workout expires.', validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(30)], verbose_name='Remind before expiration')),
                ('workout_duration', models.IntegerField(default=12, help_text='Default duration in weeks of workouts not in a schedule. Used for email workout reminders.', validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(30)], verbose_name='Default duration of workouts')),
                ('last_workout_notification', models.DateField(editable=False, null=True)),
                ('timer_active', models.BooleanField(default=True, help_text='Check to activate timer pauses between exercises.', verbose_name='Use pauses in workout timer')),
                ('timer_pause', models.IntegerField(default=90, help_text='Default duration in seconds of pauses used by the timer in the gym mode.', validators=[django.core.validators.MinValueValidator(10), django.core.validators.MaxValueValidator(400)], verbose_name='Default duration of workout pauses')),
                ('age', models.IntegerField(null=True, validators=[django.core.validators.MinValueValidator(10), django.core.validators.MaxValueValidator(100)], verbose_name='Age')),
                ('height', models.IntegerField(null=True, validators=[django.core.validators.MinValueValidator(140), django.core.validators.MaxValueValidator(230)], verbose_name='Height (cm)')),
                ('gender', models.CharField(choices=[('1', 'Male'), ('2', 'Female')], default='1', max_length=1, null=True)),
                ('sleep_hours', models.IntegerField(default=7, help_text='The average hours of sleep per day', null=True, validators=[django.core.validators.MinValueValidator(4), django.core.validators.MaxValueValidator(10)], verbose_name='Hours of sleep')),
                ('work_hours', models.IntegerField(default=8, help_text='Average hours per day', null=True, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(15)], verbose_name='Work')),
                ('work_intensity', models.CharField(choices=[('1', 'Low'), ('2', 'Medium'), ('3', 'High')], default='1', help_text='Approximately', max_length=1, null=True, verbose_name='Physical intensity')),
                ('sport_hours', models.IntegerField(default=3, help_text='Average hours per week', null=True, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(30)], verbose_name='Sport')),
                ('sport_intensity', models.CharField(choices=[('1', 'Low'), ('2', 'Medium'), ('3', 'High')], default='2', help_text='Approximately', max_length=1, null=True, verbose_name='Physical intensity')),
                ('freetime_hours', models.IntegerField(default=8, help_text='Average hours per day', null=True, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(15)], verbose_name='Free time')),
                ('freetime_intensity', models.CharField(choices=[('1', 'Low'), ('2', 'Medium'), ('3', 'High')], default='1', help_text='Approximately', max_length=1, null=True, verbose_name='Physical intensity')),
                ('calories', models.IntegerField(default=2500, help_text='Total caloric intake, including e.g. any surplus', null=True, validators=[django.core.validators.MinValueValidator(1500), django.core.validators.MaxValueValidator(5000)], verbose_name='Total daily calories')),
                ('weight_unit', models.CharField(choices=[('kg', 'Metric (kilogram)'), ('lb', 'Imperial (pound)')], default='kg', max_length=2, verbose_name='Weight unit')),
                ('ro_access', models.BooleanField(default=False, help_text='Allow external users to access your workouts and logs in a read-only mode. You need to set this before you can share links e.g. to social media.', verbose_name='Allow external access')),
                ('num_days_weight_reminder', models.IntegerField(default=0, help_text='Number of days after the last weight entry (enter 0 to deactivate)', validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(30)], verbose_name='Automatic reminders for weight entries')),
                ('gym', models.ForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, to='gym.Gym')),
                ('notification_language', models.ForeignKey(default=2, help_text='Language to use when sending you email notifications, e.g. email reminders for workouts. This does not affect the language used on the website.', on_delete=django.db.models.deletion.CASCADE, to='core.Language', verbose_name='Notification language')),
                ('user', models.OneToOneField(editable=False, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='UserCache',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('last_activity', models.DateField(null=True)),
                ('user', models.OneToOneField(editable=False, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
