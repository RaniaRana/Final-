# Generated by Django 5.0.6 on 2024-05-13 10:07

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Film',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=250)),
                ('released', models.DateField()),
                ('certificate', models.CharField(max_length=3)),
                ('duration', models.DurationField()),
                ('genre', models.CharField(max_length=100)),
                ('director', models.CharField(max_length=250)),
                ('star1', models.CharField(max_length=250)),
                ('star2', models.CharField(max_length=250)),
                ('star3', models.CharField(max_length=250)),
                ('star4', models.CharField(max_length=250)),
                ('overview', models.TextField(max_length=1000)),
                ('poster', models.URLField()),
            ],
        ),
        migrations.CreateModel(
            name='Rating',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rating', models.IntegerField()),
                ('film', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='films.film')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
