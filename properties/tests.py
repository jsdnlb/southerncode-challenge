from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from properties.models import Property
from properties.serializers import PropertySerializer


class PropertyAPITests(APITestCase):

    def setUp(self):
        self.property_data = {"name": "House Case 1", "base_price": 10.0}
        self.property = Property.objects.create(**self.property_data)
        self.url = reverse("property-list")
        self.update_data = {"name": "Updated House Case 1", "base_price": 20.0}


    def test_get_property_list(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_create_property(self):
        response = self.client.post(self.url, self.property_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Property.objects.count(), 2)
        for key, value in self.property_data.items():
            self.assertEqual(response.data[key], value)

    def test_get_property_detail(self):
        detail_url = reverse("property-detail", kwargs={"pk": self.property.pk})
        response = self.client.get(detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, PropertySerializer(self.property).data)
        self.assertEqual(Property.objects.count(), 1)

    def test_update_property(self):
        detail_url = reverse("property-detail", kwargs={"pk": self.property.pk})
        response = self.client.put(detail_url, self.update_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.property.refresh_from_db()
        self.assertEqual(self.property.name, self.update_data["name"])
        self.assertEqual(self.property.base_price, self.update_data["base_price"])

    def test_delete_property(self):
        detail_url = reverse("property-detail", kwargs={"pk": self.property.pk})
        response = self.client.delete(detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(Property.objects.filter(pk=self.property.pk).exists())

    def test_invalid_property_creation(self):
        invalid_data = {
            "name": "House Case 1",
        }
        response = self.client.post(self.url, invalid_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
