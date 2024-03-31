from rest_framework.generics import ListAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from bookings.models import Booking
from bookings.serializers import BookingSerializer
from bookings.utils import (
    calculate_final_price,
    calculate_stay_length,
    get_pricing_rules,
)


class BookingListView(ListAPIView):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer

    def post(self, request, *args, **kwargs):
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
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer

    def delete(self, request, *args, **kwargs):
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
    queryset = self.filter_queryset(self.get_queryset())
    filter_kwargs = {self.lookup_field: self.kwargs[self.lookup_url_kwarg]}
    obj = get_object_or_404(queryset, **filter_kwargs)
    self.check_object_permissions(self.request, obj)
    return obj
