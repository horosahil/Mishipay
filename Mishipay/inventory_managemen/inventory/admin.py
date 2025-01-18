
from django.contrib import admin
from .models import Supplier, Product, SaleOrder, StockMovement

admin.site.register(Supplier)
admin.site.register(Product)
admin.site.register(SaleOrder)
admin.site.register(StockMovement)
