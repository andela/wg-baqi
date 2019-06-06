# Generated by Django 2.2 on 2019-06-06 15:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('manager', '0002_auto_20190603_1934'),
    ]

    operations = [
        migrations.AlterField(
            model_name='day',
            name='description',
            field=models.CharField(help_text='A description of what is done on this day (e.g. "Pull day") or what body parts are trained (e.g. "Arms and abs")', max_length=100, verbose_name='Description'),
        ),
        migrations.AlterField(
            model_name='schedule',
            name='is_active',
            field=models.BooleanField(default=True, help_text='Tick the box if you want to mark this schedule as your active one (will be shown e.g. on your dashboard). All other schedules will then be marked as inactive', verbose_name='Schedule active'),
        ),
        migrations.AlterField(
            model_name='schedule',
            name='is_loop',
            field=models.BooleanField(default=False, help_text='Tick the box if you want to repeat the schedules in a loop (i.e. A, B, C, A, B, C, and so on)', verbose_name='Is a loop'),
        ),
        migrations.AlterField(
            model_name='schedule',
            name='name',
            field=models.CharField(help_text="Name or short description of the schedule. For example 'Program XYZ'.", max_length=100, verbose_name='Name'),
        ),
        migrations.AlterField(
            model_name='workout',
            name='comment',
            field=models.CharField(blank=True, help_text="A short description or goal of the workout. For example 'Focus on back' or 'Week 1 of program xy'.", max_length=100, verbose_name='Description'),
        ),
        migrations.AlterField(
            model_name='workoutsession',
            name='impression',
            field=models.CharField(choices=[('1', 'Bad'), ('2', 'Neutral'), ('3', 'Good')], default='2', help_text='Your impression about this workout session. Did you exercise as well as you could?', max_length=2, verbose_name='General impression'),
        ),
        migrations.AlterField(
            model_name='workoutsession',
            name='notes',
            field=models.TextField(blank=True, help_text='Any notes you might want to save about this workout session.', null=True, verbose_name='Notes'),
        ),
    ]
