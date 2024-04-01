from typing import Optional
from rest_framework import serializers
from pricing_rules.models import PricingRule
from properties.models import Property


class PricingRuleSerializer(serializers.ModelSerializer):
    """
    Serializer for the PricingRule model.

    Serializes PricingRule instances to JSON format and vice versa.
    Includes the property name as a read-only field using a SerializerMethodField.

    Attributes:
        specific_day: DateField for the specific day when the pricing rule applies.
        property_name: SerializerMethodField for the name of the associated property.
    """

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
        """
        Returns the name of the associated property.

        Args:
            obj: The PricingRule instance.

        Returns:
            The name of the associated property if available, otherwise None.
        """
        return obj.property.name if obj.property else None
