import django_filters
from properties.models import Property


class PropertyFilter(django_filters.FilterSet):
    class Meta:
        model = Property
        fields = {
            'name': ['icontains'],
            'base_price': ['exact', 'lt', 'gt']
        }