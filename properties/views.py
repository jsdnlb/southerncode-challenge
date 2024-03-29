from rest_framework.generics import ListAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import Property
from .serializers import PropertySerializer


class PropertyListView(ListAPIView):
    queryset = Property.objects.all()
    serializer_class = PropertySerializer

    def post(self, request, *args, **kwargs):
        serializer = PropertySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PropertyDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Property.objects.all()
    serializer_class = PropertySerializer

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({"detail": "Record successfully deleted."}, status=status.HTTP_200_OK)

    def patch(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)


def get_object(self):
    queryset = self.filter_queryset(self.get_queryset())
    filter_kwargs = {self.lookup_field: self.kwargs[self.lookup_url_kwarg]}
    obj = get_object_or_404(queryset, **filter_kwargs)
    self.check_object_permissions(self.request, obj)
    return obj
