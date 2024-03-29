from rest_framework import serializers
from .models import Property


class PropertySerializer(serializers.ModelSerializer):
    class Meta:
        model = Property
        fields = ["id", "name", "base_price", "created_at", "updated_at"]
