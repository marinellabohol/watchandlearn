# Generated by Django 2.0.7 on 2018-08-05 22:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('watchandlearn', '0011_episode_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='episode',
            name='image',
            field=models.ImageField(upload_to='watchandlearn/static/watchandlearn/images/episodes/'),
        ),
        migrations.AlterField(
            model_name='series',
            name='image',
            field=models.ImageField(upload_to='watchandlearn/static/watchandlearn/images/series/'),
        ),
    ]