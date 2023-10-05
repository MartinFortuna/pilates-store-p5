from django.urls import path, include, reverse
from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from profiles.models import UserDetail
from profiles.forms import UserForm, UserProfileForm
from django.contrib import messages
from django.http import HttpResponseRedirect

# Create your views here.


@login_required
def user_profile(request):
    """Display the user's profile"""
    user = request.user
    profiles = UserDetail.objects.filter(user_id=request.user)

    context = {
        'profiles': profiles,
    }

    template = 'profiles/user_profile.html'
    return render(request, template, context)


@login_required
def update_profile(request):
    """ Updates the profile info"""
    user = request.user
    profile, created = UserDetail.objects.get_or_create(user_id=user)

    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=user)
        profile_form = UserProfileForm(request.POST, instance=profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your profile was updated!')
            return HttpResponseRedirect(reverse('user_profile'))
        else:
            messages.error(request, 'Your profile was not updated, check the form')
    else:
        user_form = UserForm(instance=user)
        profile_form = UserProfileForm(instance=profile)

    context = {
        'user_form': user_form,
        'profile_form': profile_form,
    }

    template = 'profiles/update_profile.html'
    return render(request, template, context)
