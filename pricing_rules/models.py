from django.db import models


class PricingRule(models.Model):
    """
    Model that represents a pricing rule that will be applied to a property when booking.
    A rule can have a fixed price, or a percent modifier.
    Only one rule can apply per day.
    We can have multiple rules for the same day, but only the most relevant rule applies.
    """

    property = models.ForeignKey(
        "properties.Property", blank=False, null=False, on_delete=models.CASCADE
    )
    """property: This rule is applied to a particular property"""
    price_modifier = models.FloatField(null=True, blank=True)
    """price_modifier: Represents a percentage that can be positive (increment) or negative (discount)"""
    min_stay_length = models.IntegerField(null=True, blank=True)
    """min_stay_length: This rule applies only if the stay_length of the booking is >= min_stay_length """
    fixed_price = models.FloatField(null=True, blank=True)
    """fixed_price: A rule can have a fixed price for the given day"""
    specific_day = models.DateField(null=True, blank=True)
    """specific_day: A rule can apply to a specific date. Ex: Christmas"""
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=False)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=False)

    def __str__(self):
        return f"{self.property.name} "
