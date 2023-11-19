from django.db import models
from django.core.validators import MinValueValidator
from django.contrib.auth.models import AbstractUser


class Category(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200, null=False, unique=True)
    icon = models.ImageField(blank=True, upload_to='category')

    def __str__(self):
        return '{}'.format(self.name)


class Manufacturer(models.Model):
    id = models.IntegerField(primary_key=True, auto_created=True)
    name = models.CharField(max_length=200, null=False)

    def __str__(self):
        return '{}'.format(self.name)


class Product(models.Model):
    id = models.IntegerField(primary_key=True, auto_created=True)
    name = models.CharField(max_length=200, null=False, blank=False, unique=True)
    description = models.CharField(max_length=200, blank=True)
    price = models.FloatField(max_length=3, validators=[MinValueValidator(0.0)])
    quantity = models.IntegerField(validators=[MinValueValidator(0)])
    icon = models.ImageField(blank=True, upload_to='product')
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    manufacturer = models.ForeignKey(Manufacturer, on_delete=models.CASCADE)

    def __str__(self):
        return 'Product : {} with id : {}'.format(self.name, self.id)


class Client(AbstractUser):
    first_name = models.CharField(max_length=200, null=False)
    last_name = models.CharField(max_length=200, null=False)
    address = models.CharField(max_length=300, null=False)
    phone_number = models.CharField(max_length=15, unique=True)
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.username


class Order(models.Model):
    status = [
        ('AW', 'Awaiting'),
        ('PR', 'Processing'),
        ('FI', 'Finalized'),
    ]

    id = models.IntegerField(primary_key=True, auto_created=True)
    price = models.FloatField(max_length=3, validators=[MinValueValidator(0.0)])
    date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, null=False, choices=status)
    client_id = models.ForeignKey(Client, on_delete=models.CASCADE)

    def __str__(self):
        return 'Order id : {} from : {}'.format(self.id, self.client_id)


class DetailsOrder(models.Model):
    id = models.IntegerField(primary_key=True, auto_created=True)
    quantity = models.IntegerField(validators=[MinValueValidator(0)])
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE)
    order_id = models.ForeignKey(Order, on_delete=models.CASCADE)

    def __str__(self):
        return 'Details order id : {}'.format(self.id)
