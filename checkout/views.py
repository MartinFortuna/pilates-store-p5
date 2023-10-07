from django.shortcuts import render, redirect, reverse, get_object_or_404, HttpResponse
from django.views.decorators.http import require_POST
from django.contrib import messages
from django.conf import settings

from .forms import CheckoutForm
from profiles.models import User, UserDetail
from products.models import Product, InventoryProduct
from .models import Order, OrderItem
from django.contrib.auth.decorators import login_required
from bag.contexts import bag_contents

import stripe
import json
from django.views.decorators.csrf import requires_csrf_token

# Create your views here.


@require_POST
def cache_checkout_data(request):
    try:
        pid = request.POST.get('client_secret').split('_secret')[0]
        stripe.api_key = settings.STRIPE_SECRET_KEY
        stripe.PaymentIntent.modify(pid, metadata={
            'bag': json.dumps(request.session.get('bag', {})),
            'username': request.user,
        })
        return HttpResponse(status=200)
    except Exception as e:
        messages.error(request, 'Sorry, your payment cannot be \
            processed right now. Please try again later.')
        return HttpResponse(content=e, status=400)


@login_required
def checkout(request):
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

        current_bag = bag_contents(request)
        total = current_bag['grand_total']
        stripe_total = round(total * 100)
        stripe.api_key = stripe_secret_key
        intent = stripe.PaymentIntent.create(
            amount=stripe_total,
            currency=settings.STRIPE_CURRENCY,
        )

        order_form = CheckoutForm(initial=initial_data)

        if request.method == "POST":
            order_form = CheckoutForm(request.POST)
            if order_form.is_valid():
                order = order_form.save(commit=False)
                pid = request.POST.get('client_secret').split('_secret')[0]
                order.stripe_pid = pid
                order.original_bag = json.dumps(bag)
                order.user_id = request.user.id

                shipping_details = {
                        'telephone': order_form.cleaned_data.get('telephone'),
                        'address1': order_form.cleaned_data.get('address1'),
                        'address2': order_form.cleaned_data.get('address2'),
                        'postal_code': order_form.cleaned_data.get('postal_code'),
                        'city': order_form.cleaned_data.get('city'),
                        'county': order_form.cleaned_data.get('county'),
                        'country': order_form.cleaned_data.get('country')
                    }

                order.shipping_details_html = f"<p>Telephone: {shipping_details.get('telephone')}</p>"
                order.shipping_details_html = f"{order.shipping_details_html}<p>Address1: {shipping_details.get('address1')}</p>"
                order.shipping_details_html = f"{order.shipping_details_html}<p>Address2: {shipping_details.get('address2')}</p>"
                order.shipping_details_html = f"{order.shipping_details_html}<p>City: {shipping_details.get('city')}</p>"
                order.shipping_details_html = f"{order.shipping_details_html}<p>County: {shipping_details.get('county')}</p>"
                order.shipping_details_html = f"{order.shipping_details_html}<p>Postal Code: {shipping_details.get('postal_code')}</p>"

                order.save()

                # Create OrderItem instances for each product in the bag
                for item_id, item_data in bag.items():
                    product = Product.objects.get(id=item_id)
                    if isinstance(item_data, int):
                        orderitems = OrderItem(
                            order=order,
                            product=product,
                            quantity=item_data,
                        )
                        orderitems.save()
                    else:
                        for size, quantity in item_data['items_by_size'].items():
                            inventory = InventoryProduct.objects.filter(id_product=product, id_size__size=size)
                            size_inventory = inventory.first()
                            orderitems = OrderItem(
                                order=order,
                                product=product,
                                size=size,
                                quantity=quantity,
                            )
                            orderitems.save()

                return redirect(reverse('checkout_success', args=[order.order_number]))
            else:
                messages.error(request, 'There was an error with your form. \
                    Please double check your information.')

    template = 'checkout/checkout.html'
    context = {
        'order_form': order_form,
        'stripe_public_key': stripe_public_key,
        'client_secret': intent.client_secret,
    }

    return render(request, template, context)


@login_required
def checkout_success(request, order_number):
    """
    Handle successful checkouts
    """
    user = request.user
    order = get_object_or_404(Order, order_number=order_number)
    messages.success(request, f'Order successfully processed! \
        Your order number is {order_number}.')

    if 'bag' in request.session:
        del request.session['bag']

    template = 'checkout/checkout_success.html'
    context = {
        'order': order,
    }

    return render(request, template, context)
