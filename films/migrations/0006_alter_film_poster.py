# Generated by Django 5.0.6 on 2024-06-01 14:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('films', '0005_film_trailer'),
    ]

    operations = [
        migrations.AlterField(
            model_name='film',
            name='poster',
            field=models.URLField(max_length=500),
        ),
    ]
