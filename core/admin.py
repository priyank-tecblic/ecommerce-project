from django.contrib import admin
from .models import Product,Cart,DeliveryAdress,OrderDetail,Order,TrackOrder,Coupen
# Register your models here.
admin.site.register(Product)
admin.site.register(Cart)
admin.site.register(DeliveryAdress)
admin.site.register(OrderDetail)
admin.site.register(Order)
admin.site.register(TrackOrder)
admin.site.register(Coupen)
