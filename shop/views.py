# Standard library imports
import csv, datetime, json

# Core Django imports
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404

# Local app imports
from .forms import LoginForm, SignUpForm, SearchCarsForm, CarForm, CustomerForm, CarEditForm, BrandForm
from .models import Car, Customer, Brand
from .services import RequestApi

def login_view(request):
    """Login user view""" 

    form = LoginForm()
    # if request method is POST
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            user = authenticate(
                request, 
                username = data["username"], 
                password = data["password"]
            )
            # si la autenticacion fue exitosa, ejecuta el login
            if user :
                login(request, user)
                return redirect("index")
            else:
                #si no fue exitosa, renderiza un mensaje de error y redirige a la vista del login
                messages.error(
                    request,
                    'usuario o contraseña incorrecta'
                )
                return redirect('login_view')
    #añade el formulario bien sea get o post la solicitud
    context = {
        'form': form
    }
    return render(request, 'users/login.html', context)

def sign_up(request):
    """Sign up view, for register users"""
    form_signup = SignUpForm()
    # si llegan los campos del formulario y el archido de la cedula
    if request.method == 'POST' and request.FILES['document_file']:
        document_file = request.FILES['document_file']
        form_signup = SignUpForm(request.POST, request.FILES)
        if form_signup.is_valid():
            # si el formulario es valido, crea el nuevo usuario
            form_signup.save()
            messages.success(
                request,
                'usuario creado exitosamente'
            )
            return redirect("login_view")
        else:
            # si no pudo validar el usuario, redirige al formulario de nuevo
            messages.error(
                    request,
                    'Ocurrió un error, intenta de nuevo, por favor'
            )
            return redirect("sign_up")

    context = {
        "form_signup" : form_signup
    }
    return render(request, 'users/logup.html', context) 

# Decorador para exigir que el usuario esté registrado
@login_required
def index_view(request):
    """Main view after signin in app"""
    form = SearchCarsForm()
    if request.method == "GET":
        # para mostrar los autos propios del usuario autenticado
        list_cars = Car.objects.filter(car_owner=request.user.customer)
        list_cars = list_cars.order_by('-id')
        # para mostrar los datos en grupos de 5 objetos
        paginator = Paginator(list_cars, 5)
        page = request.GET.get('page')
        list_cars_pages = paginator.get_page(page)
        context = {
            "list_cars" : list_cars_pages,
            "form" : form,
        }
        return render(request, 'dashboard/index.html', context)
    else:
        # si la solicitud es POST, es porque va a realizar una busqueda
        data = request.POST
        form = SearchCarsForm(data)
        if form.is_valid():
            car_owner = None
            list_cars = []
            # busca el usuario propietario del carro segun su nombre
            if data["car_owner_name"] != "":
                car_owner = get_object_or_404(
                    User, 
                    first_name = data["car_owner_name"].lower()
                )
                car_owner = car_owner.customer
            #busca al usuario propietario por su cedula
            elif data["owner_id"] != "":
                car_owner = get_object_or_404(
                    Customer, 
                    country_id = data["owner_id"]
                )
            # genera las busquedas segun los datos que haya, en este caso, con usuario y cedula
            if car_owner and data['car_plate']:
                list_cars = Car.objects.filter(
                    car_owner=car_owner, 
                    car_plate=data['car_plate'].lower()
                )
            else:
                # busqueda por usuario o por placa
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
    """Log out view"""
    #  Cierra la sesión actual
    logout(request)
    return redirect("login_view")

@login_required
def get_report(request):
    """View for render cars and brands"""
    #obtener la url de la aplicacion
    url_base = settings.URL_BASE
    #Crea una ejemplificacion de la clase que contiene los metodos para llamar a la api
    request_api = RequestApi(url_base)
    #realiza el conteo por marca de carro 
    car_count = request_api.get_car_count_by_brand()
    # crea una lista a partir de aplicar un filtro a la respuesta de la api
    car_count = list(filter(lambda car: car["cantidad"] > 0, car_count.json()))

    #obtiene los carros por marca
    list_car_brand = request_api.get_car_list_by_brand()
    list_car_brand = list_car_brand.json()

    #crea el contexto con los datos recibidos 
    context = {
        "car_count" : car_count,
        "list_car_brand" : list_car_brand
    }
    return render(request, 'dashboard/report.html', context)

@login_required
def create_car(request):
    """ Create Car view """
    form = CarForm()
    context = {    
        "form" : form
    }
    # obtiene el numero de marcas   
    brand_count = Brand.objects.all().count()
    if request.method == "POST":
        data = request.POST
        form = CarForm(data)
        if form.is_valid():
            form.save(request)
            messages.success(
                request,
                # hace formato al mensaje para mostrar la placa del carro creado
                'Carro creado exitosamente, con placa {}'.format(data["car_plate"])
            )
            return redirect("index")
    else:
        # si no existen marcas, muestra un mensaje de advertencia
        if brand_count <= 0:
            messages.warning(
                request,
                'No hay marcas para seleccionar. Debes ser superheroe para crear una.'
            )

    return render(request, 'dashboard/create.html', context)

@login_required
def create_brand(request):
    """ Create new brand """
    form = BrandForm()
    context = {
        "form" : form
    }
    if request.method == "POST":
        data = request.POST
        form = BrandForm(data)
        if form.is_valid():
            form.save()
            messages.success(
                request,
                #renderizael mensaje para mostrar el nombre de la marca creada
                'Ahora {} es una marca'.format(data["name"])
            )
            return redirect("index")

    return render(request, 'dashboard/create.html', context)

@login_required
# recibe el ID del auto por la url
def edit_car(request, id_car):
    """ Edit car """
    car = get_object_or_404(Car, pk=id_car)
    # a partir del objeto obtenido, genera un diccionario para que al pasar al formulario
    # se carguen los datos actuales del objeto
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
                'Vehículo se actualizó el vehículo con placas {}'.format(car.car_plate)
            )
            return redirect("index")

    return render(request, 'dashboard/edit_car.html', context)

@login_required
def edit_profile(request):
    """ Edit profile view"""
    # obtiene los datos a través del request.user
    data_edit = {
        "first_name" : request.user.first_name,
        "last_name" : request.user.last_name,
        "username" : request.user.username,
        "email" : request.user.email,
        "country_id" : request.user.customer.country_id
    }
    # pasa los paramentros: datos del usuario y el documento
    form = CustomerForm(
        data_edit, 
        {
            "document_file":request.user.customer.document_file
        }
    )
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
    """Generate CSV report file"""
    # fecha de hoy
    now = datetime.datetime.now()
    response = HttpResponse(content_type='text/csv')
    # decalara el archivo con su nombre
    response['Content-Disposition'] = 'attachment; filename="report{}.csv"'.format(now.strftime("%Y-%m-%d"))
    writer = csv.writer(response)
    # la primera fila sera para las cabeceras
    writer.writerow(['Placa', 'Marca', 'Propietario', 'Tipo'])
    # obtiene el url 
    url_base = settings.URL_BASE
    # otiene los datos de las consultas a la API
    request_api = RequestApi(url_base)
    list_car_response = request_api.get_list_car()
    list_car_response = list_car_response.json()
    # si la respuesta de la api no es vacia, escribe los datos en el csv
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
     