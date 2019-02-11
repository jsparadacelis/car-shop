from django.db import models
from django.contrib.auth.models import User


class Customer(models.Model):
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    document_file = models.FileField(upload_to='uploads/')
    country_id = models.CharField(max_length=30)

    @property
    def full_name(self):
        return '%s %s' % (self.user.first_name, self.user.last_name)
    

class Brand(models.Model):
    name = models.CharField(max_length=30)
    created_at = models.DateField(auto_now_add=True)
    def __str__(self):
        return self.name
    
    
class Car(models.Model):

    VEHICULO = 'vehiculo'
    VAN = 'van'
    FAMILIAR = 'familiar'
    DEPORTIVO = 'deportivo'
    
    TYPE_CHOICES = (
        (VEHICULO, 'Vehículo'),
        (VAN, 'Van'),
        (FAMILIAR, 'Familiar'),
        (DEPORTIVO, 'Deportivo')
    )
    car_plate = models.CharField(max_length=10)
    car_brand = models.ForeignKey(Brand, verbose_name=("brand_car_fk"), on_delete=models.CASCADE)
    car_owner = models.ForeignKey(Customer, verbose_name=("customer_car_fk"), on_delete=models.CASCADE)
    car_type = models.CharField(max_length=20, choices = TYPE_CHOICES)

