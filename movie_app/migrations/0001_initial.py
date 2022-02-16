# Generated by Django 4.0.1 on 2022-01-12 07:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Genre',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, max_length=100)),
                ('slug', models.SlugField(max_length=255, unique=True, verbose_name='URL')),
            ],
            options={
                'verbose_name': 'Genre',
                'verbose_name_plural': 'Genres',
                'ordering': ('name',),
            },
        ),
        migrations.CreateModel(
            name='Movie',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, verbose_name='Film name')),
                ('slug', models.SlugField(max_length=255, unique=True, verbose_name='URL')),
                ('description', models.TextField()),
                ('cover', models.ImageField(upload_to='covers/%Y/%m/%d')),
                ('year', models.IntegerField()),
                ('rating', models.IntegerField()),
                ('genre', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='movie_app.genre')),
            ],
            options={
                'verbose_name': 'All movies',
                'verbose_name_plural': 'All movies',
                'ordering': ('title', 'year'),
            },
        ),
    ]
