# Generated by Django 5.0.6 on 2024-06-04 12:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('films', '0011_comment'),
    ]

    operations = [
        migrations.AddField(
            model_name='film',
            name='popularity',
            field=models.IntegerField(default=0, editable=False),
        ),
    ]
