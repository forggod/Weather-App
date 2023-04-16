from django.shortcuts import render
from .models import City
from .forms import CityForm
import requests


def index(request):
    appid = 'e82b22cd112ac812cb4e0a21da77ad8b'
    url = 'https://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid=' + appid
    city = 'Moscow'
    cities = City.objects.all()
    cities_list = []

    if request.method == 'POST':
        form = CityForm(request.POST)
        form.save()

    form = CityForm()

    for city in cities:
        response = requests.get(url.format(city)).json()
        city_data = {
            'city': city.name,
            'temp': response["main"]["temp"],
            'fltemp': response["main"]["feels_like"],
            'icon': response["weather"][0]["icon"],
            'visibility': int(response["visibility"] / 1000),
            'timezone': int(response["timezone"] / (60 * 60)),
        }
        cities_list.append(city_data)

    context = {
        'info': cities_list,
        'form': form
    }

    return render(request, "index.html", context)
