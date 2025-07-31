# cart/views.py
from django.shortcuts import render, redirect
from products.models import Product

def cart_add(request, product_id):
    product = Product.objects.get(id=product_id)
    cart = request.session.get('cart', {})
    cart[str(product_id)] = 1  # Default quantity
    request.session['cart'] = cart
    return redirect('home')

def view_cart(request):
    cart = request.session.get('cart', {})
    return render(request, 'cart/cart.html', {'cart': cart})

def add_to_cart(request, product_id):
    product = Product.objects.get(id=product_id)
    cart = request.session.get('cart', {})
    cart[product_id] = cart.get(product_id, 0) + 1
    request.session['cart'] = cart
    return redirect('products')