from django.db import models
from django.core.validators import MinValueValidator
from django.contrib.auth.models import AbstractUser


class Category(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200, null=False, unique=True)
    icon = models.ImageField(blank=True, upload_to='category')

    def __str__(self):
        return '{}'.format(self.name)

    class Meta:
        verbose_name_plural = 'Categories'


class Subcategory(models.Model):
    id = models.IntegerField(primary_key=True, auto_created=True)
    name = models.CharField(max_length=200, null=False)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return '{}'.format(self.name)

    class Meta:
        verbose_name_plural = 'Subcategories'


class Manufacturer(models.Model):
    id = models.IntegerField(primary_key=True, auto_created=True)
    name = models.CharField(max_length=200, null=False)

    def __str__(self):
        return '{}'.format(self.name)


class Product(models.Model):
    name = models.CharField(max_length=200, null=False, blank=False, unique=True)
    description = models.CharField(max_length=200, blank=True)
    price = models.FloatField(max_length=3, validators=[MinValueValidator(0.0)])
    quantity = models.PositiveIntegerField(default=0)
    icon = models.ImageField(blank=True, upload_to='product')
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    subcategory = models.ForeignKey(Subcategory, on_delete=models.CASCADE)
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


class Cart(models.Model):
    quantity = models.PositiveIntegerField(default=1)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    ordered = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.quantity} of {self.product.name}"

    def get_total_item_price(self):
        return self.quantity * self.product.price

    def get_final_price(self):
        return self.get_total_item_price()


class Order(models.Model):
    status = [
        ('AW', 'Awaiting'),
        ('PR', 'Processing'),
        ('FI', 'Finalized'),
    ]

    start_date = models.DateTimeField(auto_now_add=True)
    ordered_date = models.DateTimeField(blank=True, null=True)
    ordered = models.BooleanField(default=False)
    status = models.CharField(max_length=20, null=False, choices=status)
    street = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    zip_code = models.CharField(max_length=100)
    carts = models.ManyToManyField(Cart, blank=True, db_constraint=False)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)

    def __str__(self):
        return 'Order id : {} from : {}'.format(self.id, self.client.username)

    def get_total(self):
        total = 0
        for order_item in self.carts.all():
            total += order_item.get_final_price()
        return total
