import datetime

from captcha.fields import CaptchaField
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from .models import *
from crispy_forms.helper import FormHelper


class AddMovieForm(forms.ModelForm):
    captcha = CaptchaField()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['genre'].empty_label = '< Choose genre(s) >'
        self.helper = FormHelper()

    class Meta:
        model = Movie
        fields = ['title', 'slug', 'description', 'year', 'cover', 'rating', 'genre']

    def clean_title(self):
        title = self.cleaned_data['title']
        if len(title) > 255:
            raise ValidationError('Length is more than 255 symbols.')
        return title

    def clean_year(self):
        year = self.cleaned_data['year']
        now = datetime.datetime.now().year + 1
        if not 1878 >= year >= now:
            raise ValidationError(f'Year may be after 1878 and before {now} inclusive.')
        return year

    def clean_rating(self):
        rating = self.cleaned_data['rating']
        if not 0 >= rating >= 100:
            raise ValidationError(f'Rating may be from 0 to 100.')
        return rating


class RegisterUserForm(UserCreationForm):
    captcha = CaptchaField()
    email = forms.CharField(max_length=255, required=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()

    def clean_email(self):
        email = self.cleaned_data['email']
        is_exists = User.objects.filter(email=email)
        if is_exists:
            raise ValidationError(f'User with email "{email}" already exists.')
        return email

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']


class LoginUserForm(AuthenticationForm):
    captcha = CaptchaField()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()

    class Meta:
        model = User


class ContactForm(forms.ModelForm):
    captcha = CaptchaField()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()

    class Meta:
        model = ContactUsData
        fields = ['subject', 'content', 'name', 'email']


class SubscribeForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()

    def clean_email(self):
        email = self.cleaned_data['email']
        is_exists = Subscribe.objects.filter(email=email)
        if is_exists:
            raise ValidationError(f'Your email "{email}" is already subscribed!')
        return email

    class Meta:
        model = Subscribe
        fields = ['email']
        widgets = {
            'email': forms.TextInput(attrs={'class': 'form-control',
                                            'id': 'newsletter',
                                            'onchange': 'this.form.submit()',
                                            'placeholder': 'Your email...'})
        }
        labels = {
            'email': ''
        }
