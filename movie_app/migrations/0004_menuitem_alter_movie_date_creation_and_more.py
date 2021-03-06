# Generated by Django 4.0.1 on 2022-01-28 05:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movie_app', '0003_alter_movie_date_creation_alter_movie_date_update_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='MenuItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=128)),
                ('slug', models.SlugField(max_length=155, unique=True, verbose_name='URL')),
                ('position', models.PositiveIntegerField(default=1)),
            ],
            options={
                'verbose_name': 'Menu item',
                'verbose_name_plural': 'Menu items',
                'ordering': ('position',),
            },
        ),
        migrations.AlterField(
            model_name='movie',
            name='date_creation',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Creation date'),
        ),
        migrations.AlterField(
            model_name='movie',
            name='date_update',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
