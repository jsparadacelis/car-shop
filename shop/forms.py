from django import forms
from django.contrib.auth.models import User
from django.forms import ModelForm

from .models import Customer, Car, Brand

class LoginForm(forms.Form):
    """Validate form Login"""
    username = forms.CharField(label='usuario', max_length=15)
    password = forms.CharField(
        label='contraseña',
        min_length = 5, 
        max_length=15,
        widget=forms.PasswordInput()
    )

class SignUpForm(forms.Form):
    first_name = forms.CharField(label='Nombre', max_length=20)
    last_name = forms.CharField(label='Apellido', max_length=20)
    username = forms.CharField(label='usuario', max_length=15)
    password = forms.CharField(
        label='contraseña',
        min_length = 5, 
        max_length=15,
        widget=forms.PasswordInput()
    )
    confirm_password = forms.CharField(
        label='confirmar contraseña',
        min_length = 5, 
        max_length=15,
        widget=forms.PasswordInput()
    )
    country_id = forms.CharField(
        label='Cedula',
        min_length = 5,
        max_length = 11, 
        required=True
    )
    email = forms.EmailField(label='correo electrónico')
    document_file = forms.FileField()
    is_staff = forms.BooleanField(required=False)
    def clean_username(self):

        username = self.cleaned_data["username"]
        username_taken = User.objects.filter(username = username) 
        username_taken = username_taken.exists()

        if username_taken:
            raise forms.ValidationError('El usuario ya existe')
        return username
    
    def clean_country_id(self):

        country_id = self.cleaned_data["country_id"]
        print(country_id)
        country_id_taken = Customer.objects.filter(country_id=country_id)
        country_id_taken = country_id_taken.exists()

        if country_id_taken:
            raise forms.ValidationError('Ya existe un usuario registrado con esa Cedula')
        return country_id

    def clean(self):

        data = super().clean()
        password = data.get("password")
        confirm_password = data.get("confirm_password")

        if password != confirm_password:
            raise forms.ValidationError('Las contraseñas no coinciden')
        return data

    
    def save(self):
        data = self.cleaned_data
        data.pop('confirm_password')

        user = User.objects.create_user(
            data["username"],
            data["email"],
            data["password"]
        )
        user.first_name = data["first_name"].lower()
        user.last_name = data["last_name"].lower()
        user.is_staff = data["is_staff"]
        user.save()

        customer = Customer.objects.create(
            user = user,
            country_id = data["country_id"],
            document_file = data["document_file"]
        )
        customer.save()
        print(customer)

class SearchCarsForm(forms.Form):
    car_plate = forms.CharField(label="Placa",max_length=10, required=False)
    car_owner_name = forms.CharField(label="Nombre Propietario",max_length=20, required=False)
    owner_id = forms.CharField(label="Cedula Propietario",max_length=10, required=False)


class CarEditForm(ModelForm):
    class Meta:
        model = Car
        fields = ['car_plate', 'car_brand', 'car_type']
        labels = {
            "car_plate" : "Placa",
            "car_brand" : "Marca del auto",
            "car_type" : "Tipo de auto"
        }

    def save(self, car):
        data = self.cleaned_data
        car_plate = data["car_plate"]
        
        car_plate_taken = None
        if car.car_plate != car_plate:
            car_plate_taken = Car.objects.filter(car_plate=car_plate)
            car_plate_taken = car_plate_taken.exists()
            
        if car_plate_taken:
            raise forms.ValidationError('Ya existe un carro registrado con esa Placa')
        else:
            car.car_plate = data["car_plate"]
            car.car_brand = data["car_brand"]
            car.car_type = data["car_type"]
            car.save()

class CarForm(ModelForm):
    class Meta:
        model = Car
        fields = ['car_plate', 'car_brand', 'car_type']
        labels = {
            "car_plate" : "Placa",
            "car_brand" : "Marca del auto",
            "car_type" : "Tipo de auto"
        }

    def clean_car_plate(self):
        
        car_plate = self.cleaned_data["car_plate"]
        print(car_plate)
        car_plate_taken = Car.objects.filter(car_plate=car_plate)
        car_plate_taken = car_plate_taken.exists()

        if car_plate_taken:
            raise forms.ValidationError('Ya existe un Automovil con esa placa')
        return car_plate

    def save(self, request):
        data = self.cleaned_data
        print(request.user)
        
        car = Car(
            car_plate = data["car_plate"].lower(),
            car_brand = data["car_brand"],
            car_owner = request.user.customer,
            car_type = data["car_type"]
        )
        car.save()

class CustomerForm(forms.Form):

    first_name = forms.CharField(label='Nombre', max_length=20)
    last_name = forms.CharField(label='Apellido', max_length=20)
    username = forms.CharField(label='Usuario', max_length=15)
    country_id = forms.CharField(
        label='Cedula',
        min_length = 5,
        max_length = 11, 
        required=True
    )
    email = forms.EmailField(label='Correo electrónico')
    document_file = forms.FileField(label='Cargar archivo')
    is_staff = forms.BooleanField(required=False)

    def save(self, request):

        data = self.cleaned_data
        print(data)

        country_id = data["country_id"]
        document_file = data["document_file"]
        user = request.user
        customer = Customer.objects.get(user=user)
        
        country_id_taken = None
        if customer.country_id != country_id:
            country_id_taken = Customer.objects.filter(country_id=country_id)
            country_id_taken = country_id_taken.exists()
            
        if country_id_taken:
            raise forms.ValidationError('Ya existe un usuario registrado con esa Cedula')
        else:

            user.username = data["username"]
            user.first_name = data["first_name"]
            user.last_name = data["last_name"]
            user.email = data["email"]
            user.is_staff = data["is_staff"]
            user.save()
            customer.country_id = country_id
            customer.document_file = document_file
            customer.save()


class BrandForm(ModelForm):
    class Meta:
        model = Brand
        fields = ['name']
        labels = {
            "name" : "Nombre"
        }


    def clean_name(self):

        brand_name = self.cleaned_data["name"]
        brand_name_taken = Brand.objects.filter(name=brand_name)
        brand_name_taken = brand_name_taken.exists()
        if brand_name_taken:
            raise forms.ValidationError('Ya existe una marca con ese nombre')
        return brand_name


    def save(self):

        data = self.cleaned_data
        name = data["name"].lower()
        brand = Brand(
            name=name
        )
        brand.save()
