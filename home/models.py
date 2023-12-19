from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Categorie(models.Model):
    name = models.CharField(max_length=50)


    def __str__(self) :
        return self.name
    
    def save(self, *args, **Kwargs):
        super(Categorie,self).save(*args,**Kwargs)


class Customer(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE,null=True,blank=True)
    name = models.CharField(max_length=50,null=True)
    email = models.CharField(max_length=200,null=True)

    def __str__(self):
        return self.name
    
class Product(models.Model):

    name = models.CharField(max_length=50)
    prix = models.DecimalField(max_digits=6, decimal_places=2)
    detail = models.TextField()
    image = models.ImageField(upload_to='Image_Product',blank=False)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    Categorie = models.ForeignKey(Categorie, on_delete=models.CASCADE,default=False,null=True)
    date_posted = models.DateTimeField(default=timezone.now)
    digital = models.BooleanField(default=False,null=True,blank=False)


    def __str__(self) :
        return self.name
    
    def save(self, *args, **Kwargs):
        super(Product,self).save(*args,**Kwargs)

    @property
    def imageUrl(self):
        try:
            url = self.image.url
        except:
            url =''
        return url 

class Order(models.Model):
    customer =models.ForeignKey(Customer,on_delete=models.SET_NULL,blank=True, null=True)
    date_order = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False,null=True,blank=False)
    transaction_id = models.CharField(max_length=200,null=True)


    def __str__(self) :
        return str(self.id)
    
    @property
    def shipping (self):
        shipping = False
        orderitems = self.orderitem_set.all()
        for i in orderitems:
            if i.Product.digital == False:
                shipping = True
            return shipping


    
    @property
    def get_cart_total(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.get_total for item in orderitems])
        return total
    
    @property
    def get_cart_items(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.quantity for item in orderitems])
        return total


class OrderItem(models.Model):
    Product = models.ForeignKey(Product, on_delete=models.SET_NULL,blank=True,null=True)
    Order = models.ForeignKey(Order, on_delete=models.SET_NULL,blank=True,null=True)
    quantity = models.IntegerField(default=0, null=True,blank=True)
    date_added = models.DateTimeField(auto_now_add=True)

    @property
    def get_total(self):
        total = self.Product.prix * self.quantity
        return total

class ShippingAdress(models.Model):
     customer =models.ForeignKey(Customer,on_delete=models.SET_NULL,blank=True, null=True)
     Order = models.ForeignKey(Order, on_delete=models.SET_NULL,blank=True,null=True)
     address = models.CharField(max_length=50,null=True)
     city = models.CharField(max_length=50,null=True)
     state = models.CharField(max_length=50,null=True)
     zipcode = models.CharField(max_length=50,null=True)
     date_added = models.DateTimeField(auto_now_add=True)

     def __str__(self) :
        return self.address