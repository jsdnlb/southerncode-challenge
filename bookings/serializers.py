from rest_framework import serializers
from bookings.models import Booking


class BookingSerializer(serializers.ModelSerializer):
    """
    Serializer for the Booking model.
    The start date and end date of the booking (format: MM-DD-YYYY).
    """

    start_date = serializers.DateField(format="%m-%d-%Y", required=False)
    end_date = serializers.DateField(format="%m-%d-%Y", required=False)

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
