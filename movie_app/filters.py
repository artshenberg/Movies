from django import forms
import django_filters
from django.db import models
from django_filters import RangeFilter
from movie_app.models import *
from movie_app.forms import *
from movie_app.widgets import *

CHOICES = [
    ['title', 'By movie title ascent'],
    ['-title', 'By movie title descent'],
    ['year', 'Old first'],
    ['-year', 'New first'],
    ['rating', 'Lower first'],
    ['-rating', 'Top first'],
]


class MovieFilter(django_filters.FilterSet):
    ordering = django_filters.OrderingFilter(choices=CHOICES,
                                             required=True,
                                             empty_label=None,
                                             label='Sort by')
    title = django_filters.CharFilter(lookup_expr='icontains')
    year = django_filters.RangeFilter()
    rating = django_filters.RangeFilter()
    genre = django_filters.ModelMultipleChoiceFilter(queryset=Genre.objects.all().order_by('name'))

    class Meta:
        model = Movie
        fields = ['ordering', 'title', 'year', 'rating', 'genre']
        order_by_field = 'title'
