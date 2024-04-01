from rest_framework.generics import ListAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import status
from django.shortcuts import get_object_or_404
from bookings.models import Booking
from bookings.serializers import BookingSerializer
from bookings.filters import BookingFilter
from bookings.utils import (
    calculate_final_price,
    calculate_stay_length,
    get_pricing_rules,
)


class BookingListView(ListAPIView):
    """
    View for listing and creating bookings.

    Lists all existing bookings and allows creating a new booking using the
    data provided in the request.

    Supported methods:
        - GET: Lists all existing bookings.
        - POST: Creates a new booking using the provided data.

    When creating a new booking, it automatically calculates the length of
    stay and the final price based on the pricing rules associated with the
    booked property.

    Attributes:
        queryset: Queryset returning all existing bookings.
        serializer_class: Serializer used for validating and deserializing
            booking data.
        filterset_class: Filters available for filtering bookings.
    """

    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    filterset_class = BookingFilter

    def post(self, request: Request, *args, **kwargs) -> Response:
        """
        Creates a new booking using the data provided in the request.

        Automatically calculates the length of stay and the final price based
        on the pricing rules associated with the booked property.

        Returns:
            If the booking data is valid and the booking is created
            successfully, returns a response with the created booking data
            and the HTTP status code 201 (CREATED).
            If the booking data is not valid, returns a response with the
            validation errors and the HTTP status code 400 (BAD REQUEST).
        """
        serializer = BookingSerializer(data=request.data)
        if serializer.is_valid():
            property = serializer.validated_data.get("property")
            pricing_rules = get_pricing_rules(property)
            start_date = serializer.validated_data.get("start_date")
            end_date = serializer.validated_data.get("end_date")
            if start_date and end_date:
                stay_length = calculate_stay_length(start_date, end_date)
                serializer.validated_data["stay_length"] = stay_length

            if pricing_rules:
                final_price = calculate_final_price(
                    pricing_rules,
                    start_date,
                    end_date,
                    stay_length,
                    property.base_price,
                )
                serializer.validated_data["final_price"] = final_price

            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BookingDetailView(RetrieveUpdateDestroyAPIView):
    """
    View for retrieving, updating, or deleting a single booking instance.

    Retrieves, updates, or deletes a single booking instance identified by its
    unique identifier. Supports GET, PUT, PATCH, and DELETE methods.

    Attributes:
        queryset: Queryset returning all existing bookings.
        serializer_class: Serializer used for validating and deserializing
            booking data.
    """

    queryset = Booking.objects.all()
    serializer_class = BookingSerializer

    def delete(self, request: Request, *args, **kwargs) -> Response:
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(
            {"detail": "Record successfully deleted."}, status=status.HTTP_200_OK
        )

    """ def patch(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data) """


def get_object(self):
    """
    Returns the booking instance identified by its unique identifier.

    Retrieves the booking instance using the unique identifier provided in
    the URL kwargs and checks the permissions before returning the instance.

    Returns:
        The booking instance identified by its unique identifier.
    """
    queryset = self.filter_queryset(self.get_queryset())
    filter_kwargs = {self.lookup_field: self.kwargs[self.lookup_url_kwarg]}
    obj = get_object_or_404(queryset, **filter_kwargs)
    self.check_object_permissions(self.request, obj)
    return obj
