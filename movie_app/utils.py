from django.views import View
from django.views.generic import ListView

from .models import *


class ContextData:
    paginate_by = 3

    def get_user_context(self, **kwargs):
        context = kwargs
        return context
