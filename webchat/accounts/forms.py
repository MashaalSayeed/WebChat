from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from datetime import datetime

from .models import Profile


def username_validator(username: str):
    if not username.replace('_', '').isalnum():
        return ValidationError('Username can contain alphabets, digits and underscores (_) only')


class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=254, widget= forms.TextInput(attrs={'class':'form-control'}),
        help_text='Required. Inform a valid email address')

    username = forms.CharField(max_length=30, min_length=3, required=True, strip=True, validators=[username_validator],
        widget= forms.TextInput(attrs={'class':'form-control'}),
        help_text='Only alphabets, digits and underscores allowed')

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['password1'].widget = forms.PasswordInput(attrs={'class': 'form-control', 'autocomplete': 'new-password'})
        self.fields['password2'].widget = forms.PasswordInput(attrs={'class': 'form-control', 'autocomplete': 'new-password'})

    def clean(self):
        cleaned = super().clean()
        if 'username' in cleaned and not cleaned['username'].replace('_', '').isalnum():
            self.add_error('username', 'Only alphabets, digits and underscores allowed')


class ProfileForm(forms.ModelForm):
    birth_date = forms.DateField(input_formats=['%Y-%m-%d'], required=False, help_text='Format: YYYY-MM-DD')

    class Meta:
        model = Profile
        fields = ('birth_date',)

