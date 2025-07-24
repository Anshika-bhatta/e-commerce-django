from django.urls import path
from . import views, api 

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('orders/', views.order_history, name='order_history'),
    path('search/', views.search, name='search'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('register/', views.register_user, name='register'),
    path('cart/', views.view_cart, name='view_cart'),
    path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('remove-from-cart/<int:cart_item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('update-cart/<int:cart_item_id>/', views.update_cart, name='update_cart'),
    
    path('checkout/', views.checkout, name='checkout'),
    path('process-payment/', views.process_payment, name='process_payment'),
    path('payment/success/', views.payment_success, name='payment_success'),
    path('payment/cancelled/', views.payment_cancelled, name='payment_cancelled'),
    
    # APIs
    path('api/search/', api.product_search_api, name='product_search_api'),
    path('api/orders/', api.order_history_api, name='order_history_api'),
    path('api/featured/', api.featured_products_api, name='featured_products_api'),
    
]