from django.db import models


class Booking(models.Model):
    """
        Model that represent a booking.
        A booking is done when a customer books a property for a given range of days.
        The booking model is also in charge of calculating the final price the customer will pay.
    """
    property = models.ForeignKey('properties.Property', blank=False, null=False, on_delete=models.CASCADE)
    """property: The property this booking is for"""
    date_start = models.DateField(blank=False, null=False)
    """date_start: First day of the booking"""
    date_end = models.DateField(blank=False, null=False)
    """date_end: Last date of the booking"""
    final_price = models.FloatField(null=True, blank=True)
    """final_price: Calculated final price"""
