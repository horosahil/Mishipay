from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from .models import Product, Supplier, SaleOrder, StockMovement
from .forms import ProductForm, SupplierForm
from django.contrib import messages
from django.db.models import Sum

from django.contrib import messages
from .models import StockMovement, Product
from .forms import ProductForm



def delete_supplier(request, id):
    
    supplier = get_object_or_404(Supplier, id=id)
    
   
    supplier.delete()
    
 
    messages.success(request, "Supplier deleted successfully.")
    return redirect('list_suppliers')

def edit_supplier(request, id):
 
    supplier = get_object_or_404(Supplier, id=id)

    if request.method == 'POST':
       
        form = SupplierForm(request.POST, instance=supplier)
        if form.is_valid():
            
            form.save()
            messages.success(request, "Supplier updated successfully.")
            return redirect('list_suppliers')
        else:
            messages.error(request, "There was an error updating the supplier.")
    else:
        
        form = SupplierForm(instance=supplier)

    return render(request, 'inventory/edit_supplier.html', {'form': form, 'supplier': supplier})


def home(request):
    return render(request, 'inventory/home.html')

def edit_product(request, id):
    product = get_object_or_404(Product, id=id)

    return render(request, 'edit_product.html', {'product': product})



def list_products(request):
  
    products = Product.objects.all()

    
    name = request.GET.get('name', '')
    if name:
        products = products.filter(name__icontains=name)

    price_min = request.GET.get('price_min')
    price_max = request.GET.get('price_max')
    if price_min:
        products = products.filter(price__gte=price_min)
    if price_max:
        products = products.filter(price__lte=price_max)

    stock_min = request.GET.get('stock_min')
    stock_max = request.GET.get('stock_max')
    if stock_min:
        products = products.filter(stock_quantity__gte=stock_min)
    if stock_max:
        products = products.filter(stock_quantity__lte=stock_max)

    
    if 'reset_filters' in request.GET:
       
        return redirect('list_products')  

    return render(request, 'inventory/list_products.html', {'products': products})




def add_product(request):
    if request.method == 'POST':
       
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()  
            messages.success(request, "Product added successfully.")
            return redirect('list_products')  
        else:
            messages.error(request, "Please fix the errors below.")
    else:
        form = ProductForm()  

    return render(request, 'inventory/add_product.html', {'form': form})


def list_suppliers(request):
    suppliers = Supplier.objects.all()
    return render(request, 'inventory/list_suppliers.html', {'suppliers': suppliers})

def add_supplier(request):
    if request.method == 'POST':
        form = SupplierForm(request.POST)
        
        if form.is_valid():
           
            email = form.cleaned_data.get('email')
            phone = form.cleaned_data.get('phone')

            
            if Supplier.objects.filter(email=email).exists():
                messages.error(request, "A supplier with this email already exists.")
                return redirect('add_supplier')

            if Supplier.objects.filter(phone=phone).exists():
                messages.error(request, "A supplier with this phone number already exists.")
                return redirect('add_supplier')

          
            form.save()
            messages.success(request, "Supplier added successfully.")
            return redirect('list_suppliers')

        else:
            messages.error(request, "There was an error adding the supplier. Please check the form.")
    else:
        form = SupplierForm()

    return render(request, 'inventory/add_supplier.html', {'form': form})

def add_stock_movement(request):
    if request.method == 'POST':
        product_id = request.POST.get('product')
        quantity = int(request.POST.get('quantity'))
        movement_type = request.POST.get('movement_type')
        notes = request.POST.get('notes')

        product = get_object_or_404(Product, id=product_id)

        if movement_type == 'Out' and product.stock_quantity < quantity:
            messages.error(request, "Insufficient stock for this movement.")
            return redirect('add_stock_movement')

        StockMovement.objects.create(
            product=product,
            quantity=quantity,
            movement_type=movement_type,
            notes=notes
        )

        if movement_type == 'In':
            product.stock_quantity += quantity
        elif movement_type == 'Out':
            product.stock_quantity -= quantity

        product.save()
        messages.success(request, "Stock movement recorded successfully.")
        return redirect('list_products')

    products = Product.objects.all()
    return render(request, 'inventory/add_stock_movement.html', {'products': products})


from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Product, SaleOrder

def create_sale_order(request):
    
    pending_orders_count = SaleOrder.objects.filter(status='Pending').count()

    if request.method == 'POST':
        product_id = request.POST.get('product')
        quantity = int(request.POST.get('quantity'))

        product = get_object_or_404(Product, id=product_id)

    
        if product.stock_quantity < quantity:
            messages.error(request, "Insufficient stock to fulfill the order.")
            return redirect('create_sale_order')  

     
        if pending_orders_count >= 5:  
            messages.error(request, "There are too many pending orders. Please try again later.")
            return redirect('create_sale_order')

        total_price = product.price * quantity
        SaleOrder.objects.create(
            product=product,
            quantity=quantity,
            total_price=total_price,
            status='Pending'
        )

       
        product.stock_quantity -= quantity
        product.save()

        messages.success(request, "Sale order created successfully.")
        return redirect('list_orders')  
    products = Product.objects.all()
    return render(request, 'inventory/create_sale_order.html', {'products': products})

def list_orders(request):
    orders = SaleOrder.objects.all()
    return render(request, 'inventory/list_orders.html', {'orders': orders})


def cancel_sale_order(request, id):
    order = get_object_or_404(SaleOrder, id=id)

    if order.status != 'Pending':
        messages.error(request, "Only pending orders can be canceled.")
        return redirect('list_orders')

    order.status = 'Cancelled'
    order.product.stock_quantity += order.quantity
    order.product.save()
    order.save()
    messages.success(request, "Sale order canceled successfully.")
    return redirect('list_orders')


def complete_sale_order(request, id):
    order = get_object_or_404(SaleOrder, id=id)

    if order.status != 'Pending':
        messages.error(request, "Only pending orders can be completed.")
        return redirect('list_orders')

    order.status = 'Completed'
    order.product.stock_quantity -= order.quantity
    order.product.save()
    order.save()
    messages.success(request, "Sale order completed successfully.")
    return redirect('list_orders')


def check_stock_levels(request):
    products = Product.objects.all()  
    return render(request, 'inventory/check_stock_levels.html', {'products': products})

def edit_product(request, id):
    product = get_object_or_404(Product, id=id)
    suppliers = Supplier.objects.all()  
    if request.method == 'POST':
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
           
            form.save()
            messages.success(request, "Product updated successfully.")
            return redirect('list_products')
        else:
            
            print(form.errors)
            messages.error(request, "There was an error updating the product.")
    else:
        form = ProductForm(instance=product)

    return render(request, 'inventory/edit_product.html', {'form': form, 'product': product, 'suppliers': suppliers})

def delete_product(request, id):
    product = get_object_or_404(Product, id=id)  
    product.delete()
    
   
    messages.success(request, "Supplier deleted successfully.")
    return redirect('list_products')


def edit_stock_movement(request, id):
    stock_movement = get_object_or_404(StockMovement, id=id)  

    if request.method == 'POST':
        form = StockMovementForm(request.POST, instance=stock_movement)  
        if form.is_valid():
            
            form.save()
            messages.success(request, "Stock movement updated successfully.")
            return redirect('list_products')  
        else:
            messages.error(request, "There was an error updating the stock movement.")
    else:
        form = StockMovementForm(instance=stock_movement)  

    return render(request, 'inventory/edit_stock_movement.html', {'form': form, 'stock_movement': stock_movement})
