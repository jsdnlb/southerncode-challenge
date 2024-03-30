from datetime import date
from typing import List, Dict
from pricing_rules.models import PricingRule
from properties.models import Property


# We add +1 one to count the start date
# By default it only returns the value between the dates but without counting the start date.
# Calculate stay_length dynamically
def calculate_stay_length(start_date: date, end_date: date) -> int:
    return (end_date - start_date).days + 1


# The rules are ordered by min_stay_length from smallest to largest, thus ensuring that regardless of the order in which the price rules are registered, they are applied correctly.
# It also ensures that elements with None are placed at the beginning of the sort.
def sort_pricing_rules(pricing_rules: List[Dict]) -> List[Dict]:
    return sorted(
        pricing_rules,
        key=lambda x: (
            x.get("min_stay_length", float("inf"))
            if x.get("min_stay_length") is not None
            else float("-inf")
        ),
    )


def get_pricing_rules(property_id: Property) -> List[Dict]:
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
    final_price = 0
    new_stay_length = stay_length
    count_specific_day = False

    # The count_specific_day is used to use the formula to add the final price
    for rule in pricing_rules:
        if rule["specific_day"] and rule["fixed_price"]:
            if start_date <= rule["specific_day"] <= end_date:
                final_price += rule["fixed_price"]
                new_stay_length = stay_length - 1
                count_specific_day = True

        if rule["min_stay_length"] and rule["price_modifier"]:
            if stay_length >= rule["min_stay_length"]:
                new_base_price = base_price * new_stay_length
                percent_rule = rule["price_modifier"] / 100
                price = new_base_price + (new_base_price * percent_rule)
                if count_specific_day:
                    final_price += price
                else:
                    final_price = price
    return final_price
