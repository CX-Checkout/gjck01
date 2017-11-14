def checkout(skus):
    if not isinstance(skus, basestring):
        return -1
    total = 0
    for sku in skus:
        try:
            total += get_sku_price(sku)
        except InvalidSKUException:
            return -1

    total -= get_special_offer_discount_for_5As(skus)
    total -= get_special_offer_discount_for_3As(skus)
    total -= get_special_offer_discount_for_Bs(skus)
    total -= get_special_offer_discount_for_Es(skus)
    total -= get_discount_for_buy_2Fs_get_1_free(skus)
    return total

def get_special_offer_discount_for_5As(skus):
    items_required_for_discount = 5
    number_of_As = len(filter(lambda x: x == 'A', skus))
    discounted_price_of_5As = 200
    discount_per_5As = (items_required_for_discount * Price.A) - discounted_price_of_5As
    discount_for_As = (number_of_As / items_required_for_discount) * discount_per_5As
    return discount_for_As

def get_special_offer_discount_for_3As(skus):
    items_required_for_discount = 3
    number_of_As = len(filter(lambda x: x=='A', skus))
    discounted_price_of_3As = 130
    discount_per_3As = (items_required_for_discount * Price.A) - discounted_price_of_3As
    discount_for_As = ((number_of_As % 5) / items_required_for_discount) * 20
    return discount_for_As

def get_special_offer_discount_for_Bs(skus):
    items_required_for_discount = 2
    number_of_Bs = len(filter(lambda x: x == 'B', skus))
    number_of_Es = len(filter(lambda x: x == 'E', skus))
    discounted_price_of_2Bs = 45
    discount_per_2Bs = (items_required_for_discount * Price.B) - discounted_price_of_2Bs
    number_of_free_Bs_in_basket = get_number_of_free_Bs_in_basket(number_of_Bs, number_of_Es)
    discount_for_Bs = ((number_of_Bs - number_of_free_Bs_in_basket) / items_required_for_discount) * discount_per_2Bs;
    return discount_for_Bs

def get_special_offer_discount_for_Es(skus):
    number_of_Es = len(filter(lambda x: x == 'E', skus))
    number_of_Bs = len(filter(lambda x: x == 'B', skus))
    number_of_free_Bs_in_basket = get_number_of_free_Bs_in_basket(number_of_Bs, number_of_Es)
    discount_for_Es = number_of_free_Bs_in_basket * Price.B
    return discount_for_Es

def get_discount_for_buy_2Fs_get_1_free(skus):
    items_required_for_discount = 3
    number_of_3Fs = len(filter(lambda x: x == 'F', skus))
    discounted_price_of_3Fs = 2 * Price.F
    discount_per_3Fs = (items_required_for_discount * Price.F) - discounted_price_of_3Fs
    discount_for_3Fs = (number_of_3Fs / items_required_for_discount) * discount_per_3Fs
    return discount_for_3Fs

def get_number_of_free_Bs_in_basket(number_of_Bs, number_of_Es):
    number_allowed_free_Bs = (number_of_Es / 2)
    return min(number_allowed_free_Bs, number_of_Bs)

def get_sku_price(sku):
    if sku == 'A':
        return Price.A
    if sku == 'B':
        return Price.B
    if sku == 'C':
        return Price.C
    if sku == 'D':
        return Price.D
    if sku == 'E':
        return Price.E
    if sku == 'F':
        return Price.F
    raise InvalidSKUException()

class Price(object):
    A = 50
    B = 30
    C = 20
    D = 15
    E = 40
    F = 10

class InvalidSKUException(Exception):
    pass

