from django.shortcuts import render, redirect, get_object_or_404
from .models import Product, Order
from django.contrib.auth.decorators import login_required

def product_list(request):
    products = Product.objects.all()
    return render(request, 'store/product_list.html', {'products': products})

def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'store/product_detail.html', {'product': product})

@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    order, created = Order.objects.get_or_create(
        user=request.user,
        is_completed=False
    )
    # Add logic to handle order items
    return redirect('cart')

@login_required
def cart(request):
    order = Order.objects.filter(user=request.user, is_completed=False).first()
    return render(request, 'store/cart.html', {'order': order})