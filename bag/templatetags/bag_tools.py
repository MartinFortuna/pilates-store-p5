from django import template


register = template.Library()


@register.filter(name='calc_subtotal')
def calc_subtotal(price, quantity):
    return price * quantity


@register.filter(name='calc_total_quantity')
def calc_total_quantity(order):
    return sum(item.quantity for item in order.orderitems.all())