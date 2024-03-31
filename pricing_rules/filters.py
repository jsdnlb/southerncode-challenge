import django_filters
from .models import PricingRule


class PricingRuleFilter(django_filters.FilterSet):
    class Meta:
        model = PricingRule
        fields = {
            "property__name": ["icontains"],
            "price_modifier": ["exact", "lt", "gt"],
            "min_stay_length": ["exact", "lt", "gt"],
            "fixed_price": ["exact", "lt", "gt"],
            "specific_day": ["exact", "lt", "gt"],
        }
