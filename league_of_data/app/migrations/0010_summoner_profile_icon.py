# Generated by Django 5.0.4 on 2024-06-18 01:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0009_time_info_summoner_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='summoner',
            name='profile_icon',
            field=models.IntegerField(default=None, verbose_name='ícono de cuenta'),
        ),
    ]
