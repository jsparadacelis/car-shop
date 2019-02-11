import requests
from urllib.parse import urljoin


class RequestApi:

    def __init__(self, url_base):
        self.headers = {
                'Cache-Control': 'no-cache',
                'Content-Type':'application/json'
        }
        self.url_base = url_base
    
    def get_car_count_by_brand(self):  
        url = urljoin(self.url_base, 'get_car_count_by_brand')
        try:
            response = requests.get(
                url,
                headers = self.headers
            )
        except requests.exceptions.RequestException as error:
            raise error
        return response
    
    def get_car_list_by_brand(self):  
        url = urljoin(self.url_base, 'list_car_by_brand')
        try:
            response = requests.get(
                url,
                headers = self.headers
            )
        except requests.exceptions.RequestException as error:
            raise error
        return response
    
    def get_list_car(self):
        url = urljoin(self.url_base, 'list_car')
        try:
            response = requests.get(
                url,
                headers = self.headers
            )
        except requests.exceptions.RequestException as error:
            raise error
        return response


    