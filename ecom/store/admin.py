from django.contrib import admin
from .models import (Category, Product, Customer, 
                    Order, OrderItem, Cart,
                    About, Contact)

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'stock', 'available')
    list_filter = ('available', 'category')
    list_editable = ('price', 'stock', 'available')
    search_fields = ('name', 'description')
    readonly_fields = ('created', 'updated')

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer', 'date_ordered', 'complete')
    list_filter = ('complete', 'date_ordered')
    inlines = [OrderItemInline]

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'quantity', 'created_at')
    list_filter = ('created_at',)

@admin.register(About)
class AboutAdmin(admin.ModelAdmin):
    list_display = ('title', 'last_updated')
    readonly_fields = ('last_updated',)
    
    def has_add_permission(self, request):
        return not About.objects.exists()

@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'subject', 'submitted_at', 'is_resolved')
    list_filter = ('is_resolved', 'submitted_at')
    search_fields = ('name', 'email', 'subject')
    readonly_fields = ('submitted_at',)
    list_editable = ('is_resolved',)