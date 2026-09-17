from payments_utils.core import mask_pan, is_valid_card_number


def test_mask_pan_default():
    assert mask_pan("4111111111111111") == "************1111"


def test_mask_pan_short_input():
    assert mask_pan("123") == "123"


def test_mask_pan_strips_separators():
    assert mask_pan("4111-1111-1111-1111") == "************1111"


def test_valid_card_number():
    assert is_valid_card_number("4111111111111111") is True


def test_invalid_card_number():
    assert is_valid_card_number("4111111111111112") is False


def test_invalid_short_input():
    assert is_valid_card_number("1") is False
