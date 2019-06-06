# Generated by Django 2.2 on 2019-06-05 09:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('exercises', '0002_auto_20190603_1934'),
    ]

    operations = [
        migrations.AlterField(
            model_name='exercise',
            name='license_author',
            field=models.CharField(blank=True, help_text='If you are not the author, enter the name or source here. This is needed for some licenses e.g. the CC-BY-SA.', max_length=50, null=True, verbose_name='Author'),
        ),
        migrations.AlterField(
            model_name='exerciseimage',
            name='is_main',
            field=models.BooleanField(default=False, help_text='Tick the box if you want to set this image as the main one for the exercise (will be shown e.g. in the search). The first image is automatically marked by the system.', verbose_name='Main picture'),
        ),
        migrations.AlterField(
            model_name='exerciseimage',
            name='license_author',
            field=models.CharField(blank=True, help_text='If you are not the author, enter the name or source here. This is needed for some licenses e.g. the CC-BY-SA.', max_length=50, null=True, verbose_name='Author'),
        ),
    ]
