"""
Small, illustrative payment-adjacent utility functions.

These are intentionally simple. The point of this project is to demonstrate
JFrog Artifactory + GitHub Actions build integration during the workshop —
not to model real production payment logic. Don't use this for anything real.
"""


def mask_pan(card_number: str, visible_digits: int = 4) -> str:
    """
    Mask all but the last `visible_digits` of a card number.

    >>> mask_pan("4111111111111111")
    '************1111'
    """
    digits = card_number.replace(" ", "").replace("-", "")
    if len(digits) <= visible_digits:
        return digits
    masked_len = len(digits) - visible_digits
    return "*" * masked_len + digits[-visible_digits:]


def is_valid_card_number(card_number: str) -> bool:
    """
    Validate a card number using the Luhn algorithm.

    >>> is_valid_card_number("4111111111111111")
    True
    >>> is_valid_card_number("4111111111111112")
    False
    """
    digits = [int(d) for d in card_number.replace(" ", "").replace("-", "") if d.isdigit()]
    if len(digits) < 2:
        return False

    checksum = 0
    parity = len(digits) % 2
    for i, digit in enumerate(digits):
        if i % 2 == parity:
            digit *= 2
            if digit > 9:
                digit -= 9
        checksum += digit
    return checksum % 10 == 0
