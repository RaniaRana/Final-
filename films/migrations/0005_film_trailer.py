# Generated by Django 5.0.6 on 2024-06-01 13:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('films', '0004_watchlist'),
    ]

    operations = [
        migrations.AddField(
            model_name='film',
            name='trailer',
            field=models.URLField(default='', max_length=1500),
        ),
    ]
