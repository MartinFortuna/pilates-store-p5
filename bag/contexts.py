from decimal import Decimal
from django.conf import settings
from django.shortcuts import get_object_or_404
from products.models import Product


def bag_contents(request):
    bag_items = []
    total = 0
    product_count = 0
    bag = request.session.get('bag', {})

    delivery_cost_percentage = Decimal(settings.STANDARD_DELIVERY_PERCENTAGE) / Decimal(100)
    free_delivery_threshold = settings.FREE_DELIVERY_THRESHOLD

    if total < free_delivery_threshold:
        delivery = total * delivery_cost_percentage
    else:
        delivery = 0
        free_delivery_delta = 0
    if total >= 100.00:
        delivery = 0
        delivery_display = "Free Delivery"
    else:
        delivery = total * delivery_cost_percentage
        delivery_display = f"€{delivery:.2f}"
        free_delivery_delta = free_delivery_threshold - total

    grand_total = delivery + total

    context = {
        'bag_items': bag_items,
        'total': total,
        'product_count': product_count,
        'delivery': delivery,
        'free_delivery_delta': free_delivery_delta,
        'free_delivery_threshold': free_delivery_threshold,
        'delivery_display': delivery_display,
        'grand_total': grand_total,
    }

    return context
