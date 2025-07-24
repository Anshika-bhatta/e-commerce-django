from django.db import models
import datetime
from django.contrib.auth.models import User

class Category(models.Model):
    name =models.CharField(max_length=100)
    
    def __str__(self):
        return self.name
    
    # class Meta:
    #     verbose_name-plural = 'categories'

class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    first_name = models.CharField(max_length=50, default='')
    last_name = models.CharField(max_length=50, default='')
    phone = models.CharField(max_length=100, default='')
    email = models.EmailField(max_length=100, default='')
    password = models.CharField(max_length=50, default='')  
    
    def __str__(self):
        return f'{self.first_name} {self.last_name}'

class Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(default=0, max_digits=6, decimal_places=2)
    category = models. ForeignKey(Category, on_delete=models.CASCADE,default=1,null=True)
    description = models.CharField(max_length=100, default='', blank=True, null=True)
    image = models.ImageField(upload_to='upload/products/')
    is_featured = models.BooleanField(default=False)

def __str__(self):
    return self.name


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)  
    Customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product)
    quantity = models.IntegerField(default=1)
    total_price = models.FloatField(null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    status = models.CharField(max_length=20, default='Pending')
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order #{self.id} - {self.Product.name}"

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.quantity} x {self.product.name}"

    def total_price(self):
        return self.quantity * self.product.price
    
@property
def cart_set(self):
    return Cart.objects.filter(user=self)

@property
def total_price(self):
    return sum(item.total_price() for item in self.cart_set.all())


