# Generated by Django 5.0.4 on 2024-04-21 20:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_graphic_data_assists_graphic_data_damage_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='summoner',
            name='region',
            field=models.CharField(default=None, max_length=30),
        ),
    ]
