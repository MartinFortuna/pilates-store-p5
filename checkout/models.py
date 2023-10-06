import uuid

from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum
from django.conf import settings
from products.models import Product, SizeProduct

# Create your models here.

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    order_number = models.CharField(max_length=32, null=True, editable=False)
    date = models.DateTimeField(auto_now_add=True)
    total_items = models.IntegerField(default=0)
    delivery_cost = models.DecimalField(max_digits=6, decimal_places=2, null=False, default=0)
    grand_total = models.DecimalField(max_digits=10, decimal_places=2, null=False, default=0)
    original_bag = models.TextField(null=False, blank=False, default='')
    stripe_pid = models.CharField(max_length=254, null=False, blank=False, default='')
    shipping_details_html = models.TextField(null=True, default='')

    def _generate_order_number(self):
        """
        Generate a random, unique order number using UUID
        """
        return uuid.uuid4().hex.upper()

    def update_total(self):
        """
        Update grand total each time a line item is added,
        accounting for delivery costs.
        """
        self.total_items = self.orderitems.aggregate(Sum('quantity'))['quantity__sum'] or 0
        self.grand_total = self.orderitems.aggregate(Sum('subtotal'))['subtotal__sum'] or 0
        if self.grand_total < settings.FREE_DELIVERY_THRESHOLD:
            self.delivery_cost = self.grand_total * settings.STANDARD_DELIVERY_PERCENTAGE / 100
        else:
            self.delivery_cost = 0
        self.grand_total = self.grand_total + self.delivery_cost
        self.save()

    def save(self, *args, **kwargs):
        """
        Override the original save method to set the order number
        if it hasn't been set already.
        """
        if not self.order_number:
            self.order_number = self._generate_order_number()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.order_number

class OrderItem(models.Model):
    order = models.ForeignKey(Order, null=False, blank=False, on_delete=models.CASCADE, related_name='orderitems')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(null=False, blank=False, default=0)
    size = models.CharField(max_length=20, null=True, blank=False)
    subtotal = models.DecimalField(max_digits=6, decimal_places=2, null=False, blank=False, editable=False)

    def save(self, *args, **kwargs):
        """
        Override the original save method to calculate the subtotal
        each time an item's quantity changes.
        """
        self.subtotal = self.product.price * self.quantity
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.product.name} on order {self.order.order_number}"