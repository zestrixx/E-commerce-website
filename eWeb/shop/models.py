import django
from django.db import models
from django.utils import timezone
# Create your models here.


class Product(models.Model):
    product_id = models.AutoField
    product_name = models.CharField(max_length=100)
    category = models.CharField(max_length=50, default="")
    subcategory = models.CharField(max_length=50, default="")
    price = models.IntegerField(default=0)
    desc = models.CharField(max_length=300)
    pub_date = models.DateField()
    image = models.ImageField(upload_to="shop/images", default="")

    def __str__(self):
        return self.product_name


class Contact(models.Model):
    msg_id = models.AutoField
    name = models.CharField(max_length=100, default="")
    email = models.CharField(max_length=100, default="")
    phone = models.CharField(max_length=50, default="")
    query = models.CharField(max_length=500)

    def __str__(self):
        return self.email


class Order(models.Model):
    order_id = models.AutoField(primary_key=True)
    items_json = models.CharField(max_length=5000)
    amount = models.IntegerField(default=0)
    name = models.CharField(max_length=90)
    phone = models.CharField(max_length=111)
    address = models.CharField(max_length=111)
    local_address = models.CharField(max_length=111)
    city = models.CharField(max_length=111)
    state = models.CharField(max_length=111)
    pin_code = models.CharField(max_length=111)


class OrderUpdate(models.Model):
    update_id = models.AutoField(primary_key=True)
    order_id = models.IntegerField(default="")
    update_desc = models.CharField(max_length=5000)
    timestamp = models.DateTimeField(default=django.utils.timezone.now)

    def __str__(self):
        return self.update_desc[0:25] + "..."


class BannerImage(models.Model):
    image_name = models.CharField(max_length=50)
    image = models.ImageField(upload_to="shop/bannerimages", blank=False, null=False)

    def __str__(self):
        return self.image_name
