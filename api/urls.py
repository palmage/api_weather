from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import ListWeatherAPIWiew

router = DefaultRouter()
router.register('wheather', ListWeatherAPIWiew)
urlpatterns = [
    path('weather/', ListWeatherAPIWiew.as_view(), name='get_weather'),
]
