from django.http import HttpResponse
from django.core.mail import send_mail
from django.template.loader import render_to_string
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

    def _send_confirmation_email(self, order):
        """Send the user a confirmation email"""
        customer_email = order.user.email
        # user_details = order.user.userdetail_set.first() // Mofidy the emails, remove user_details and use order. 
        subject = render_to_string(
            'checkout/confirmation_emails/confirmation_email_subject.txt',
            {'order': order})
        body = render_to_string(
            'checkout/confirmation_emails/confirmation_email_body.txt',
            {'order': order, 'contact_email': settings.DEFAULT_FROM_EMAIL})

        send_mail(
            subject,
            body,
            settings.DEFAULT_FROM_EMAIL,
            [customer_email]
        )

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
        save_info = intent.metadata.save_info

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
                        content=f'Webhook received: {event["type"]} | SUCCESS: Verified order already in database',
                        status=200)
                else:
                    if not order_exists:
                        shipping_details_html = f"<p>Telephone: {shipping_details.get('telephone')}</p>"
                        shipping_details_html += f"<p>Address1: {shipping_details.get('address1')}</p>"
                        shipping_details_html += f"<p>Address2: {shipping_details.get('address2')}</p>"
                        shipping_details_html += f"<p>City: {shipping_details.get('city')}</p>"
                        shipping_details_html += f"<p>County: {shipping_details.get('county')}</p>"
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
                content=f'Webhook received: {event["type"]} | SUCCESS: Created order in webhook',
                status=200)

    def handle_payment_intent_payment_failed(self, event):
        """
        Handle the payment_intent.payment_failed webhook from Stripe
        """
        return HttpResponse(
            content=f'Webhook received: {event["type"]}',
            status=200)