from django.contrib import admin
from food.models import CreateContact,item,my_cart,address
from django.contrib.auth.models import User,auth
# Register your models here.
admin.site.register(CreateContact)
admin.site.register(item)
admin.site.register(my_cart)
admin.site.register(address)