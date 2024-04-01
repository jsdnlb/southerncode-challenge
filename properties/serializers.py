from rest_framework import serializers
from properties.models import Property


class PropertySerializer(serializers.ModelSerializer):
    """
    Serializer for the Property model.

    Serializes Property instances into JSON representations and validates
    incoming JSON data against the defined fields and model constraints.

    Attributes:
        model (Property): The Property model to be serialized/deserialized.
        fields (list): List of fields to include in the serialized output.
        extra_kwargs (dict): Additional keyword arguments to customize field behavior.
    """

    class Meta:
        model = Property
        fields = ["id", "name", "base_price", "created_at", "updated_at"]
        extra_kwargs = {
            "name": {"required": True},
            "base_price": {"required": True},
        }
