# Generated by Django 2.0.7 on 2018-08-04 03:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('watchandlearn', '0006_episode_subtitle'),
    ]

    operations = [
        migrations.AlterField(
            model_name='episode',
            name='subtitle',
            field=models.FilePathField(allow_folders=True, default='Default', path='/watchandlearn/static/watchandlearn/subtitles', recursive=True),
        ),
    ]
