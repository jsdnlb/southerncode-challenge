from rest_framework.generics import ListAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import status
from django.shortcuts import get_object_or_404
from pricing_rules.models import PricingRule
from pricing_rules.serializers import PricingRuleSerializer
from pricing_rules.filters import PricingRuleFilter


class PricingRuleListView(ListAPIView):
    queryset = PricingRule.objects.all()
    serializer_class = PricingRuleSerializer
    filterset_class = PricingRuleFilter

    def post(self, request: Request, *args, **kwargs) -> Response:
        """
        Method for the creation of pricing rules.

        Args:
            request (Request): The request object containing the data.

        Returns:
            Response: The response object containing the serialized data or errors.

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
    queryset = PricingRule.objects.all()
    serializer_class = PricingRuleSerializer
    lookup_url_kwarg = "pk"

    def get_object(self):
        queryset = self.filter_queryset(self.get_queryset())
        filter_kwargs = {self.lookup_field: self.kwargs[self.lookup_url_kwarg]}
        obj = get_object_or_404(queryset, **filter_kwargs)
        self.check_object_permissions(self.request, obj)
        return obj

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(
            {"detail": "Record successfully deleted."}, status=status.HTTP_200_OK
        )

    def patch(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)
