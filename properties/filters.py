import django_filters
from properties.models import Property


class PropertyFilter(django_filters.FilterSet):
    """
    Filter class for the PropertyFilter model.
    """

    class Meta:
        model = Property
        fields = {
            'name': ['icontains'],
            'base_price': ['exact', 'lt', 'gt']
        }