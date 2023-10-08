from django.http import HttpResponse
from django.conf import settings

from .models import Order, OrderItem
from products.models import Product

from django.contrib.auth.models import User
from profiles.models import UserDetail

import json
import time
import stripe


class StripeWH_Handler:
    """Handle Stripe webhooks"""

    def __init__(self, request):
        self.request = request

    def handle_event(self, event):
        """
        Handle a generic/unknown/unexpected webhook event
        """
        return HttpResponse(
            content=f'Unhandled webhook received: {event["type"]}',
            status=200)

    def handle_payment_intent_succeeded(self, event):
        """
        Handle the payment_intent.succeeded webhook from Stripe
        """
        intent = event.data.object
        pid = intent.id
        bag = intent.metadata.bag

        stripe_charge = stripe.Charge.retrieve(
            intent.latest_charge
        )

        billing_details = stripe_charge.billing_details
        shipping_details = intent.shipping
        grand_total = round(stripe_charge.amount / 100, 2)

        # Clean data in the shipping details
        for field, value in shipping_details.address.items():
            if value == "":
                shipping_details.address[field] = None

            try:
                user = User.objects.get(
                    username=billing_details.name,
                    email=billing_details.email
                )

                shipping_details = {
                    'telephone': billing_details.phone,
                    'address1': shipping_details.address.line1,
                    'address2': shipping_details.address.line2,
                    'city': shipping_details.address.city,
                    'county': shipping_details.address.state
                }

                order_exists = False
                attempt = 1
                while attempt <= 5:
                    try:
                        order = Order.objects.get(
                            user=user,
                            grand_total=grand_total,
                            original_bag=bag,
                            stripe_pid=pid,
                        )
                        order_exists = True
                        break
                    except Order.DoesNotExist:
                        attempt += 1
                        time.sleep(1)
                if order_exists:
                    self._send_confirmation_email(order)
                    return HttpResponse(
                        content=(
                            f'Webhook received: {event["type"]} | '
                            f'SUCCESS: Verified order already in database'
                        ),
                        status=200
                    )
                else:
                    if not order_exists:
                        shipping_details_html += (
                            f"<p>Telephone: "
                            f"{shipping_details.get('telephone')}</p>"
                        )
                        shipping_details_html += (
                            f"<p>Address1: "
                            f"{shipping_details.get('address1')}</p>"
                        )
                        shipping_details_html += (
                            f"<p>Address2: "
                            f"{shipping_details.get('address2')}</p>"
                        )
                        shipping_details_html += (
                            f"<p>City: "
                            f"{shipping_details.get('city')}</p>"
                        )
                        shipping_details_html += (
                            f"<p>County: "
                            f"{shipping_details.get('county')}</p>"
                        )

                        order = Order.objects.create(
                            user=user,
                            shipping_details_html=shipping_details_html,
                            grand_total=grand_total,
                            original_bag=bag,
                            stripe_pid=pid,
                        )

                    for item_id, item_data in json.loads(bag).items():
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
                                orderitems = OrderItem(
                                    order=order,
                                    product=product,
                                    size=size,
                                    quantity=quantity,
                                )
                                orderitems.save()

            except Exception as e:
                if order:
                    order.delete()
                return HttpResponse(
                    content=f'Webhook received: {event["type"]} | ERROR: {e}',
                    status=500)
            self._send_confirmation_email(order)
            return HttpResponse(
                content=(
                    f'Webhook received: {event["type"]} '
                    f'| SUCCESS: Created order in webhook'
                ),
                status=200
            )

    def handle_payment_intent_payment_failed(self, event):
        """
        Handle the payment_intent.payment_failed webhook from Stripe
        """
        return HttpResponse(
            content=f'Webhook received: {event["type"]}',
            status=200)
