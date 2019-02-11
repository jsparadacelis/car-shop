from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404

import csv, datetime, json

from .forms import LoginForm, SignUpForm, SearchCarsForm, CarForm, CustomerForm, CarEditForm, BrandForm
from .models import Car, Customer, Brand
from .services import RequestApi

def login_view(request):
    
    form = LoginForm()
    if request.method == "POST":
        form = LoginForm(request.POST)
        
        if form.is_valid():
            data = form.cleaned_data
            user = authenticate(
                request, 
                username = data["username"], 
                password = data["password"]
            )
            if user :
                login(request, user)
                return redirect("index")
            else:
                messages.error(
                    request,
                    'usuario o contraseña incorrecta'
                )
                return redirect('login_view')
            
    context = {
        'form': form
    }

    return render(request, 'users/login.html', context)

def sign_up(request):
    
    form_signup = SignUpForm()
    if request.method == 'POST' and request.FILES['document_file']:
        document_file = request.FILES['document_file']

        form_signup = SignUpForm(request.POST, request.FILES)
        if form_signup.is_valid():
            form_signup.save()
            messages.success(
                    request,
                    'usuario creado exitosamente'
            )
            return redirect("login_view")

    context = {
        "form_signup" : form_signup
    }

    return render(request, 'users/logup.html', context) 

@login_required
def index_view(request):
    
    form = SearchCarsForm()
    if request.method == "GET":
        list_cars = Car.objects.filter(car_owner=request.user.customer)
        list_cars = list_cars.order_by('-id')
        
        paginator = Paginator(list_cars, 5)
        page = request.GET.get('page')
        list_cars_pages = paginator.get_page(page)
        context = {
            "list_cars" : list_cars_pages,
            "form" : form,
        }
        return render(request, 'dashboard/index.html', context)
    else:
        data = request.POST
        form = SearchCarsForm(data)
        if form.is_valid():
            car_owner = None
            list_cars = []
            if data["car_owner_name"] != "":
                car_owner = get_object_or_404(
                    User, 
                    first_name = data["car_owner_name"].lower()
                )
                car_owner = car_owner.customer
            elif data["owner_id"] != "":
                car_owner = get_object_or_404(
                    Customer, 
                    country_id = data["owner_id"]
                )
            
            if car_owner and data['car_plate']:
                list_cars = Car.objects.filter(
                    car_owner=car_owner, 
                    car_plate=data['car_plate'].lower()
                )
            else: 
                list_cars = Car.objects.filter(
                    Q(car_owner=car_owner) | Q(car_plate=data['car_plate'].lower()) 
                )
            context = {
                "list_cars" : list_cars,
                "form" : SearchCarsForm()
            }
        return render(request, 'dashboard/index.html', context)

@login_required
def log_out(request):
    logout(request)
    return redirect("login_view")

@login_required
def get_report(request):
    url_base = settings.URL_BASE
    request_api = RequestApi(url_base)

    car_count = request_api.get_car_count_by_brand()
    car_count = list(filter(lambda car: car["cantidad"] > 0, car_count.json()))
    list_car_brand = request_api.get_car_list_by_brand()
    list_car_brand = list_car_brand.json()
    context = {
        "car_count" : car_count,
        "list_car_brand" : list_car_brand
    }
    
    return render(request, 'dashboard/report.html', context)

@login_required
def create_car(request):
    form = CarForm()
    context = {    
        "form" : form
    }
    brand_count = Brand.objects.all().count()
    if request.method == "POST":
        data = request.POST
        form = CarForm(data)
        if form.is_valid():
            form.save(request)
            messages.success(
                    request,
                    'Carro creado exitosamente'
            )
            return redirect("index")
    else:
        if brand_count <= 0:
            messages.error(
                    request,
                    'No hay marcas para seleccionar.'
            )


    return render(request, 'dashboard/create.html', context)

@login_required
def create_brand(request):
    form = BrandForm()
    context = {
        "form" : form
    }
    if request.method == "POST":
        data = request.POST
        form = BrandForm(data)
        print(form.is_valid())
        if form.is_valid():
            form.save()
            messages.success(
                request,
                'Ahora {} es una marca'.format(data["name"])
            )
            return redirect("index")

    return render(request, 'dashboard/create.html', context)

@login_required
def edit_car(request, id_car):
    car = get_object_or_404(Car, pk=id_car)
    form = CarEditForm(
        {
            "car_plate" : car.car_plate,
            "car_brand" : car.car_brand,
            "car_type"  : car.car_type
        }
    )
    context = {
        "form" :form
    }

    if request.method == "POST":
        data = request.POST
        form = CarEditForm(data)
        if form.is_valid():
            form.save(car)
            messages.error(
                request,
                'Vehículo actualizado'
            )
            return redirect("index")


    return render(request, 'dashboard/edit_car.html', context)

@login_required
def edit_profile(request):
    
    data_edit = {
        "first_name" : request.user.first_name,
        "last_name" : request.user.last_name,
        "username" : request.user.username,
        "email" : request.user.email,
        "country_id" : request.user.customer.country_id
    }
    form = CustomerForm(data_edit, {"document_file":request.user.customer.document_file})
    context = {    
        "form" : form
    }
    if request.method == "POST":
        form = CustomerForm(request.POST, request.FILES)
        if form.is_valid():
            form.save(request)
            messages.success(
                request,
                'Perfil actualizado'
            )
            return redirect("index")

    return render(request, 'users/edit.html', context)

@login_required
def dowload_csv_file(request):

    now = datetime.datetime.now()
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="report{}.csv"'.format(now.strftime("%Y-%m-%d"))
    writer = csv.writer(response)
    writer.writerow(['Placa', 'Marca', 'Propietario', 'Tipo'])

    url_base = settings.URL_BASE
    request_api = RequestApi(url_base)
    list_car_response = request_api.get_list_car()
    list_car_response = list_car_response.json()

    if list_car_response != []:
        for car in list_car_response:
            writer.writerow(
                [
                    car["car_plate"].upper(), 
                    car["car_brand"]["name"],
                    car["car_owner"]["full_name"], 
                    car["car_type"]
                ]
            )
        return response  
    else:
        messages.error(
                request,
                'No existe información suficiente'
        )
        return redirect("index")
     