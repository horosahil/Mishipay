from django import forms
from .models import Product, Supplier
from django.core.exceptions import ValidationError

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'category', 'price', 'stock_quantity', 'supplier']

 
    def clean_price(self):
        price = self.cleaned_data.get('price')
        if price <= 0:
            raise ValidationError('Price must be a positive value.')
        return price

    
    def clean_stock_quantity(self):
        stock_quantity = self.cleaned_data.get('stock_quantity')
        if stock_quantity < 0:
            raise ValidationError('Stock quantity cannot be negative.')
        return stock_quantity

  
    def clean_supplier(self):
        supplier = self.cleaned_data.get('supplier')
        if supplier is None:
            raise ValidationError('Please select a supplier.')
        return supplier
