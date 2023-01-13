from django.db import models
from django.utils.timezone import now
from django.contrib.auth.models import AbstractUser,BaseUserManager, AbstractBaseUser

# Create your models here

from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)


class MyUserManager(BaseUserManager):
    def create_user(self, email, firstname,lastname, password=None):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            firstname=firstname,
            lastname=lastname,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, firstname,lastname, password=None):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
            email,
            password=password,
            firstname=firstname,
            lastname=lastname,

        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class MyUser(AbstractBaseUser):
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )

    firstname = models.CharField(("first name"), max_length=50)
    lastname = models.CharField(("last name"), max_length=50)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = MyUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['firstname','lastname']

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin

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
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0)
    price = models.IntegerField(default=0)
    total = models.IntegerField(default=0)
    def __str__(self):
        return self.product.pname+"  for "+self.user.username

class Order(models.Model):
    oid = models.AutoField(primary_key=True)
    user = models.ForeignKey(MyUser,on_delete=models.CASCADE)

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
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE)
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
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE,null=True,blank=True)

    def __str__(self):
        return self.code

class Review(models.Model):
    star = models.IntegerField()
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

class ProductComment(models.Model):
    cno = models.AutoField(primary_key=True)
    comment = models.TextField()
    user = models.ForeignKey(MyUser,on_delete = models.CASCADE)
    product = models.ForeignKey(Product,on_delete = models.CASCADE)
    parent = models.ForeignKey('self',on_delete=models.CASCADE,null=True,blank=True)
    timestamp = models.DateTimeField(default=now)