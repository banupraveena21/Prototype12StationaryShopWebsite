from django.db import models
from django.contrib.auth.models import User

class Product(models.Model):
    CATEGORY_CHOICES = [
        ('papers', 'Papers & Notebooks'),
        ('calculators', 'Calculators'),
        ('staplers', 'Staplers'),
        ('pens', 'Pens'),
        ('scissors', 'Scissors'),
    ]

    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='products/')
    price = models.DecimalField(max_digits=6, decimal_places=2)
    bulk_price = models.DecimalField(max_digits=6, decimal_places=2)
    rating = models.IntegerField(default=5)
    description = models.TextField(default='', help_text='Product description')
    features = models.TextField(default='', help_text='Add features, one per line')  
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES,blank=False,null=False)  

    def feature_list(self):
        return self.features.split('\n')
    def __str__(self):
        return self.name
    

class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message from {self.name}"
    

class Signup(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15)
    otp = models.CharField(max_length=10)

    def __str__(self):
        return self.email
    

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def total_price(self):
        return sum(item.total_price() for item in self.items.all())

    def __str__(self):
        return f"Cart #{self.id}"

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def unit_price(self):
        return self.product.price

    def total_price(self):
        if self.quantity >= 10:
            return self.product.bulk_price
        return self.product.price * self.quantity

    def __str__(self):
        return f"{self.product.name} x {self.quantity}"
    

class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def total_price(self):
        return self.product.price * self.quantity

class Order(models.Model):
    items = models.ManyToManyField(OrderItem)
    created_at = models.DateTimeField(auto_now_add=True)
    


