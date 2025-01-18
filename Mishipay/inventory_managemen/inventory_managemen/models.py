from django.db import models
from django.core.exceptions import ValidationError

class Supplier(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=10, unique=True)
    address = models.TextField()

    def clean(self):
       
        if len(self.phone) != 10:
            raise ValidationError({'phone': 'Phone number must be exactly 10 digits.'})

        
        if not self.phone.isdigit():
            raise ValidationError({'phone': 'Phone number must contain only digits.'})

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField()
    category = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock_quantity = models.PositiveIntegerField()
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE)

    def clean(self):
      
        if self.price <= 0:
            raise ValidationError({'price': 'Price must be greater than zero.'})

        
        if self.stock_quantity < 0:
            raise ValidationError({'stock_quantity': 'Stock quantity cannot be negative.'})

    def __str__(self):
        return self.name

class SaleOrder(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Completed', 'Completed'),
        ('Cancelled', 'Cancelled'),
    ]
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    sale_date = models.DateField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES)

    def clean(self):
      
        if self.quantity <= 0:
            raise ValidationError({'quantity': 'Quantity must be greater than zero.'})

        
        if self.quantity > self.product.stock_quantity:
            raise ValidationError({'quantity': 'Not enough stock available.'})


        if self.total_price != self.product.price * self.quantity:
            raise ValidationError({'total_price': 'Total price must match product price * quantity.'})

    def __str__(self):
        return f"Order {self.id} - {self.status}"

class StockMovement(models.Model):
    MOVEMENT_TYPES = [
        ('In', 'In'),
        ('Out', 'Out'),
    ]
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    movement_type = models.CharField(max_length=10, choices=MOVEMENT_TYPES)
    movement_date = models.DateField(auto_now_add=True)
    notes = models.TextField(null=True, blank=True)

    def clean(self):
       
        if self.quantity <= 0:
            raise ValidationError({'quantity': 'Quantity must be greater than zero.'})

       
        if self.movement_type == 'Out' and self.product.stock_quantity - self.quantity < 0:
            raise ValidationError({'quantity': 'Not enough stock available for this movement.'})

    def __str__(self):
        return f"{self.movement_type} - {self.product.name}"
