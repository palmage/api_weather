import pytz

from django.db import models

TIMEZONES = tuple(zip(pytz.all_timezones, pytz.all_timezones))
WEATHER_SITES = [
    ('weatherbit', 'weatherbit'),
    ('openweathermap', 'openweathermap'),
]


class City(models.Model):
    name = models.CharField(max_length=50)
    id_in_weatherbit = models.PositiveIntegerField()
    id_in_openweathermap = models.PositiveIntegerField()
    latitude = models.DecimalField(max_digits=8, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    timezone = models.CharField(
        max_length=32, choices=TIMEZONES, default='UTC'
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Города'


class Weather(models.Model):
    temperature = models.DecimalField(max_digits=3, decimal_places=1)
    datetime = models.DateTimeField()
    city = models.ForeignKey(
        City, related_name='weather', on_delete=models.CASCADE
    )
    source = models.CharField(
        max_length=30, choices=WEATHER_SITES
    )

    class Meta:
        verbose_name_plural = 'Погода'
        ordering = ['-datetime']
        constraints = [
            models.UniqueConstraint(
                fields=['datetime', 'city'],
                name='unique_weather_obj'
            ),
        ]

    def __str__(self):
        return f'Погода в {self.city} {self.datetime}'
