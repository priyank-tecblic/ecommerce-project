from django.db import models
from django.contrib.auth.models import User

# Create your models here
class Product(models.Model):
    pid = models.AutoField(primary_key=True)
    pname = models.CharField(max_length=50)
    pdesc = models.CharField(max_length=100,default="")
    pcategory = models.CharField(max_length=30,default="")
    psubcategory = models.CharField( max_length=50,default="")
    price = models.IntegerField(default=0)
    pdate = models.DateField()
    image = models.ImageField(upload_to="shop/image",default="")

    def __str__(self):
        return self.pname

class Cart(models.Model):
    cid = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0)
    price = models.IntegerField(default=0)
    total = models.IntegerField(default=0)
    def __str__(self):
        return self.product.pname+"  for "+self.user.username

class Order(models.Model):
    oid = models.AutoField(primary_key=True)
    user = models.ForeignKey(User,on_delete=models.CASCADE)

class OrderDetail(models.Model):
    odid = models.AutoField(primary_key=True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0)
    price = models.IntegerField(default=0)
    total = models.IntegerField(default=0)

class DeliveryAdress(models.Model):
    did = models.AutoField(primary_key=True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    email = models.CharField(max_length=50)
    add1 = models.CharField(max_length=100)
    add2 = models.CharField(max_length=200)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=30)
    zip = models.CharField(max_length=10)
    phone =models.CharField(max_length=10)