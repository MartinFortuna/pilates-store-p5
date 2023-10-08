from django.shortcuts import render, redirect, reverse
from products.models import Product, InventoryProduct
from django.contrib.auth.decorators import login_required
from django.contrib import messages

# Create your views here.


@login_required
def view_bag(request):
    """ Returns bag page """
    return render(request, 'bag/bag.html')


@login_required
def add_to_bag(request, item_id):
    """ Add a quantity of the specified product to the shopping bag """
    product = Product.objects.get(id=item_id)
    quantity = int(request.POST.get('quantity'))
    redirect_url = request.POST.get('redirect_url')
    size = request.POST.get('size')
    bag = request.session.get('bag', {})
    inventory_item = InventoryProduct.objects.filter(
        id_product=product, id_size__size=size).first()

    if size:
        if item_id not in bag:
            bag[item_id] = {'items_by_size': {size: quantity}}
            messages.success(
                request,
                f'Added {bag[item_id]["items_by_size"][size]} '
                f'"{product.name}" size { inventory_item.id_size.size } '
                'to your bag'
            )
        else:
            if 'items_by_size' not in bag[item_id]:
                bag[item_id] = {'items_by_size': {size: quantity}}
                messages.success(
                    request,
                    f'Added {bag[item_id]["items_by_size"][size]} '
                    f'"{product.name}" size { inventory_item.id_size.size } '
                    'to your bag'
                )
            else:
                if size in bag[item_id]['items_by_size']:
                    bag[item_id]['items_by_size'][size] += quantity
                    messages.success(
                        request,
                        f'Updated quantity of "{product.name}" size '
                        f'{ inventory_item.id_size.size } to '
                        f'{bag[item_id]["items_by_size"][size]} in your bag'
                    )
                else:
                    bag[item_id]['items_by_size'][size] = quantity
                    success_message = (
                        f'Added {bag[item_id]["items_by_size"][size]} '
                        f'"{product.name}" size {inventory_item.id_size.size} '
                        'to your bag'
                    )
                    messages.success(request, success_message)
    else:
        if item_id in bag and isinstance(bag[item_id], int):
            bag[item_id] += quantity
            messages.success(
                request,
                f'Updated quantity of "{product.name}" to '
                f'{bag[item_id]} to in bag'
            )
        else:
            bag[item_id] = quantity
            messages.success(request, f'Added "{product.name}" to your bag')

    request.session['bag'] = bag
    return redirect(redirect_url)


@login_required
def remove_from_bag(request, item_id):
    """ Remove the specified product from the shopping bag """
    product = Product.objects.get(id=item_id)
    size = request.POST.get('size')
    bag = request.session.get('bag', {})
    inventory_item = InventoryProduct.objects.filter(
        id_product=product, id_size__size=size).first()

    if size:
        del bag[item_id]['items_by_size'][size]
        success_message = (
            f'Deleted  all "{product.name}" products size '
            f'{ inventory_item.id_size.size } from your bag'
        )
        messages.success(request, success_message)
        if not bag[item_id]['items_by_size']:
            del bag[item_id]
    else:
        del bag[item_id]
        messages.success(
            request,
            f'Deleted  all "{product.name}" products from your bag'
        )
    request.session['bag'] = bag

    return redirect(reverse('bag'))


@login_required
def update_bag(request, item_id):
    """ Update the quantity of the specified product on the bag"""
    redirect_url = request.POST.get('redirect_url')
    str_quantity = request.POST.get('quantity')
    if str_quantity == '' or str_quantity is None:
        return redirect(redirect_url)

    product = Product.objects.get(id=item_id)
    quantity = int(str_quantity)
    size = request.POST.get('size')
    bag = request.session.get('bag', {})
    inventory_item = InventoryProduct.objects.filter(
        id_product=product, id_size__size=size).first()

    if size:
        if item_id in bag and 'items_by_size' in bag[item_id] and \
           size in bag[item_id]['items_by_size']:
            if quantity > 0:
                bag[item_id]['items_by_size'][size] = quantity
            success_message = (
                f'Updated quantity of "{product.name}" size '
                f'{ inventory_item.id_size.size } to '
                f'{bag[item_id]["items_by_size"][size]} in your bag'
            )
            messages.success(request, success_message)
        else:
            del bag[item_id]['items_by_size'][size]
            if not bag[item_id]['items_by_size']:
                del bag[item_id]
    else:
        if quantity > 0:
            bag[item_id] = quantity
            success_message = (
                f'Updated quantity of "{product.name}" to '
                f'{bag[item_id]} in your bag'
            )
            messages.success(request, success_message)

    request.session['bag'] = bag
    return redirect(redirect_url)
