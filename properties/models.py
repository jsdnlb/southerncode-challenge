from django.db import models


class Property(models.Model):
    """
    Model that represents a property.
    A property could be a house, a flat, a hotel room, etc.
    """

    name = models.CharField(max_length=255, blank=True, null=True)
    """name: Name of the property"""
    base_price = models.FloatField(null=True, blank=True)
    """base_price: base price of the property per day"""
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=False)
    """created_at: Date of creation"""
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=False)
    """updated_at: Date of update"""

    def __str__(self):
        return f"{self.name} - ${self.base_price}"
