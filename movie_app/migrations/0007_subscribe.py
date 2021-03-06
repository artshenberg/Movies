# Generated by Django 4.0.1 on 2022-02-03 03:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movie_app', '0006_contactusdata'),
    ]

    operations = [
        migrations.CreateModel(
            name='Subscribe',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('is_active', models.BooleanField(default=True, verbose_name='Is subscribed')),
                ('date_subscribe', models.DateTimeField(auto_now_add=True, verbose_name='Subscribe date')),
                ('date_unsubscribe', models.DateTimeField(null=True, verbose_name='Unsubscribe date')),
            ],
            options={
                'verbose_name': 'Subscriber',
                'verbose_name_plural': 'Subscribers',
                'ordering': ('email',),
            },
        ),
    ]
