import datetime

from django.db import models
from django.urls import reverse
from django.utils import timezone


class Movie(models.Model):
    title = models.CharField(max_length=255, verbose_name='Movie title')
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name='URL')
    description = models.TextField()
    cover = models.ImageField(upload_to='covers/%Y/%m/%d')
    year = models.IntegerField()
    rating = models.IntegerField()
    genre = models.ManyToManyField('Genre')
    date_creation = models.DateTimeField(verbose_name='Creation date', auto_now_add=True)
    date_update = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'All movies'
        verbose_name_plural = 'All movies'
        ordering = ('title', 'year',)

    def __str__(self):
        return f'{self.title}, {self.year}'

    def get_absolute_url(self):
        return reverse('movie_app:movie', kwargs={'slug_movie': self.slug})

    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.date_creation <= now


class Genre(models.Model):
    name = models.CharField(max_length=100, unique=True, db_index=True)
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name='URL')

    class Meta:
        verbose_name = 'Genre'
        verbose_name_plural = 'Genres'
        ordering = ('name',)

    def __str__(self):
        return str(self.name)

    def get_absolute_url(self):
        return reverse('movie_app:genre', kwargs={'slug_genre': self.slug})


def auto_incrementor():
    last_int = MenuItem.objects.all().order_by('position').last()
    if not last_int:
        return 1
    return last_int.position + 1


class MenuItem(models.Model):
    title = models.CharField(max_length=128)
    slug = models.SlugField(max_length=155, unique=True, verbose_name='URL')
    position = models.PositiveIntegerField(default=auto_incrementor,)

    def __str__(self):
        return str(self.title)

    class Meta:
        ordering = ('position',)
        verbose_name = 'Menu item'
        verbose_name_plural = 'Menu items'


class ContactUsData(models.Model):
    name = models.CharField(max_length=255)
    subject = models.CharField(max_length=255)
    email = models.EmailField()
    content = models.TextField()

    def __str__(self):
        return f'From {self.name}, {self.email};\nsubject:\n{self.subject}'

    class Meta:
        ordering = ('name',)
        verbose_name = 'Contact us message'
        verbose_name_plural = 'Contact us messages'


class Subscribe(models.Model):
    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=True, verbose_name='Is subscribed')
    date_subscribe = models.DateTimeField(auto_now_add=True, verbose_name='Subscribe date')
    date_unsubscribe = models.DateTimeField(null=True, verbose_name='Unsubscribe date')

    def __str__(self):
        return self.email

    class Meta:
        ordering = ('email',)
        verbose_name = 'Subscriber'
        verbose_name_plural = 'Subscribers'


class FavoriteMovie(models.Model):
    pass
    # TODO
