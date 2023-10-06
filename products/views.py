from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from products.models import Product

# Create your views here.

@login_required
def all_products(request):
    """Show all products to authenticated users only
    including search and filtering features."""
    products = Product.objects.all()

    context = {
        'products': products
    }

    template = 'products/products.html'
    return render(request, template, context)