from django.shortcuts import (
    render,
    redirect,
    reverse,
    get_object_or_404,
    HttpResponse
)
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.conf import settings


from .forms import CheckoutForm
from profiles.models import User, UserDetail

# Create your views here.


@login_required
def checkout(request):
    """ User checkout """
    stripe_public_key = settings.STRIPE_PUBLIC_KEY
    stripe_secret_key = settings.STRIPE_SECRET_KEY

    bag = request.session.get('bag', {})
    if not bag:
        messages.error(request, "No products in your bag yet!")
        return redirect(reverse('products'))
    else:
        user_details = UserDetail.objects.filter(user_id=request.user.id).first()
        if user_details is not None:
            initial_data = {
                'username': request.user.username,
                'email': request.user.email,
                'first_name': request.user.first_name,
                'last_name': request.user.last_name,
                'telephone': user_details.telephone,
                'address1': user_details.address1,
                'address2': user_details.address2,
                'postal_code': user_details.postal_code,
                'city': user_details.city,
                'county': user_details.county,
            }
        else:
            initial_data = {
                'username': request.user.username,
                'email': request.user.email,
                'first_name': request.user.first_name,
                'last_name': request.user.last_name,
            }

        order_form = CheckoutForm(initial=initial_data)

    template = 'checkout/checkout.html'
    context = {
        'order_form': order_form,
        'stripe_public_key': stripe_public_key,
        'client_secret': 'test client secret'
    }
    return render(request, template, context)