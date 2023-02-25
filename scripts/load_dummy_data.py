from UWEFlixApp.models import MonthlyStatement, Club
from random import randint
from string import ascii_letters

def create_random_date():
    from datetime import datetime
    from random import randint
    year = randint(2022, 2023)
    month = randint(1, 12)
    day = randint(1, 28)
    date = datetime(year, month, day)
    date = date.date()
    return str(date)

def create_random_string():
    length = randint(5, 10)
    string = "".join([ascii_letters[randint(0, len(ascii_letters) - 1)] for _ in range(length)])
    return string

def create_random_club():
    name = create_random_string()
    card_number = randint(100000, 999999)
    card_expiry = create_random_date()
    discount_rate = randint(0, 100)
    address = create_random_string()
    club = Club.objects.create(name=name, card_number=card_number, card_expiry=card_expiry, discount_rate=discount_rate, address=address)
    return club

def create_random_monthly_statement(club):
    club = club
    date = create_random_date()
    amount = randint(0, 100)
    monthly_statement = MonthlyStatement.objects.create(club=club, date=date, amount=amount)
    return monthly_statement

def run():
    # Create a Club
    for _ in range(10):
        club = create_random_club()
        club.save()
        # Create a MonthlyStatement
        monthly_statement = create_random_monthly_statement(club)
        monthly_statement.save()