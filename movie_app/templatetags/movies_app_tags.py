from django import template
from movie_app.models import *
from movie_app.forms import *

register = template.Library()


@register.filter
def subtract(value, arg):
    return value - arg


@register.simple_tag
def concat_all(*args):
    """concatenate all args"""
    return ''.join(map(str, args))


@register.inclusion_tag('includes/movie_app/navbar.html', takes_context=True)
def show_top_menu(context):
    context['menu_items'] = MenuItem.objects.all()
    return context


@register.inclusion_tag('includes/movie_app/subscribe.html')
def subscribe_form():
    return {'subscribe_form': SubscribeForm}


@register.simple_tag
def url_replace(request, field, value):
    dict_ = request.GET.copy()
    dict_[field] = value
    return dict_.urlencode()


@register.filter
def slice_partitions(value: str, arg: (int, float, str)):
    words = value.split()
    try:
        delimiter = int(arg)
        data = dict()
        data['first_part'] = ' '.join(words[:delimiter])
        data['second_part'] = ' '.join(words[delimiter:])
        return data
    except ValueError(f'''Incorrect value of delimiter "{arg}".
                        Use delimiters like these: "x:" or ":x".'''):
        raise
