Python code
from .models import Product, Order, OrderItem
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required

def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    return render(request, 'store/product_detail.html', {'product': product})

@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    order, created = Order.objects.get_or_create(user=request.user, is_active=True)
    order_item, created = OrderItem.objects.get_or_create(order=order, product=product)
    order_item.quantity += 1
    order_item.save()
    return redirect('cart')

@login_required
def view_cart(request):
    order = Order.objects.get(user=request.user, is_active=True)
    return render(request, 'store/cart.html', {'order': order})

@login_required
def update_cart(request, order_item_id, action):
    order_item = get_object_or_404(OrderItem, id=order_item_id)
    if action == "increase":
        order_item.quantity += 1
    elif action == "decrease" and order_item.quantity > 1:
        order_item.quantity -= 1
    order_item.save()
    return redirect('cart')
