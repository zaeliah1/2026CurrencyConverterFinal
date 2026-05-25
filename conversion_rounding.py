import all_constant as c


def nzd_to_jpy(amount):
    """
    Converts a NZD amount to JPY.
    JPY is returned as a whole number (no decimal subdivisions).
    """
    result = amount * c.NZD_TO_JPY
    return round(result)


def jpy_to_nzd(amount):
    """
    Converts a JPY amount to NZD.
    NZD is returned rounded to 2 decimal places (cents).
    """
    result = amount * c.JPY_TO_NZD
    return round(result, 2)
