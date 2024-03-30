from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from properties.models import Property
from pricing_rules.models import PricingRule
from pricing_rules.serializers import PricingRuleSerializer


class PricingRuleCreateTestCase(APITestCase):
    def setUp(self):
        self.property = Property.objects.create(name="Test Property", base_price=10.0)
        self.list_url = reverse("pricing-rule-list")
        self.detail_url = reverse(
            "pricing-rule-detail", kwargs={"pk": self.property.pk}
        )
        self.rule_data = {
            "property": self.property.pk,
            "fixed_price": 20,
            "specific_day": "01-04-2022",
        }
        self.rule1 = PricingRule.objects.create(
            min_stay_length=7, price_modifier=-10.0, property=self.property
        )
        self.rule2 = PricingRule.objects.create(
            property=self.property, min_stay_length=14, price_modifier=15.0
        )
        self.update_data = {
            "property": self.property.pk,
            "min_stay_length": 5,
            "price_modifier": 20.0,
        }

    def test_get_pricing_rule_list(self):
        response = self.client.get(self.list_url)
        expected_data = PricingRuleSerializer([self.rule1, self.rule2], many=True).data
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, expected_data)

    def test_create_pricing_rule(self):
        response = self.client.post(self.list_url, self.rule_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(PricingRule.objects.filter(property=self.property).exists())
        self.assertEqual(PricingRule.objects.count(), 3)

    def test_get_pricing_rule_detail(self):
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, PricingRuleSerializer(self.rule1).data)
        self.assertEqual(PricingRule.objects.count(), 2)

    def test_update_pricing_rule(self):
        response = self.client.put(self.detail_url, self.update_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.rule1.refresh_from_db()
        self.assertEqual(
            self.rule1.min_stay_length, self.update_data["min_stay_length"]
        )
        self.assertEqual(self.rule1.price_modifier, self.update_data["price_modifier"])

    def test_delete_pricing_rule(self):
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(PricingRule.objects.filter(pk=self.rule1.pk).exists())
