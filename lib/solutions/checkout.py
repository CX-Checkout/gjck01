def checkout(skus):
    if not isinstance(skus, basestring):
        return -1
    total = 0
    for sku in skus:
        try:
            total += get_sku_price(sku)
        except InvalidSKUException:
            return -1

    total -= get_special_offer_discount_for_As(skus)
    total -= get_special_offer_discount_for_Bs(skus)
    return total


def get_special_offer_discount_for_As(skus):
    number_of_As = len(filter(lambda x: x == 'A', skus))
    discount_for_As = (number_of_As / 3) * 20;
    return discount_for_As


def get_special_offer_discount_for_Bs(skus):
    number_of_Bs = len(filter(lambda x: x == 'B', skus))
    discount_for_Bs = (number_of_Bs / 2) * 15;
    return discount_for_Bs


def get_sku_price(sku):
    if sku == 'A':
        return 50
    if sku == 'B':
        return 30
    if sku == 'C':
        return 20
    if sku == 'D':
        return 15
    raise InvalidSKUException()


class InvalidSKUException(Exception):
    pass