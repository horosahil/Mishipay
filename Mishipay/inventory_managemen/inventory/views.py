# from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from .models import Product, Supplier, SaleOrder, StockMovement
from django.db.models import Sum
from django.contrib import messages

def list_products(request):
    products = Product.objects.all()
    return render(request, 'inventory/list_products.html', {'products': products})

def add_product(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        category = request.POST.get('category')
        price = request.POST.get('price')
        stock_quantity = request.POST.get('stock_quantity')
        supplier_id = request.POST.get('supplier')

        # Check for duplicates
        if Product.objects.filter(name=name).exists():
            messages.error(request, "Product with this name already exists.")
            return redirect('add_product')

        supplier = get_object_or_404(Supplier, id=supplier_id)
        Product.objects.create(
            name=name,
            description=description,
            category=category,
            price=price,
            stock_quantity=stock_quantity,
            supplier=supplier
        )
        messages.success(request, "Product added successfully.")
        return redirect('list_products')

    suppliers = Supplier.objects.all()
    return render(request, 'inventory/add_product.html', {'suppliers': suppliers})

def list_suppliers(request):
    suppliers = Supplier.objects.all()
    return render(request, 'inventory/list_suppliers.html', {'suppliers': suppliers})

def add_supplier(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        address = request.POST.get('address')

        # Validate unique email and phone
        if Supplier.objects.filter(email=email).exists() or Supplier.objects.filter(phone=phone).exists():
            messages.error(request, "Supplier with this email or phone already exists.")
            return redirect('add_supplier')

        Supplier.objects.create(name=name, email=email, phone=phone, address=address)
        messages.success(request, "Supplier added successfully.")
        return redirect('list_suppliers')

    return render(request, 'inventory/add_supplier.html')

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

def create_sale_order(request):
    if request.method == 'POST':
        product_id = request.POST.get('product')
        quantity = int(request.POST.get('quantity'))

        product = get_object_or_404(Product, id=product_id)

        if product.stock_quantity < quantity:
            messages.error(request, "Insufficient stock to fulfill the order.")
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
    order.save()
    messages.success(request, "Sale order completed successfully.")
    return redirect('list_orders')

def check_stock_levels(request):
    products = Product.objects.all().values('name', 'stock_quantity')
    return JsonResponse(list(products), safe=False)
