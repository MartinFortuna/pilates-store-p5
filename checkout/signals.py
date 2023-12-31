from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from checkout.models import OrderItem


@receiver(post_save, sender=OrderItem)
def update_on_save(sender, instance, created, **kwargs):
    """
    Update order total on orderitem update/create
    """
    instance.order.update_total()


@receiver(post_delete, sender=OrderItem)
def update_on_save(sender, instance, **kwargs):
    """
    Update order total on orderitem update/create
    """
    instance.order.update_total()
