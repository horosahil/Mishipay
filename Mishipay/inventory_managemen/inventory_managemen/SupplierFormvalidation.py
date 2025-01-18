from django import forms
from .models import Product, Supplier
from django.core.exceptions import ValidationError
from django.core.validators import EmailValidator, RegexValidator

class SupplierForm(forms.ModelForm):
    class Meta:
        model = Supplier
        fields = ['name', 'email', 'phone', 'address']

    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if Supplier.objects.filter(email=email).exists():
            raise ValidationError('Supplier with this email already exists.')
        try:
            EmailValidator()(email)
        except ValidationError:
            raise ValidationError('Invalid email format.')
        return email

 
    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        if Supplier.objects.filter(phone=phone).exists():
            raise ValidationError('Supplier with this phone number already exists.')
        phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
        phone_regex(phone) 
        return phone

   
    def clean_address(self):
        address = self.cleaned_data.get('address')
        if not address:
            raise ValidationError('Address cannot be empty.')
        return address
