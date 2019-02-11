from django.urls import path

from .api import CarList, get_car_list_by_user, get_car_list_by_brand, get_car_count_by_brand, request_to_api
from .views import login_view, sign_up, index_view, get_report, create_car, edit_profile, dowload_csv_file, edit_car, create_brand, log_out

urlpatterns = [
    path("", login_view, name="login_view"),
    path("sign_up", sign_up, name="sign_up"),
    path("index", index_view, name="index"),
    path("get_report", get_report, name="get_report"),
    path("create_car", create_car, name="create_car"),
    path("create_brand", create_brand, name="create_brand"),
    path("edit_profile", edit_profile , name="edit_profile"),
    path("download_csv", dowload_csv_file, name="download_csv"),
    path("edit_car/<int:id_car>", edit_car, name="edit_car"),
    path("log_out", log_out, name="log_out"),
    #API Urls
    path('list_car', CarList.as_view(), name = 'list_car'),
    #List cars by user
    path('list_car_by_user/<int:customer_id>', get_car_list_by_user, name = 'list_car_by_user'),
    path('list_car_by_user', get_car_list_by_user),
    #List car by brand
    path('list_car_by_brand', get_car_list_by_brand, name = 'list_car_by_brand'),
    path('list_car_by_brand/<str:brand_name>', get_car_list_by_brand),
    #Get count by brand
    path('get_car_count_by_brand', get_car_count_by_brand, name = 'get_car_count_by_brand'),
    path('get_car_count_by_brand/<str:brand_name>', get_car_count_by_brand, name = 'get_car_count_by_brand'),
    path('api', request_to_api, name = 'api')
]