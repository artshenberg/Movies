"""Movies URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls.static import static
from django.urls import path
from django.views.decorators.cache import cache_page

from Movies import settings
from .views import *

app_name = 'movie_app'
urlpatterns = [
    path('', MovieList.as_view(), name='main'),
    path('subscribe/', SubscribeView.as_view(), name='subscribe'),
    path('movie/<slug:slug_movie>', ShowMovie.as_view(), name='movie'),
    path('year/<int:year_movie>', MovieByYear.as_view(), name='year'),
    path('genre/<slug:slug_genre>', MovieByGenre.as_view(), name='genre'),
    path('rating/<int:rating>', MovieByRating.as_view(), name='rating'),
    path('genres/', GenreList.as_view(), name='genres'),
    path('add-movie/', AddMovie.as_view(), name='add-movie'),
    path('about/', about, name='about'),
    path('login/', LoginUser.as_view(), name='login'),
    path('logout/', logout_user, name='logout'),
    path('register/', RegisterUser.as_view(), name='register'),
    path('contacts/', ContactFormView.as_view(), name='contact-us'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
