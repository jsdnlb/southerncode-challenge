from rest_framework.generics import ListAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import status
from django.shortcuts import get_object_or_404
from pricing_rules.models import PricingRule
from pricing_rules.serializers import PricingRuleSerializer
from pricing_rules.filters import PricingRuleFilter


class PricingRuleListView(ListAPIView):
    """
    View for listing and creating pricing rules.

    Lists all existing pricing rules and allows creating new pricing rules
    using the data provided in the request. Supports GET and POST methods.

    Attributes:
        queryset: Queryset returning all existing pricing rules.
        serializer_class: Serializer used for serializing pricing rule data.
        filterset_class: Filters available for filtering pricing rules.
    """

    queryset = PricingRule.objects.all()
    serializer_class = PricingRuleSerializer
    filterset_class = PricingRuleFilter

    def post(self, request: Request, *args, **kwargs) -> Response:
        """
        Accepts a POST request with JSON data representing the new pricing rule.
        Validates the data and saves the new pricing rule to the database if valid.

        Args:
            request (Request): The HTTP request object containing the data.

        Returns:
            Response: The HTTP response object containing the serialized data
            of the created pricing rule or errors if the data is invalid.

        Example:
            Example of request JSON:
            {
                "property": 1,
                "price_modifier": -10,
                "min_stay_length": 7,
                "fixed_price": 20,
                "specific_day": "01-04-2022"
            }
        """
        serializer = PricingRuleSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PricingRuleDetailView(RetrieveUpdateDestroyAPIView):
    """
    Retrieves, updates, or deletes a single pricing rule instance identified
    by its unique identifier. Supports GET, PUT, PATCH, and DELETE methods.

    Attributes:
        queryset: Queryset returning all existing pricing rules.
        serializer_class: Serializer used for validating and deserializing
            pricing rule data.
        lookup_url_kwarg: Name of the URL keyword argument used to retrieve
            the unique identifier of the pricing rule.
    """

    queryset = PricingRule.objects.all()
    serializer_class = PricingRuleSerializer
    lookup_url_kwarg = "pk"

    def get_object(self):
        """
        Retrieves the pricing rule instance using the unique identifier provided
        in the URL kwargs and checks the permissions before returning the instance.

        Returns:
            The pricing rule instance identified by its unique identifier.
        """
        queryset = self.filter_queryset(self.get_queryset())
        filter_kwargs = {self.lookup_field: self.kwargs[self.lookup_url_kwarg]}
        obj = get_object_or_404(queryset, **filter_kwargs)
        self.check_object_permissions(self.request, obj)
        return obj

    def delete(self, request: Request, *args, **kwargs) -> Response:
        """
        Deletes the pricing rule instance identified by its unique identifier.
        Returns a success message upon successful deletion.

        Args:
            request (Request): The HTTP request object.

        Returns:
            Response: The response object containing the success message and
            the HTTP status code 200 (OK) upon successful deletion.
        """
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(
            {"detail": "Record successfully deleted."}, status=status.HTTP_200_OK
        )

    def patch(self, request: Request, *args, **kwargs) -> Response:
        """
        Accepts a PATCH request with JSON data representing the partial update
        of the pricing rule instance. Validates the data and performs the partial
        update of the instance.

        Args:
            request (Request): The HTTP request object.

        Returns:
            Response: The response object containing the serialized data
            of the updated pricing rule instance or errors if the data is invalid.
        """
        partial = kwargs.pop("partial", False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)
