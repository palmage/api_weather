from datetime import datetime

import pytz

from rest_framework import serializers

from .models import City, Weather


class WeatherBitSerializer(serializers.ModelSerializer):
    city_name = serializers.SlugRelatedField(
        slug_field='name',
        source='city',
        queryset=City.objects.all()
    )
    temp = serializers.DecimalField(
        source='temperature', decimal_places=1, max_digits=3
    )
    ob_time = serializers.DateTimeField(
        source='datetime', default_timezone=pytz.timezone('UTC')
    )

    class Meta:
        model = Weather
        fields = ('city_name', 'temp', 'ob_time',)


class MainSerializer(serializers.Serializer):
    temp = serializers.FloatField()


class OpenWeatherMapSerializer(serializers.Serializer):
    name = serializers.SlugRelatedField(
        slug_field='name',
        source='city',
        queryset=City.objects.all()
    )
    main = MainSerializer(source='temperature')
    dt = serializers.IntegerField(min_value=0, source='datetime')

    def to_internal_value(self, data):
        ret = super().to_internal_value(data)
        temperature = ret['temperature']['temp']
        ret['temperature'] = round(temperature - 273, 1)
        dt = ret['datetime']
        ret['datetime'] = datetime.fromtimestamp(dt, tz=pytz.timezone('UTC'))
        return ret


class GetWeatherSerializer(serializers.Serializer):
    city_name = serializers.CharField()
    longitude = serializers.FloatField()
    latitude = serializers.FloatField()
    temperature = serializers.FloatField()
    datetime = serializers.DateTimeField()
    source = serializers.CharField()
