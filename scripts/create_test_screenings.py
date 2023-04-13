from UWEFlixApp.models import MonthlyStatement, Club, Booking, Screening, Movie, Screen
from random import randint
from string import ascii_letters
from datetime import datetime, timedelta, date, time

def create_random_date():
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

def create_random_movie():
    name = create_random_string()
    # Create a timedelta between 1 and 3 hours
    running_time_hours = randint(1, 3)
    description = create_random_string()
    rating = randint(0, 10)
    movie = Movie.objects.create(name=name, running_time=timedelta(hours=running_time_hours), description=description, rating=rating)
    return movie

def create_random_screen():
    name = create_random_string()
    description = create_random_string()
    capacity = randint(0, 100)
    screen = Screen.objects.create(name=name, description=description, capacity=capacity)
    return screen

def create_random_screening(movie, screen):
    movie = movie
    screen = screen
    # create a random datetime between now and 1 year from now
    showing_at = datetime.now() + timedelta(days=randint(0, 365))
    
    seats_available = randint(0, 100)
    screening = Screening.objects.create(movie=movie, screen=screen, showing_at=showing_at, seats_remaining=seats_available)
    return screening

def create_random_booking(screening, club):
    screening = screening 
    number_of_tickets = randint(0, 10)
    total_price = number_of_tickets * 4.99
    club = club
    date = datetime.now().date()
    booking = Booking.objects.create(screening=screening, number_of_tickets=number_of_tickets, total_price=total_price, club=club, date=date)
    return booking

from datetime import datetime, timedelta
def create_screenings(movie, screen):
    dates = []
    dates.append(datetime.now().date())
    for d in range(1,6):
        dates.append(datetime.now().date() + timedelta(days=d))
    for date in dates:
        for _ in range(10):
            date = datetime.combine(date , time(randint(8, 22),0,0))
            screening = Screening.objects.create(movie=movie, screen=screen, showing_at=date, seats_remaining=screen.capacity)
            screening.save()


def run():
    # Create a Club
    for _ in range(10):
        # Create a Movie
        movie = create_random_movie()
        movie.save()
        # Create a Screen
        screen = create_random_screen()
        screen.save()
        # Create a Screening
        screening = create_screenings(movie, screen)


