from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic

from .forms import ProfileForm, SignUpForm


def login(request, user=None):
    return render(request, 'registration/login.html')


def signup(request):
    if request.method == 'POST':
        user_form = SignUpForm(request.POST)
        profile_form = ProfileForm(request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.refresh_from_db()  # load the profile instance created by the signal

            profile_form = ProfileForm(request.POST, instance=user.profile) 
            profile_form.full_clean()
            profile_form.save()

            return login(request, None)
    else:
        user_form = SignUpForm()
        profile_form = ProfileForm()
    
    return render(request, 'signup.html', {'user_form': user_form, 'profile_form': profile_form})