from django.db import models
from django.contrib.auth.models import User,auth
from django.core.validators import RegexValidator
# makemigrations - create changes and store in a file 
# migrate - apply the pending changes created by makemigrations

# Create your models here.
class CreateContact(models.Model):
    name = models.CharField(max_length=122)
    email = models.CharField(max_length=122)
    phone = models.CharField(max_length=12)
    desc = models.TextField()
    date = models.DateField()
    def __str__(self):
        return self.name
class item(models.Model):
    name = models.CharField(max_length=50)
    image = models.CharField(max_length=50)
    price = models.IntegerField()
    def __str__(self):
        return self.name

class my_cart(models.Model):
    user = models.ForeignKey(User, on_delete= models.CASCADE,)
    name = models.CharField(max_length=50)
    image = models.CharField(max_length=50)
    price = models.IntegerField()
    number=models.IntegerField()
    totalprice= models.IntegerField(default=1)
    def __str__(self):
        return self.name
class address(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,)
    name = models.CharField(max_length=50)
    house = models.CharField(max_length=50)
    street = models.CharField(max_length=50)
    city = models.CharField(max_length=20)
    pincode = models.CharField(validators=[RegexValidator(regex='^.{6}$')],max_length=6)
    phone = models.CharField(validators=[RegexValidator(regex='^.{10}$')],max_length=10)