from django.urls import path
from . import views

urlpatterns = [
    path('', views.product_list, name='product_list'),  # /products/
    path('<int:pk>/', views.product_detail, name='detail'),  # /products/1/
]