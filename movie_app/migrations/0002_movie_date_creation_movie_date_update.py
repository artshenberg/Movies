# Generated by Django 4.0.1 on 2022-01-18 05:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movie_app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='movie',
            name='date_creation',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AddField(
            model_name='movie',
            name='date_update',
            field=models.DateTimeField(auto_now=True),
        ),
    ]