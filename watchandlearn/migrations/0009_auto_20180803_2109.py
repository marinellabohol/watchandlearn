# Generated by Django 2.0.7 on 2018-08-04 04:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('watchandlearn', '0008_auto_20180803_2050'),
    ]

    operations = [
        migrations.AlterField(
            model_name='episode',
            name='subtitle',
            field=models.FilePathField(allow_folders=True, default='Default', path='/watchandlearn/media/subtitles/', recursive=True),
        ),
    ]