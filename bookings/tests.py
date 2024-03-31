from datetime import datetime as d
from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from bookings.utils import create_property_with_rules


class BookingCreateTestCase(APITestCase):

    def setUp(self):
        self.list_url = reverse("booking-list")

        # Rules
        RULE_MIN_STAY_3_INCREASE_10 = {"min_stay_length": 3, "price_modifier": 10.0}
        RULE_MIN_STAY_7_DISCOUNT_10 = {"min_stay_length": 7, "price_modifier": -10.0}
        RULE_MIN_STAY_7_DISCOUNT_5 = {"min_stay_length": 7, "price_modifier": -5.0}
        RULE_MIN_STAY_7_DISCOUNT_9 = {"min_stay_length": 7, "price_modifier": -9.0}
        RULE_MIN_STAY_30_DISCOUNT_20 = {"min_stay_length": 30, "price_modifier": -20.0}
        RULE_MIN_STAY_45_DISCOUNT_30 = {"min_stay_length": 45, "price_modifier": -30.0}

        # Dates
        DAY_01_04_2022 = d.strptime("01-04-2022", "%m-%d-%Y").strftime("%Y-%m-%d")
        DAY_01_05_2022 = d.strptime("01-05-2022", "%m-%d-%Y").strftime("%Y-%m-%d")
        self.START_01_01_2022_END_01_10_2022 = {
            "start_date": "01-01-2022",
            "end_date": "01-10-2022",
        }
        self.START_01_01_2022_END_02_14_2022 = {
            "start_date": "01-01-2022",
            "end_date": "02-14-2022",
        }
        self.START_01_01_2022_END_01_03_2022 = {
            "start_date": "01-01-2022",
            "end_date": "01-03-2022",
        }

        # Setup case one
        self.property_one = create_property_with_rules(
            property_data={"name": "House Case 1", "base_price": 10.0},
            rules_data=[RULE_MIN_STAY_7_DISCOUNT_10],
        )

        # Setup case two
        self.property_two = create_property_with_rules(
            property_data={"name": "House Case 2", "base_price": 10.0},
            rules_data=[RULE_MIN_STAY_7_DISCOUNT_10, RULE_MIN_STAY_30_DISCOUNT_20],
        )

        # Setup case three
        self.property_three = create_property_with_rules(
            property_data={"name": "House Case 3", "base_price": 10.0},
            rules_data=[
                RULE_MIN_STAY_7_DISCOUNT_10,
                {"specific_day": DAY_01_04_2022, "fixed_price": 20.0},
            ],
        )

        # Setup case four
        self.property_four = create_property_with_rules(
            property_data={"name": "House Case 4", "base_price": 15.0},
            rules_data=[
                RULE_MIN_STAY_7_DISCOUNT_9,
                {"specific_day": DAY_01_04_2022, "fixed_price": 20.0},
                {"specific_day": DAY_01_05_2022, "fixed_price": 25.0},
            ],
        )

        # Setup case five
        self.property_five = create_property_with_rules(
            property_data={"name": "House Case 5", "base_price": 10.1},
            rules_data=[
                RULE_MIN_STAY_7_DISCOUNT_10,
                RULE_MIN_STAY_30_DISCOUNT_20,
                RULE_MIN_STAY_45_DISCOUNT_30,
            ],
        )

        # Setup case five
        self.property_six = create_property_with_rules(
            property_data={"name": "House Case 6", "base_price": 12},
            rules_data=[
                RULE_MIN_STAY_3_INCREASE_10,
                RULE_MIN_STAY_7_DISCOUNT_5,
            ],
        )

    def test_create_booking_case_1(self):
        booking_data = {"property": self.property_one.pk}
        booking_data.update(self.START_01_01_2022_END_01_10_2022)
        response = self.client.post(self.list_url, booking_data, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["final_price"], 90)
        self.assertEqual(response.data["stay_length"], 10)

    def test_create_booking_case_2(self):
        booking_data = {"property": self.property_two.pk}
        booking_data.update(self.START_01_01_2022_END_01_10_2022)
        response = self.client.post(self.list_url, booking_data, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["final_price"], 90)
        self.assertEqual(response.data["stay_length"], 10)

    def test_create_booking_case_2_greater_than_30_days(self):
        """Validates that you take the largest discount since it complies with the 30-day rule, ignoring the 7-day rule"""
        booking_data = {"property": self.property_two.pk}
        booking_data.update(self.START_01_01_2022_END_02_14_2022)

        response = self.client.post(self.list_url, booking_data, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["final_price"], 360)
        self.assertEqual(response.data["stay_length"], 45)

    def test_create_booking_case_2_equal_to_30_days(self):
        """Validates that you take the largest discount since it complies with the 30-day rule, ignoring the 7-day rule"""
        booking_data = {
            "property": self.property_two.pk,
            "start_date": "01-01-2022",
            "end_date": "01-30-2022",
        }
        response = self.client.post(self.list_url, booking_data, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["final_price"], 240)
        self.assertEqual(response.data["stay_length"], 30)

    def test_create_booking_case_3(self):
        booking_data = {"property": self.property_three.pk}
        booking_data.update(self.START_01_01_2022_END_01_10_2022)

        response = self.client.post(self.list_url, booking_data, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["final_price"], 101)
        self.assertEqual(response.data["stay_length"], 10)

    def test_create_booking_case_4(self):
        booking_data = {"property": self.property_four.pk}
        booking_data.update(self.START_01_01_2022_END_01_10_2022)

        response = self.client.post(self.list_url, booking_data, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["final_price"], 154.2)
        self.assertEqual(response.data["stay_length"], 10)

    def test_create_booking_case_5(self):
        booking_data = {
            "property": self.property_five.pk,
            "start_date": "01-01-2022",
            "end_date": "02-13-2022",
        }

        response = self.client.post(self.list_url, booking_data, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["final_price"], 355.52)
        self.assertEqual(response.data["stay_length"], 44)

    def test_create_booking_case_5_equal_to_45_days(self):
        """Forcing third rule"""
        booking_data = {"property": self.property_five.pk}
        booking_data.update(self.START_01_01_2022_END_02_14_2022)

        response = self.client.post(self.list_url, booking_data, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["final_price"], 318.15)
        self.assertEqual(response.data["stay_length"], 45)

    def test_create_booking_case_6(self):
        booking_data = {"property": self.property_six.pk}
        booking_data.update(self.START_01_01_2022_END_01_03_2022)

        response = self.client.post(self.list_url, booking_data, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["final_price"], 39.6)
        self.assertEqual(response.data["stay_length"], 3)

    def test_create_booking_case_6_greater_than_7_days(self):
        booking_data = {"property": self.property_six.pk}
        booking_data.update(self.START_01_01_2022_END_01_10_2022)

        response = self.client.post(self.list_url, booking_data, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["final_price"], 114)
        self.assertEqual(response.data["stay_length"], 10)
