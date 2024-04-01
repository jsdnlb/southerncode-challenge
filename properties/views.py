from rest_framework.generics import ListAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import status
from django.shortcuts import get_object_or_404
from properties.models import Property
from properties.serializers import PropertySerializer
from properties.filters import PropertyFilter


class PropertyListView(ListAPIView):
    """
    Retrieves a list of existing properties and supports creating a new
    property instance via POST method.

    Attributes:
        queryset: Queryset returning all existing property instances.
        serializer_class: Serializer used for validating and deserializing
            property data.
        filterset_class: Filterset used for filtering property instances.
    """

    queryset = Property.objects.all()
    serializer_class = PropertySerializer
    filterset_class = PropertyFilter

    def post(self, request: Request, *args, **kwargs) -> Response:
        """
        Create a new property instance.

        Validates the incoming request data and creates a new property instance
        if the data is valid. Returns the serialized data of the created property
        instance upon successful creation.

        Args:
            request: The HTTP request object.

        Returns:
            Response: The response object containing the serialized data of the
            created property instance or errors if the data is invalid.
        """
        serializer = PropertySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PropertyDetailView(RetrieveUpdateDestroyAPIView):
    """
    Retrieves, updates, or deletes a single property instance identified
    by its unique identifier. Supports GET, PUT, PATCH, and DELETE methods.

    Attributes:
        queryset: Queryset returning all existing property instances.
        serializer_class: Serializer used for validating and deserializing
            property data.
        lookup_url_kwarg: Name of the URL keyword argument used to retrieve
            the unique identifier of the property.
    """

    queryset = Property.objects.all()
    serializer_class = PropertySerializer
    lookup_url_kwarg = "pk"

    def get_object(self):
        """
        Retrieves the property instance identified by its unique identifier
        from the database. Raises a 404 Not Found error if the instance
        does not exist.

        Returns:
            Property: The retrieved property instance.

        Raises:
            Http404: If the property instance does not exist.
        """
        queryset = self.get_queryset()
        filter_kwargs = {self.lookup_field: self.kwargs[self.lookup_url_kwarg]}
        obj = get_object_or_404(queryset, **filter_kwargs)
        self.check_object_permissions(self.request, obj)
        return obj

    def delete(self, request: Request, *args, **kwargs) -> Response:
        """
        Deletes the property instance identified by its unique identifier.
        Returns a success message upon successful deletion.

        Args:
            request: The HTTP request object.

        Returns:
            Response: The response object containing the success message
            and the HTTP status code 200 (OK) upon successful deletion.
        """
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(
            {"detail": "Record successfully deleted."}, status=status.HTTP_200_OK
        )

    def patch(self, request: Request, *args, **kwargs) -> Response:
        """
        Accepts a PATCH request with JSON data representing the partial update
        of the property instance. Validates the data and performs the partial
        update of the instance.

        Args:
            request: The HTTP request object.

        Returns:
            Response: The response object containing the serialized data
            of the updated property instance or errors if the data is invalid.
        """
        partial = kwargs.pop("partial", False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)
