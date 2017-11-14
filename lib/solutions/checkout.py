from collections import Counter
from copy import deepcopy
from math import floor

def checkout(basket):
    if not isinstance(basket, basestring):
        return -1

    try:
        sku_counts = get_sku_counts(basket)
    except InvalidSKUException:
        return -1

    for offer in GET_ONE_FREE_OFFERS:
        sku_counts = get_basket_with_free_items_removed(
            sku_counts,
            offer['sku_required_for_free_ones'],
            offer['number_required'],
            offer['free_sku'],
        )

    total = 0
    for sku, sku_count in sku_counts.items():
        total += (sku_count * get_sku_price(sku))

    sku_ids_with_discount = [
        k for k, v in SKUS.items() if v.get('discount_offers')
    ]
    for sku_id  in sku_ids_with_discount:
        sku = SKUS[sku_id]
        ordered_dicount_offers = sorted(
                sku['discount_offers'],
                key=lambda x: x['number_required'],
                reverse=True
        )
        discount_offer = ordered_dicount_offers[0]
        number_available_for_discount = sku_counts[sku_id]
        for discount_offer in ordered_dicount_offers:
            discount, number_available_for_discount = \
                get_single_level_offer_discount(
                    number_available_for_discount,
                    discount_offer['number_required'],
                    sku['price'],
                    discount_offer['discounted_price'],
                )
            total -= discount
    return total

def get_basket_with_free_items_removed(
        sku_counts,
        sku_required_for_free_ones,
        number_required,
        free_sku
        ):
    remainig_sku_counts = deepcopy(sku_counts)

    number_of_free_items = \
        sku_counts[sku_required_for_free_ones] / number_required
    remainig_sku_counts[free_sku] \
        = max(sku_counts[free_sku] - number_of_free_items, 0)
    return remainig_sku_counts

def get_single_level_offer_discount(
        sku_counts,
        items_required_for_discount,
        normal_price_per_item,
        discounted_price):
    discount = (items_required_for_discount * normal_price_per_item)\
        - discounted_price
    number_of_discounts = sku_counts / items_required_for_discount
    discount_for_Bs = number_of_discounts * discount
    number_of_undiscounted_items = sku_counts \
        % items_required_for_discount

    return (discount_for_Bs, number_of_undiscounted_items)


def get_sku_price(sku):
    sku = SKUS[sku]
    return sku['price']

def get_sku_counts(basket):
    present_sku_counts = Counter(basket)
    valid_skus = SKUS.keys()
    if not set(list(basket)).issubset(valid_skus):
        raise InvalidSKUException
    sku_counts = {}
    for sku in valid_skus:
        sku_counts[sku] = present_sku_counts.get(sku) or 0

    return sku_counts


SKUS = {
    'A': {'price': 50, 'discount_offers': [
        {'number_required': 5, 'discounted_price': 200},
        {'number_required': 3, 'discounted_price': 130}
    ]},
    'B': {'price': 30, 'discount_offers': [
        {'number_required': 2, 'discounted_price': 45}
    ]},
    'C': {'price': 20},
    'D': {'price': 15},
    'E': {'price': 40},
    'F': {'price': 10},
    'G': {'price': 20},
    'H': {'price': 10, 'discount_offers': [
        {'number_required': 5, 'discounted_price': 45},
        {'number_required': 10, 'discounted_price': 80},
    ]},
    'I': {'price': 35},
    'J': {'price': 60},
    'L': {'price': 90},
    'M': {'price': 15},
    'O': {'price': 10},
    'S': {'price': 30},
    'T': {'price': 20},
    'W': {'price': 20},
    'X': {'price': 90},
    'Y': {'price': 10},
    'Z': {'price': 50},
    'K': {'price': 80, 'discount_offers': [
        {'number_required': 2, 'discounted_price': 150},
    ]},
    'N': {'price': 40},
    'P': {'price': 50, 'discount_offers': [
        {'number_required': 5, 'discounted_price': 200},
    ]},
    'Q': {'price': 30, 'discount_offers': [
        {'number_required': 3, 'discounted_price': 80},
    ]},
    'R': {'price': 50},
    'U': {'price': 40},
    'V': {'price': 50, 'discount_offers': [
        {'number_required': 3, 'discounted_price': 130},
        {'number_required': 2, 'discounted_price': 90},
    ]},
}

# TODO: Need to sort out difference if you're getting a sku
# of the same type for free.
# e.g. buy 2F get on free requires 'number_required=4
GET_ONE_FREE_OFFERS = [
    {
        'sku_required_for_free_ones': 'U',
        'number_required': 4,
        'free_sku': 'U'
    },
    {
        'sku_required_for_free_ones': 'F',
        'number_required': 3,
        'free_sku': 'F'
    },
    {
        'sku_required_for_free_ones': 'E',
        'number_required': 2,
        'free_sku': 'B'
    },
    {
        'sku_required_for_free_ones': 'N',
        'number_required': 3,
        'free_sku': 'M'
    },
    {
        'sku_required_for_free_ones': 'R',
        'number_required': 3,
        'free_sku': 'Q'
    },
]

class InvalidSKUException(Exception):
    pass
