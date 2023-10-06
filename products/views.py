from django.shortcuts import render, redirect, reverse
from django.contrib.auth.decorators import login_required
from django.db.models import Avg, Value, FloatField
from django.db.models.functions import Coalesce
from django.db.models import Q
from django.contrib import messages

from products.models import Product, RateProduct, CategoryProduct

# Create your views here.

@login_required
def all_products(request):
    """Show all products to authenticated users only
    including search and filtering features."""
    products = Product.objects.all().annotate(
        avg_rating=Coalesce(Avg('rateproduct__rate'), Value(0), output_field=FloatField())
    )
    ratings = RateProduct.objects.all()
    query = None
    categories = None
    direction = None
    sort_key = None
    sort_order = None

    if request.GET:

        if 'q' in request.GET:
            query = request.GET['q']
            if not query:
                messages.error(request, "You didn't enter any search criteria!")
                return redirect(reverse('products'))

            queries = Q(name__icontains=query) | Q(description__icontains=query)
            products = products.filter(queries)

        if not products.exists():
            messages.error(request, "Nothing matches your search criteria!")
            return redirect(reverse('products'))

        if 'category' in request.GET:
            categories = request.GET['category'].split(',')
            products = products.filter(category_id__name__in=categories)
            category = CategoryProduct.objects.filter(name__in=categories)

        if 'sort' in request.GET:
            sort_key = request.GET['sort']
            sort_order = request.GET.get('order', 'asc')
            if sort_key == 'price':
                if sort_order == 'desc':
                    products = products.order_by('-price')
                else:
                    products = products.order_by('price')
            elif sort_key == 'rating':
                if sort_order == 'desc':
                    products = products.order_by('-avg_rating')
                else:
                    products = products.order_by('avg_rating')

    context = {
        'products': products,
        'ratings': ratings,
        'search_term': query,
        'current_category': categories,
    }

    template = 'products/products.html'
    return render(request, template, context)
