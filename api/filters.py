import django_filters

from django_filters import rest_framework as filters

from api.models import City, Weather


class WeatherFilter(filters.FilterSet):

    source = django_filters.ModelMultipleChoiceFilter(
        to_field_name='source',
        queryset=Weather.objects.all()
    )
    city_name = django_filters.ModelMultipleChoiceFilter(
        to_field_name='name',
        queryset=City.objects.all()
    )
    datetime = django_filters.DateTimeFromToRangeFilter(
    )
