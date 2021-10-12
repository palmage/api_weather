from django.db.models import F
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics

from .filters import WeatherFilter
from .models import Weather
from .serializers import GetWeatherSerializer


class ListWeatherAPIWiew(generics.ListAPIView):
    queryset = Weather.objects.select_related('city').annotate(
        city_name=F('city__name'),
        latitude=F('city__latitude'),
        longitude=F('city__longitude'),
    )
    serializer_class = GetWeatherSerializer

    filter_backends = [DjangoFilterBackend]
    filterset_class = WeatherFilter
