from django.contrib import admin
from .models import Customer, Car, Brand


admin.site.register(Customer)
admin.site.register(Car)
admin.site.register(Brand)