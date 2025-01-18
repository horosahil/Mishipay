from django.urls import path
from . import views
from django.shortcuts import redirect


from django.urls import path
from . import views

urlpatterns = [

    path('', views.home, name='home'),

  
    path('products/', views.list_products, name='list_products'),
    path('products/add/', views.add_product, name='add_product'),
    path('products/edit/<int:id>/', views.edit_product, name='edit_product'),  
    path('products/delete/<int:id>/', views.delete_product, name='delete_product'),  

  
    path('suppliers/', views.list_suppliers, name='list_suppliers'),
    path('suppliers/add/', views.add_supplier, name='add_supplier'),
    path('suppliers/edit/<int:id>/', views.edit_supplier, name='edit_supplier'),  
    path('suppliers/delete/<int:id>/', views.delete_supplier, name='delete_supplier'),  

    path('stock/add/', views.add_stock_movement, name='add_stock_movement'),
    path('stock/edit/<int:id>/', views.edit_stock_movement, name='edit_stock_movement'),  


    path('orders/', views.list_orders, name='list_orders'),
    path('orders/add/', views.create_sale_order, name='create_sale_order'),
    path('orders/cancel/<int:id>/', views.cancel_sale_order, name='cancel_sale_order'),
    path('orders/complete/<int:id>/', views.complete_sale_order, name='complete_sale_order'),

   
    path('stock/check/', views.check_stock_levels, name='check_stock_levels'),
]
