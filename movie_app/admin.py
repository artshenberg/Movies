from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import *


class MoviesAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'get_html_photo', 'year', 'rating', 'get_html_genres')
    list_display_links = ('id', 'title',)
    search_fields = ('title', 'description',)
    list_editable = ('rating',)
    list_filter = ('year', 'rating', 'genre')
    prepopulated_fields = {'slug': ('title', 'year')}
    fields = ('title', 'slug', 'date_creation', 'year', 'rating', 'genre', 'get_html_photo', 'cover', 'description')
    readonly_fields = ('get_html_photo',)
    save_on_top = True

    def get_html_photo(self, obj):
        if obj.cover:
            return mark_safe(f'<img src="{obj.cover.url}" style="width: 50px;">')

    def get_html_genres(self, obj):
        genres = '<div class="d-flex flex-wrap justify-content-start">'
        for genre in obj.genre.all():
            genres += f'<small class="me-2">{genre}</small>'
        genres += '</div>'
        return mark_safe(genres)

    get_html_photo.short_description = 'Cover'
    get_html_genres.short_description = 'Genres'


class GenreAdmin(admin.ModelAdmin):
    list_display = ('id', 'name',)
    list_display_links = ('id', 'name',)
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}


class MenuItemAdmin(admin.ModelAdmin):
    list_display = ('position', 'title', 'slug')
    list_display_links = ('title',)
    search_fields = ('title',)
    prepopulated_fields = {'slug': ('title',)}
    list_editable = ('position',)


class SubscribeAdmin(admin.ModelAdmin):
    list_display = ('email', 'date_subscribe', 'is_active', 'date_unsubscribe')
    search_fields = ('email', 'date_subscribe')


admin.site.register(Movie, MoviesAdmin)
admin.site.register(Genre, GenreAdmin)
admin.site.register(MenuItem, MenuItemAdmin)
admin.site.register(Subscribe, SubscribeAdmin)

admin.site.site_title = 'All movies administration'
admin.site.site_header = 'All movies administration'
