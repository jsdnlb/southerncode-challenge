from typing import Optional
from rest_framework import serializers
from pricing_rules.models import PricingRule
from properties.models import Property


class PricingRuleSerializer(serializers.ModelSerializer):
    specific_day = serializers.DateField(format="%m-%d-%Y", required=False)
    property_name = serializers.SerializerMethodField()

    class Meta:
        model = PricingRule
        fields = [
            "id",
            "property",
            "property_name",
            "price_modifier",
            "min_stay_length",
            "fixed_price",
            "specific_day",
            "created_at",
            "updated_at",
        ]

    def get_property_name(self, obj: Property) -> Optional[str]:
        return obj.property.name if obj.property else None
