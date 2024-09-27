import geocoder
import requests
from datetime import datetime

from django.http import HttpResponse
from django.template import loader
from WeatherAppDjango.models import Worldcities
from geopy.geocoders import Nominatim

def temp(request):
    location = geocoder.ip('me').latlng

    if location:
        geolocator = Nominatim(user_agent="my_app")
        reverse_location = geolocator.reverse(f"{location[0]}, {location[1]}", exactly_one=True)

        if reverse_location:
            city = reverse_location.raw.get('address', {}).get('city', 'Unknown Location')
        else:
            city = "Unknown Location"

    request_data = get_temp( location)
    template = loader.get_template('index.html')
    context = {
        'city': city,
        'request_data': request_data}

    return HttpResponse(template.render(context, request))

def temp_rand(request):
    rand_item = Worldcities.objects.all().order_by('?').first()
    city = rand_item.city
    location = [rand_item.lat, rand_item.lng]
    temp = get_temp(location)
    template = loader.get_template('index.html')
    context = {'city' : city,
               'request_data': temp}
    return HttpResponse(template.render(context, request))

def get_temp( location):
    endpoint = "https://api.open-meteo.com/v1/forecast"
    api_request = f"{endpoint}?latitude={location[0]}&longitude={location[1]}&hourly=temperature_2m"
    now = datetime.now()
    hour = now.hour
    request_data = requests.get(api_request).json()['hourly']['temperature_2m'][hour]
    return request_data
