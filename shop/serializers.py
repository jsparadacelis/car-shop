from django.contrib.auth.models import User
from rest_framework.serializers import ModelSerializer
from .models import Car, Customer, Brand

class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ('first_name', 'last_name')

class CustomerSerializer(ModelSerializer):
    user = UserSerializer(read_only=True)
    class Meta:
        model = Customer
        fields = ('user', 'country_id', 'full_name')

class BrandSerializer(ModelSerializer):
    class Meta:
        model = Brand
        fields = ('name',)

class CarSerializer(ModelSerializer):
    car_owner = CustomerSerializer(read_only=True)
    car_brand = BrandSerializer(read_only=True)
    class Meta:
        model = Car
        fields = ('pk', 'car_plate', 'car_brand', 'car_type','car_owner')