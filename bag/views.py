from django.shortcuts import render, redirect, reverse
from products.models import Product, InventoryProduct
from django.contrib.auth.decorators import login_required
from django.contrib import messages

# Create your views here.

@login_required
def view_bag(request):
    """Returns bag page"""
    return render(request, 'bag/bag.html')
