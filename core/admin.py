from django.contrib import admin
from .models import Product,Cart,DeliveryAdress,OrderDetail,Order
# Register your models here.
admin.site.register(Product)
admin.site.register(Cart)
admin.site.register(DeliveryAdress)
admin.site.register(OrderDetail)
admin.site.register(Order)
