def check_luhn(card_number):
    """Checks if the card number is valid using the Luhn algorithm
    :param card_number: The card number to check
    :return: True if the card number is valid, False otherwise"""

    card_number = str(card_number)
    num_digits = len(card_number)
    n_sum = 0
    is_second = False

    for i in range(num_digits - 1, -1, -1):
        d = ord(card_number[i]) - ord('0')

        if is_second == True:
            d = d * 2

        n_sum += d // 10
        n_sum += d % 10

        is_second = not is_second

    if n_sum % 10 == 0:
        return True
    else:
        return False