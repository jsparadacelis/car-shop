from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render

import json
from rest_framework import generics
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Car, Customer, Brand
from .serializers import CarSerializer, UserSerializer

class CarList(generics.ListCreateAPIView):
    queryset = Car.objects.all()
    serializer_class = CarSerializer
    template_name = "dashboard/edit_car.html"

@api_view(['GET'])
def get_car_list_by_user(request, customer_id=None):
    
    list_response = []
    list_users = Customer.objects.all()
    list_cars = Car.objects.all()

    if request.method == "GET":
        if customer_id != None:
            customer = get_object_or_404(Customer, country_id=customer_id)
            list_cars = list(
                filter(lambda car:car.car_owner==customer, list_cars)
            )
            print(list_cars)
            list_cars = CarSerializer(list_cars, many=True)
            list_response = [
                {
                    "list_cars" : list_cars.data
                }
            ]
            return Response(list_response)
        else:
            list_cars = CarSerializer(list_cars, many=True)
            return Response(list_cars.data)
    
@api_view(['GET'])
def get_car_list_by_brand(request, brand_name=None):

    list_brand = Brand.objects.all()
    list_cars = Car.objects.all()
    list_response = []

    if request.method == "GET":
        if brand_name != None:
            brand = get_object_or_404(Brand, name=brand_name)
            list_cars = list(filter(lambda car: car.car_brand == brand,list_cars))
            list_cars = CarSerializer(list_cars, many=True)
            list_response = [
                {
                    "marca" : brand.name,
                    "list_cars" : list_cars.data
                }
            ]
            return Response(list_response)
        else:
            for brand in list_brand:
                list_cars = Car.objects.filter(car_brand=brand)
                if list_cars.count() > 0:
                    list_cars = CarSerializer(list_cars, many=True)
                    item = {
                        "brand" : brand.name,
                        "list_cars" : list_cars.data
                    }
                    list_response.append(item)
            return Response(list_response)

@api_view(['GET'])
def get_car_count_by_brand(request, brand_name=None):
    
    list_response = []
    if request.method == "GET":
        if brand_name:
            print(brand_name)
            brand = get_object_or_404(Brand, name = brand_name)
            count_cars = Car.objects.filter(car_brand=brand).count()
            item ={
                "marca" : brand.name,
                "cantidad" : count_cars
            }
            list_response.append(item)
        else:
            list_brands = Brand.objects.all()
            for brand in list_brands:
                count_cars = Car.objects.filter(car_brand=brand).count()
                item = {
                    "marca" : brand.name,
                    "cantidad" : count_cars
                }
                list_response.append(item)
        
        return Response(list_response)

def request_to_api(request):
    return render(request, "dashboard/api_view.html")