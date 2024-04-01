from django.db import models


class Booking(models.Model):
    """
    Model that represent a booking.
    A booking is done when a customer books a property for a given range of days.
    The booking model is also in charge of calculating the final price the customer will pay.
    """

    property = models.ForeignKey(
        "properties.Property", blank=False, null=False, on_delete=models.CASCADE
    )
    """property: The property this booking is for"""
    start_date = models.DateField(blank=False, null=False)
    """start_date: First day of the booking"""
    end_date = models.DateField(blank=False, null=False)
    """end_date: Last date of the booking"""
    stay_length = models.IntegerField(blank=False, null=True)
    """stay_length: Days of stay """
    final_price = models.FloatField(null=True, blank=True)
    """final_price: Calculated final price"""
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=False)
    """created_at: Date of creation"""
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=False)
    """updated_at: Date of update"""

    def __str__(self):
        return f"{self.id} - {self.property.name} - {self.final_price}"
