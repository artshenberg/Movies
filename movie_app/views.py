from django.contrib.auth import logout, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.db.models import Count
from django.http import HttpResponseRedirect, QueryDict
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import ListView, DetailView, CreateView, FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.cache import cache
from django_filters.views import FilterView

from .filters import MovieFilter
from .models import *
from .forms import *
from .utils import *

titles = {
    'main': 'All movies',
    'add-movie': 'Add movie',
    'about': 'About',
    'login': 'Log in',
    'register': 'Registration',
    'contacts': 'Contact us',
    'genres': 'All genres',
    'genre': 'Genre',
    'year': 'Movies from the',
    'rating': 'Movies by rating',
    'subscribe': 'Subscribing result'
}


class MovieList(ContextData, FilterView, ListView):
    model = Movie
    template_name = 'movie_app/main.html'
    context_object_name = 'movies'
    filterset_class = MovieFilter

    def get_queryset(self):
        # movies = cache.get('movies')
        # if not movies:
        #     movies = Movies.objects.filter(date_creation__lte=timezone.now()).select_related('genre')
        #     cache.set('movies', movies, 60)
        # return movies
        return self.model.objects\
            .filter(date_creation__lte=timezone.now())\
            .prefetch_related('genre')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(MovieList, self).get_context_data(**kwargs)
        context_data = self.get_user_context(title=titles['main'])
        return context | context_data


class ShowMovie(ContextData, DetailView):
    model = Movie
    template_name = 'movie_app/movie.html'
    slug_url_kwarg = 'slug_movie'
    context_object_name = 'movie'

    def get_queryset(self):
        return self.model.objects.filter(date_creation__lte=timezone.now()).prefetch_related('genre')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context_data = self.get_user_context(title=f"{context['movie'].title} ({context['movie'].year})")
        return context | context_data


class MovieByGenre(ContextData, FilterView):
    model = Movie
    template_name = 'movie_app/sorted_movies_by.html'
    context_object_name = 'movies'
    allow_empty = False
    filterset_class = MovieFilter

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context_data = self.get_user_context(title=f"{titles['genre']} \"{self.kwargs['slug_genre'].title()}\"")
        return context | context_data

    def get_queryset(self):
        order = self.request.GET.get('orderby', 'title')
        return self.model.objects\
            .filter(genre__slug=self.kwargs['slug_genre'])\
            .prefetch_related('genre')


class MovieByYear(ContextData, FilterView):
    model = Movie
    template_name = 'movie_app/sorted_movies_by.html'
    context_object_name = 'movies'
    allow_empty = False
    filterset_class = MovieFilter

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context_data = self.get_user_context(title=f"{titles['year']} \"{self.kwargs['year_movie']}\"")
        return context | context_data

    def get_queryset(self):
        return self.model.objects\
            .filter(year=self.kwargs['year_movie'])\
            .prefetch_related('genre')


class MovieByRating(ContextData, FilterView):
    model = Movie
    template_name = 'movie_app/sorted_movies_by.html'
    context_object_name = 'movies'
    allow_empty = False
    filterset_class = MovieFilter

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context_data = self.get_user_context(title=f"{titles['rating']} \"{self.kwargs['rating']}\"")
        return context | context_data

    def get_queryset(self):
        return self.model.objects\
            .filter(rating=self.kwargs['rating'])\
            .prefetch_related('genre')


class GenreList(ContextData, ListView):
    model = Genre
    template_name = 'movie_app/genre_list.html'
    context_object_name = 'genres'
    paginate_by = 0
    filterset_class = MovieFilter

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context_data = self.get_user_context(title=titles['genres'])
        return context | context_data

    def get_queryset(self):
        return self.model.objects.all().annotate(Count('movie'))


class AddMovie(LoginRequiredMixin, ContextData, CreateView):
    form_class = AddMovieForm
    template_name = 'movie_app/add_movie.html'
    raise_exception = True

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context_data = self.get_user_context(title=titles['add-movie'])
        return context | context_data


def about(request):
    context = {
        'title': titles['about'],
    }
    return render(request, 'movie_app/about.html', context)


class RegisterUser(ContextData, CreateView):
    form_class = RegisterUserForm
    template_name = 'movie_app/register.html'
    success_url = reverse_lazy('movie_app:login')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context_data = self.get_user_context(title=titles['register'])
        return context | context_data

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('movie_app:main')


class LoginUser(ContextData, LoginView):
    form_class = LoginUserForm
    template_name = 'movie_app/login.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context_data = self.get_user_context(title=titles['login'])
        return context | context_data

    def get_success_url(self):
        return reverse_lazy('movie_app:main')


def logout_user(request):
    logout(request)
    return redirect('movie_app:login')


class ContactFormView(ContextData, FormView):
    form_class = ContactForm
    template_name = 'movie_app/contact.html'
    success_url = reverse_lazy('movie_app:main')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context_data = self.get_user_context(title=titles['contacts'])
        return context | context_data

    def form_valid(self, form):
        print(form.cleaned_data)
        return redirect('movie_app:main')


class SubscribeView(CreateView):
    form_class = SubscribeForm
    model = Subscribe
    success_url = reverse_lazy('movie_app:subscribe')
    template_name = 'movie_app/subscribe_done.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = titles['subscribe']
        return context
