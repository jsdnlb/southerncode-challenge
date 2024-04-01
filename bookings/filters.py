import django_filters
from bookings.models import Booking


class BookingFilter(django_filters.FilterSet):
    """
    Filter class for the Booking model.
    """

    start_date = django_filters.DateFilter(
        field_name="start_date",
        lookup_expr=["exact", "lt", "gt"],
        input_formats=["%m-%d-%Y"],
    )
    end_date = django_filters.DateFilter(
        field_name="end_date",
        lookup_expr=["exact", "lt", "gt"],
        input_formats=["%m-%d-%Y"],
    )

    class Meta:
        model = Booking
        fields = {
            "property__name": ["icontains"],
            "stay_length": ["exact", "lt", "gt"],
            "final_price": ["exact", "lt", "gt"],
        }
