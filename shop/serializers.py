# Core django imports
from django.contrib.auth.models import User
# Third party libraries import
from rest_framework.serializers import ModelSerializer
# Local import app
from .models import Car, Customer, Brand

class UserSerializer(ModelSerializer):
    """ user Serializer """
    class Meta:
        model = User
        # campos a serializar
        fields = ('first_name', 'last_name')

class CustomerSerializer(ModelSerializer):
    """ Customer serializer """
    user = UserSerializer(read_only=True)
    class Meta:
        model = Customer
        # campos a serializar
        fields = ('user', 'country_id', 'full_name')

class BrandSerializer(ModelSerializer):
    """ Brand serializer """
    class Meta:
        model = Brand
        fields = ('name',)

class CarSerializer(ModelSerializer):
    """ Car serilizer """
    # obtiene el propietario y la marca asociada al carro
    car_owner = CustomerSerializer(read_only=True)
    car_brand = BrandSerializer(read_only=True)
    class Meta:
        model = Car
        # renderiza los datos del carro junto con el propietario y la marca
        fields = ('pk', 'car_plate', 'car_brand', 'car_type','car_owner')