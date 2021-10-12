import os

import requests

from .models import City, Weather
from .serializers import OpenWeatherMapSerializer, WeatherBitSerializer


def get_weather():
    # Получаем и сохраняем погоду с api openweathermap
    cities = City.objects.values_list('id_in_openweathermap')
    for city in cities:
        response = requests.get(
            'https://api.openweathermap.org/data/2.5/weather',
            params={'id': city, 'appid': os.environ.get('KEY_OPENWEATHERMAP')},
        )
        if response.status_code != 200:
            print('Нет ответа от сервиса погоды')
            return None
        serializer = OpenWeatherMapSerializer(data=response.json())
        if serializer.is_valid():
            Weather.objects.get_or_create(
                source='openweathermap', **serializer.validated_data
            )
        else:
            print(serializer.errors)

    # Получаем и сохраняем погоду с api weatherbit
    cities = City.objects.values_list('id_in_weatherbit')
    for city in cities:
        response = requests.get(
            'http://api.weatherbit.io/v2.0/current',
            params={'city_id': city, 'key': os.environ.get('KEY_WEATHERBIT')},
        )
        if response.status_code != 200:
            print('Нет ответа от сервиса погоды')
            return None
        serializer = WeatherBitSerializer(data=response.json()['data'][0])
        if serializer.is_valid():
            Weather.objects.get_or_create(
                source='weatherbit', **serializer.validated_data
            )
        else:
            print(serializer.errors)
