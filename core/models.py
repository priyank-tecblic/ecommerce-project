from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now

# Create your models here
class CustomUser(models.Model):
    uid = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    email = models.CharField(max_length=40)
    password = models.CharField(max_length=100)
    def __str__(self):
        return self.first_name + " "+ self.last_name

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

    def delete(self, *args, **kwargs):
        # You have to prepare what you need before delete the model
        storage, path = self.image.storage, self.image.path
        # Delete the model before the file
        super(Product, self).delete(*args, **kwargs)
        # Delete the file after the model
        storage.delete(path)
        
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

class TrackOrder(models.Model):
    toid = models.AutoField(primary_key=True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    description = models.CharField(max_length=250)
    date = models.DateTimeField()

    def __str__(self):
        return self.description

class Coupen(models.Model):
    code = models.CharField(max_length=10)
    discount = models.IntegerField()
    description = models.CharField(max_length=100)
    applied = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE,null=True,blank=True)

    def __str__(self):
        return self.code

class Review(models.Model):
    star = models.IntegerField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

class ProductComment(models.Model):
    cno = models.AutoField(primary_key=True)
    comment = models.TextField()
    user = models.ForeignKey(User,on_delete = models.CASCADE)
    product = models.ForeignKey(Product,on_delete = models.CASCADE)
    parent = models.ForeignKey('self',on_delete=models.CASCADE,null=True,blank=True)
    timestamp = models.DateTimeField(default=now)