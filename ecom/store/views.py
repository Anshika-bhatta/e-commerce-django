from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.db import transaction
from .models import Product, Cart, Order, Customer
from .forms import SignUpForm
import logging
from django.core.mail import send_mail
from django.conf import settings

logger = logging.getLogger(__name__)

# Authentication Views
def home(request):
    products = Product.objects.all()
    return render(request, 'home.html', {'products': products})
    featured_products = Product.objects.filter(is_featured=True)[:4]
    return render(request, 'index.html', {'featured_products': featured_products})

def about(request):
    return render(request, 'about.html')

def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')
        send_mail(
            f'Contact from {name}',
            message,
            email,
            [settings.EMAIL_HOST_USER],
            fail_silently=False,
        )
        return redirect('home')
    return render(request, 'contact.html')


def login_user(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "Login successful!")
            return redirect('home')
        messages.error(request, "Invalid credentials. Please try again.")
    return render(request, 'login.html')

def logout_user(request):
    logout(request)
    messages.success(request, "You've been logged out.")
    return redirect('home')

def register_user(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful!")
            return redirect('home')
        messages.error(request, "Registration failed. Please correct the errors.")
    else:
        form = SignUpForm()
    return render(request, 'register.html', {'form': form})

# Cart Views
@login_required
def view_cart(request):
    cart_items = Cart.objects.filter(user=request.user)
    total_price = sum(item.total_price() for item in cart_items)
    return render(request, 'cart.html', {
        'cart_items': cart_items,
        'total_price': total_price
    })

@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart_item, created = Cart.objects.get_or_create(
        user=request.user,
        product=product,
        defaults={'quantity': 1}
    )
    if not created:
        cart_item.quantity += 1
        cart_item.save()
    messages.success(request, f"Added {product.name} to your cart.")
    return redirect('view_cart')

@login_required
def remove_from_cart(request, cart_item_id):
    cart_item = get_object_or_404(Cart, id=cart_item_id, user=request.user)
    cart_item.delete()
    messages.success(request, "Item removed from cart.")
    return redirect('view_cart')

@login_required
def update_cart(request, cart_item_id):
    cart_item = get_object_or_404(Cart, id=cart_item_id, user=request.user)
    if request.method == 'POST':
        quantity = int(request.POST.get('quantity', 1))
        if quantity > 0:
            cart_item.quantity = quantity
            cart_item.save()
            messages.success(request, "Cart updated.")
        else:
            cart_item.delete()
            messages.success(request, "Item removed.")
    return redirect('view_cart')

# Payment Views
@login_required
def checkout(request):
    cart_items = Cart.objects.filter(user=request.user)
    if not cart_items:
        messages.warning(request, "Your cart is empty.")
        return redirect('view_cart')
    return render(request, 'checkout.html')

@login_required
@transaction.atomic
def process_payment(request):
    if request.method != 'POST':
        messages.error(request, "Invalid request method.")
        return redirect('checkout')
    
    try:
        # Get existing customer (must exist in database)
        customer = Customer.objects.get(user=request.user)
        
        # Get cart items
        cart_items = Cart.objects.filter(user=request.user)
        if not cart_items:
            messages.error(request, "Your cart is empty.")
            return redirect('view_cart')
        
        # Create order for each product in cart
        for cart_item in cart_items:
            Order.objects.create(
                Customer=customer,  
                Product=cart_item.product,  
                quantity=cart_item.quantity,
                total=cart_item.total_price(),
                status=True
            )
        
        # Clear cart
        cart_items.delete()
        
        messages.success(request, "Order created successfully!")
        return redirect('payment_success')
    
    except Customer.DoesNotExist:
        messages.error(request, "Customer profile not found. Please contact support.")
        return redirect('checkout')
    except Exception as e:
        logger.error(f"Payment error: {str(e)}")
        messages.error(request, "Payment processing failed. Please try again.")
        return redirect('checkout')

def payment_success(request):
    return render(request, 'payment_success.html')

def payment_cancelled(request):
    messages.info(request, "Payment was cancelled.")
    return render(request, 'payment_cancelled.html')

@login_required
def order_history(request):
    orders = Order.objects.filter(user=request.user)
    return render(request, 'order_history.html', {'orders': orders})

def search(request):
    query = request.GET.get('q')
    products = Product.objects.filter(name__icontains=query) if query else []
    return render(request, 'search.html', {'products': products, 'query': query})