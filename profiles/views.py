from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import include, path, reverse

from profiles.forms import UserProfileForm, UserForm
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


@login_required
def order_history(request, order_number):
    # Bug here, function not being called. 
    print("Inside order_history view")
    order = get_object_or_404(Order, order_number=order_number)
    user_details = order.user.userdetails_set.first()

    messages.info(request, (
        f'This is a past confirmation for order number {order_number}.'
        'A confirmation email was sent on order date'
    ))

    template - 'checkout/checkout_success.html'
    context = {
        'order': order,
        'user_details': user_details,
        'from_userserfile': True,
    }

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

@login_required
def delete_profile(request):
    if request.method == 'POST':
        user = request.user
        profile = get_object_or_404(UserDetail, user_id=request.user)
        profile.delete()
        user.delete()
        messages.success(request, "Your profile was deleted")
        logout(request)
        return HttpResponseRedirect(reverse('home'))
    else:
        template = 'profiles/delete_profile.html'
        return render(request, template)
