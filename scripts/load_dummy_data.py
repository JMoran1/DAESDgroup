from UWEFlixApp.models import MonthlyStatement, Club

def run():
    # Create a Club
    club = Club.objects.create(clubName="UWEFlix", cardNum="123456", expDate="2020-12-31", discountRate=0.1, clubAddress="Bristol")
    # Create a MonthlyStatement
    monthly_statement = MonthlyStatement.objects.create(clubID=club, statementDate="2020-01-01", statementAmount=100.00)
    # Print the Club and MonthlyStatement
    club.save()
    monthly_statement.save()