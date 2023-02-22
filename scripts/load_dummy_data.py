from UWEFlixApp.models import MonthlyStatement, Club

def run():
    # Create a Club
    club = Club.objects.create(name="UWEFlix", card_number="123456", card_expiry="2020-12-31", discount_rate=0.1, address="Bristol")
    # Create a MonthlyStatement
    monthly_statement = MonthlyStatement.objects.create(club=club, date="2020-01-01", amount=100.00)
    # Print the Club and MonthlyStatement
    club.save()
    monthly_statement.save()