# Generated by Django 2.0.7 on 2018-08-04 03:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('watchandlearn', '0005_remove_word_definition'),
    ]

    operations = [
        migrations.AddField(
            model_name='episode',
            name='subtitle',
            field=models.FilePathField(allow_folders=True, default='Default', path='watchandlearn/static/subtitles', recursive=True),
        ),
    ]
