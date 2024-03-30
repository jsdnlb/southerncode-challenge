from rest_framework import serializers
from bookings.models import Booking


class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = [
            "id",
            "property",
            "start_date",
            "end_date",
            "stay_length",
            "final_price",
            "created_at",
            "updated_at",
        ]