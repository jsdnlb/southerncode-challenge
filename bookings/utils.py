from datetime import date
from typing import List, Dict
from pricing_rules.models import PricingRule
from properties.models import Property


def calculate_stay_length(start_date: date, end_date: date) -> int:
    """
    Calculate the length of stay between two dates, including both the start and end dates.
    Add +1 one to count the start date, by default it only returns the value between the dates but without counting the start date.

    Args:
        start_date (date): The start date of the stay.
        end_date (date): The end date of the stay.

    Returns:
        int: The length of stay in days
    """
    return (end_date - start_date).days + 1


def sort_pricing_rules(pricing_rules: List[Dict]) -> List[Dict]:
    """
    Sort pricing rules based on the minimum stay length in ascending order.
    It also ensures that elements with None are placed at the beginning of the sort.

    Args:
        pricing_rules (List[Dict]): A list of pricing rules, where each rule is represented as a dictionary.

    Returns:
        List[Dict]: A list of pricing rules sorted in ascending order based on the minimum stay length.
        Rules with no minimum stay length are placed at the end.
    """
    return sorted(
        pricing_rules,
        key=lambda x: (
            x.get("min_stay_length", float("inf"))
            if x.get("min_stay_length") is not None
            else float("-inf")
        ),
    )


def get_pricing_rules(property_id: Property) -> List[Dict]:
    """
    Get pricing rules associated with a property and sort them based on the minimum stay length.

    Args:
        property_id (Property): The ID of the property for which pricing rules are retrieved.

    Returns:
        List[Dict]: A list of pricing rules associated with the property, sorted based on the minimum stay length.
        Each rule is represented as a dictionary containing the fields 'min_stay_length', 'price_modifier', 'specific_day', and 'fixed_price'.
    """
    pricing_rules = PricingRule.objects.filter(property_id=property_id).values(
        "min_stay_length", "price_modifier", "specific_day", "fixed_price"
    )
    return sort_pricing_rules(pricing_rules)


def calculate_final_price(
    pricing_rules: List[Dict],
    start_date: date,
    end_date: date,
    stay_length: int,
    base_price: float,
) -> float:
    """
    Calculates the final price of a booking applying pricing rules.

    Args:
        pricing_rules (List[Dict]): A list of dictionaries containing applicable pricing rules.
        start_date (date): The start date of the booking.
        end_date (date): The end date of the booking.
        stay_length (int): The length of stay in days.
        base_price (float): The base price per day of the property.

    Returns:
        float: The final price of the booking.

    Notes:
        The count_specific_day is used to use the formula to add the final price
        It has a valid condition when there is no discount applied, it is not used within the loop,
        since all the rules are validated there with the values "min_stay_length", "price_modifier", "specific_day", "fixed_price"
    """
    final_price = 0
    count_specific_day = False

    for rule in pricing_rules:
        specific_day = rule.get("specific_day")
        fixed_price = rule.get("fixed_price")
        min_stay_length = rule.get("min_stay_length")
        price_modifier = rule.get("price_modifier")

        if specific_day is not None and fixed_price is not None:
            if start_date <= specific_day <= end_date:
                final_price += fixed_price
                stay_length -= 1
                count_specific_day = True

        if min_stay_length is not None and price_modifier is not None:
            if stay_length >= min_stay_length:
                new_base_price = base_price * stay_length
                price = new_base_price + (new_base_price * price_modifier / 100)
                if count_specific_day:
                    final_price += price
                else:
                    final_price = price

    if final_price == 0 and stay_length > 0 and base_price > 0:
        final_price = base_price * stay_length

    return round(final_price, 2)


def create_property_with_rules(property_data: dict, rules_data: List[dict]) -> Property:
    """
    Create a property along with pricing rules.

    Args:
        property_data (dict): A dictionary containing the data for creating the property.
        rules_data (List[dict]): A list of dictionaries, where each dictionary contains the data for creating
        a pricing rule associated with the property.

    Returns:
        Property: The created property object.
    """
    property = Property.objects.create(**property_data)
    for rule_data in rules_data:
        PricingRule.objects.create(property=property, **rule_data)
    return property
