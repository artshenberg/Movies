import datetime
import random

from django.test import TestCase
from django.utils import timezone
from django.urls import reverse

from .models import *


class MoviesModelTests(TestCase):

    def test_was_published_recently_with_future_movie(self):
        """
        was_published_recently() returns False for movies whose date_creation
        is in the future.
        """
        time = timezone.now() + datetime.timedelta(days=30)
        future_movie = Movie(date_creation=time)
        self.assertIs(future_movie.was_published_recently(), False)

    def test_was_published_recently_with_old_question(self):
        """
        was_published_recently() returns False for questions whose pub_date
        is older than 1 day.
        """
        time = timezone.now() - datetime.timedelta(days=1, seconds=1)
        old_question = Movie(date_creation=time)
        self.assertIs(old_question.was_published_recently(), False)

    def test_was_published_recently_with_recent_question(self):
        """
        was_published_recently() returns True for questions whose pub_date
        is within the last day.
        """
        time = timezone.now() - datetime.timedelta(hours=23, minutes=59, seconds=59)
        recent_question = Movie(date_creation=time)
        self.assertIs(recent_question.was_published_recently(), True)


def create_genre(genre_name):
    """
    Create a genre with the given `movie_data` and published the
    given number of `days` offset to now (negative for movies added
    in the past, positive for movies that have yet to be visible).
    """
    return Genre.objects.create(name=genre_name,
                                slug=genre_name.lower().replace(' ', '-'))


def create_movie(movie_data, days):
    """
    Create a movie with the given `movie_data` and published the
    given number of `days` offset to now (negative for movies added
    in the past, positive for movies that have yet to be visible).
    """
    time = timezone.now() + datetime.timedelta(days=days)
    return Movie.objects.create(title=movie_data['title'],
                                slug=f'test{round(random.random() * 1000)}',
                                description=movie_data['description'],
                                cover='',
                                year=movie_data['year'],
                                rating=movie_data['rating'],
                                genre=movie_data['genre'],
                                date_creation=time,
                                date_update=time)


class MovieListTests(TestCase):
    def test_no_movie(self):
        """
        If no movie exist, an appropriate message is displayed.
        """
        response = self.client.get(reverse('movie_app:main'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No movies are available.")
        self.assertQuerysetEqual(response.context['movies'], [])

    def test_past_movie(self):
        """
        Movies with a date_creation in the past are displayed on the
        index page.
        """
        create_genre('Adventure')
        create_movie(movie_data={'title': 'past movie',
                                 'description': 'test1',
                                 'cover': '',
                                 'year': 2021,
                                 'rating': 100,
                                 'genre': Genre.objects.get(name='Adventure')},
                     days=-30)
        response = self.client.get(reverse('movie_app:main'))
        self.assertQuerysetEqual(
            response.context['movies'],
            ["<Movies: past movie, 2021>"]
        )

    def test_future_movie(self):
        """
        Movies with a date_creation in the future aren't displayed on
        the index page.
        """
        create_genre('Adventure')
        create_movie(movie_data={'title': 'future movie',
                                 'description': 'test1',
                                 'cover': '',
                                 'year': 2021,
                                 'rating': 100,
                                 'genre': Genre.objects.get(name='Adventure')},
                     days=30)
        response = self.client.get(reverse('movie_app:main'))
        self.assertContains(response, "No movies are available.")
        self.assertQuerysetEqual(response.context['movies'], [])

    def test_future_movie_and_past_movie(self):
        """
        Even if both past and future movies exist, only past movie
        are displayed.
        """
        create_genre('Adventure')
        create_movie(movie_data={'title': 'past movie',
                                 'description': 'test1',
                                 'cover': '',
                                 'year': 2021,
                                 'rating': 100,
                                 'genre': Genre.objects.get(name='Adventure')},
                     days=-30)
        create_movie(movie_data={'title': 'future movie',
                                 'description': 'test1',
                                 'cover': '',
                                 'year': 2021,
                                 'rating': 100,
                                 'genre': Genre.objects.get(name='Adventure')},
                     days=30)
        response = self.client.get(reverse('movie_app:main'))
        self.assertQuerysetEqual(
            response.context['movies'],
            ["<Movies: past movie, 2021>"]
        )

    def test_two_past_movies(self):
        """
        The movies index page may display multiple movies.
        """
        create_genre('Adventure')
        create_movie(movie_data={'title': 'past movie 1',
                                 'description': 'test1',
                                 'cover': '',
                                 'year': 2021,
                                 'rating': 100,
                                 'genre': Genre.objects.get(name='Adventure')},
                     days=-30)
        create_movie(movie_data={'title': 'past movie 2',
                                 'description': 'test1',
                                 'cover': '',
                                 'year': 2021,
                                 'rating': 100,
                                 'genre': Genre.objects.get(name='Adventure')},
                     days=-5)
        response = self.client.get(reverse('movie_app:main'))
        self.assertQuerysetEqual(
            response.context['movies'],
            ["<Movies: past movie 1, 2021>",
             "<Movies: past movie 2, 2021>"]
        )


class MovieDetailViewTests(TestCase):

    def test_future_movie(self):
        """
        The detail view of a movie with a date_creation in the future
        returns a 404 not found.
        """
        create_genre('Adventure')
        future_movie = create_movie(movie_data={'title': 'future movie',
                                                'description': 'test1',
                                                'cover': '',
                                                'year': 2021,
                                                'rating': 100,
                                                'genre': Genre.objects.get(name='Adventure')},
                                    days=5)
        url = reverse('movie_app:movie', args=(future_movie.slug,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_past_movie(self):
        """
        The detail view of a movie with a date_creation in the past
        displays the movie's description.
        """
        create_genre('Adventure')
        past_movie = create_movie(movie_data={'title': 'past movie',
                                              'description': 'test1',
                                              'cover': '',
                                              'year': 2021,
                                              'rating': 100,
                                              'genre': Genre.objects.get(name='Adventure')},
                                  days=-5)
        url = reverse('movie_app:movie', args=(past_movie.slug,))
        response = self.client.get(url)
        self.assertContains(response, past_movie.title)
