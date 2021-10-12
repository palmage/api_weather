from django.contrib import admin

from .models import City, Weather


@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'latitude', 'longitude', 'timezone',)
    list_display_links = ('id', 'name', 'latitude', 'longitude', 'timezone',)


@admin.register(Weather)
class WeatherAdmin(admin.ModelAdmin):
    list_display = ('id', 'temperature', 'datetime', 'city', 'source',)
    list_display_links = ('id', 'temperature', 'datetime', 'city', 'source',)
