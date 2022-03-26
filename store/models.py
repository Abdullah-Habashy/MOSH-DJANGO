
from datetime import datetime
from tkinter import CASCADE
from django.db import models
from django.forms import FloatField

# Create your models here.


class Promotion(models.Model):
    title = models.CharField(max_length=255)
    discount = models.FloatField()
    
    
class Collection(models.Model):
    title = models.CharField(max_length=255)
    


class Product(models.Model):
    # this class inherit Model class from models module
    title = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    # decimal is better than float in monitoring values
    # max digits : all digits before and after decimal point
    inventory = models.IntegerField()
    last_update = models.DateTimeField(auto_now=True)
    # to add current time directly
    # last_update = models.DateTimeField(auto_now_add=True)
    # auto_now_add : to add current time directly only in the forst time you created a product
    collection = models.ForeignKey(Collection, on_delete=models.CASCADE)
    promotions = models.ManyToManyField(Promotion)
    # promotions = models.ManyToManyField(Promotion , related_name = 'products')
    # here we defined many to many relation between products and promotions , the related name field specify the name of th efield in corresponding clas (ie : product) to be called "products " instead of "product_set " which is the default convention (it is better to stick to the default convention)
    


class Customer(models.Model):
    # this class inherit Model class from models module
    MEMBERSHIP_BRONZE = 'B'
    MEMBERSHIP_SILVER = 'S'
    MEMBERSHIP_GOLD = 'G'
#  we store letters in variables as a best practice to change the letter (if we want) in the future in one place instead of many places

    MEMBERSHIP_CHOICES = [
        (MEMBERSHIP_BRONZE, 'Bronze'),
        (MEMBERSHIP_SILVER, 'Silver'),
        (MEMBERSHIP_GOLD, 'Gold'),
    ]

    # this is the list of values we will use to create a multichoices field

    # first is the value stored in DB , second is human readable name displayed in admin panel
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=255)
    birth_date = models.DateField(null=True)
    membership = models.CharField(max_length=1, choices=MEMBERSHIP_CHOICES, default=MEMBERSHIP_BRONZE
                                  )


class Order(models.Model):
    # this class inherit Model class from models module
    PAYMENT_STATUS_PENDING = 'P'
    PAYMENT_STATUS_COMPLETE = 'C'
    PAYMENT_STATUS_FAILED = 'F'

    PAYMENT_STATUS_CHOICES = [
        (PAYMENT_STATUS_PENDING, 'P'),
        (PAYMENT_STATUS_COMPLETE, 'C'),
        (PAYMENT_STATUS_FAILED, 'F'),
    ]

    # first is the value stored in DB , second is human readable name displayed in admin panel

    placed_at = models.DateTimeField(auto_now_add=True)
    payment_status = models.CharField(
        max_length=1, choices=PAYMENT_STATUS_CHOICES, default=PAYMENT_STATUS_PENDING)
    customer = models.ForeignKey(Customer, on_delete=models.PROTECT)


class OrderItems(models.Model):
    order = models.ForeignKey(Order, on_delete=models.PROTECT)
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    quantity = models.PositiveBigIntegerField()
    # to prevent entry of negative values 
    price = models.DecimalField(max_digits=6, decimal_places=2)
    # we define unit price here again to stoe value of the product in the time of placing order as prices is changed continously

    
class Address(models.Model):
    street = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    customer = models.OneToOneField(
        Customer, on_delete=models.CASCADE, primary_key=True)
    customer = models.ForeignKey(Customer, on_delete=models.PROTECT)

    # we set customer to primary key to prevent duplication of another customer to the same address (PK not allowed to be duplicated)

class Cart(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    # cascade to remove all items if we delete the cart
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    # if we delete a product we need to remove it from all carts as well
    quantity = models.PositiveBigIntegerField()
    
    

    """
    Declare relations :
    
    FIRST : parent class MUST be defined before child
    
    if you cant pass the name of the parent class as a string
    
    1- ONE TO ONE : 
        - relations declare in child class only , we dont have to rpeat declaration in parent as it done ayutomatically by PYTHON (Customer has an address : son , Customer is parent and addrss is child)
        
        - on_delete:
            Cascade : delete related field.
            Protect : prevent deletion
            Null : set to null
            default : Set to default value
    
    ex : relation between customer (parent) & address (child)
    
    inside child class write :         
    customer = models.OneToOneField(Customer,on_delete=models.CASCADE, primary_key=True)
            
    2- ONE TO MANY : 
    
    inside child class (which can be many) write :         
    customer = models.ForeignKey(Customer,on_delete=models.CASCADE)
    remove primary key to allow repetition , and add foreign key 
    
    
    3- MANY TO MANY :
        Defined in any one of the two related classes according to context
        
        relation between product and promotion : each product has many promotions and each promotion can be applied to many products
        
    promotions = models.ManyToManyField(Promotion)
        
        
        
        """
