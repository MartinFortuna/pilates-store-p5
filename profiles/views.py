from django.urls import path
from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from profiles.models import UserDetail

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
