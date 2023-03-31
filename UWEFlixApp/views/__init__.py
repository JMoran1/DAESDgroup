import random
import secrets
from datetime import datetime
from string import ascii_letters, digits

from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib.auth.views import LoginView
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import ListView

from UWEFlixApp.forms import (BookingForm, ClubForm, ClubRepBookingForm, ClubTopUpForm,
                    CustomerRegistrationForm, LoginForm, MovieForm, ScreenForm,
                    ScreeningForm, UserForm)
from UWEFlixApp.models import (Booking, Club, MonthlyStatement, Movie, Screen, Screening,
                     User)

from django.db.models import Sum
from django.shortcuts import get_object_or_404

from .auth import UserRoleCheck
from .booking import create_booking, confirm_booking
from .screening import (
    create_screening, show_screening, show_all_screening, delete_screening,
    edit_screening
)


def home(request):
    if request.user.is_authenticated:
        roles = User.objects.get(username=request.user)
        uType = roles.role
        return render(request, "UWEFlixApp/homepage.html", {'uType': uType})
    else:
        return render(request, "UWEFlixApp/homepage.html")

@login_required()
@user_passes_test(UserRoleCheck(User.Role.CINEMA_MANAGER), redirect_field_name=None)
def cinema_manager_view(request):
    return render(request, "UWEFlixApp/cmanager.html")


def booking_start(request):
    return render(request, "UWEFlixApp/booking.html")



class ViewMonthlyStatement(UserPassesTestMixin, ListView):
    model = MonthlyStatement

    def get_context_data(self, **kwargs):
        context = super(ViewMonthlyStatement, self).get_context_data(**kwargs)
        return context

    def test_func(self):
        return UserRoleCheck(User.Role.CINEMA_MANAGER, User.Role.ACCOUNT_MANAGER)(self.request.user)

    def handle_no_permission(self):
        return redirect('home')



@login_required()
@user_passes_test(UserRoleCheck(User.Role.ACCOUNT_MANAGER), redirect_field_name=None)
def create_monthly_statements(request):
    """Creates a monthly statement for each club in the database"""
    clubs = Club.objects.all()
    for club in clubs:
        bookings = Booking.objects.filter(club=club, date__month=datetime.now().month)
        amount = 0
        for booking in bookings:
            amount += booking.total_price
        ms = MonthlyStatement.objects.create(club=club, amount=amount, date = datetime.now())
        ms.save()

    return redirect("view_monthly_statement")

@login_required()
@user_passes_test(UserRoleCheck(User.Role.ACCOUNT_MANAGER), redirect_field_name=None)
def account_manager_view(request):
    return render(request, "UWEFlixApp/account_manager_page.html")

class CustomLoginView(LoginView):
    template_name = 'UWEFlixApp/login.html'
    authentication_form = LoginForm
    redirect_authenticated_user = True

    def get_success_url(self):
        if self.request.user.role == User.Role.CLUB_REP:
            return reverse_lazy('club_rep_view')
        else:
            return reverse_lazy('home')

def logout_user(request):
    logout(request)
    return redirect('home')


@login_required()
@user_passes_test(UserRoleCheck(User.Role.CLUB_REP), redirect_field_name=None)
def club_top_up(request):
    """Allows club rep to top up club account balance"""
    club = Club.objects.get(pk=1)
    form = ClubTopUpForm(request.POST or None)

    if request.method == "POST":
        if form.is_valid():
            card_number = form.cleaned_data["card_number"]
            expiry_date = form.cleaned_data["card_expiry"]

            if card_number != club.card_number:
                return render(request, "UWEFlixApp/club_top_up.html", {"club": club, "error": "Card number does not match", "form": form})
            
            if expiry_date != club.card_expiry:
                return render(request, "UWEFlixApp/club_top_up.html", {"club": club, "error": "Expiry date does not match", "form": form})

            club.balance += form.cleaned_data["amount"]
            club.save()
            return redirect('home')


    return render(request, "UWEFlixApp/club_top_up.html", {"form": form})

def register_customer(request):
    """Allows a customer to register for an account"""
    form = CustomerRegistrationForm(request.POST or None)

    if request.method == "POST":
        if form.is_valid():
            password1 = form.cleaned_data["password1"]
            password2 = form.cleaned_data["password2"]

            if password1 != password2:
                return render(request, "UWEFlixApp/register.html", {"error": "Passwords do not match", "form": form})
            else:
                if User.objects.filter(username=form.cleaned_data["username"]).exists():
                    return render(request, "UWEFlixApp/register.html", {"error": "Username already taken", "form": form})
                else:
                    User.objects.create_user(username=form.cleaned_data["username"], password=password1, role=User.Role.CUSTOMER)
                    return redirect('login')

    return render(request, "UWEFlixApp/register.html", {"form": form})


@login_required()
@user_passes_test(UserRoleCheck(User.Role.CLUB_REP), redirect_field_name=None)
def club_rep_view(request):
    """Displays the club rep page"""
    return render(request, "UWEFlixApp/club_rep_page.html")


@login_required()
@user_passes_test(UserRoleCheck(User.Role.CINEMA_MANAGER), redirect_field_name=None)
def register_club_rep(request):
    """Allows a cinema manager register a club rep"""
    if request.method == 'POST':
        username = random.randint(100000, 999999)
        password = ''.join(secrets.choice(ascii_letters + digits)
                           for i in range(8))
        if not User.objects.filter(username=username).exists():
            User.objects.create_user(
                username=username, password=password, role=User.Role.CLUB_REP)
            return render(request, "UWEFlixApp/create_club_rep_success.html", {"username": username, "password": password})
    return render(request, "UWEFlixApp/create_club_rep.html")


@login_required()
@user_passes_test(UserRoleCheck(User.Role.CLUB_REP), redirect_field_name=None)
def view_transactions(request):
    """Displays all transactions for the club"""
    # TODO: Change to get club from session when club rep is given a club
    club = Club.objects.get(pk=1)
    bookings = Booking.objects.filter(club=club, date__month=datetime.now().month)
    return render(request, "UWEFlixApp/view_transactions.html", {"transaction_list": bookings})



@login_required()
@user_passes_test(UserRoleCheck(User.Role.ACCOUNT_MANAGER), redirect_field_name=None)
def view_club_transactions(request, pk):
    """Displays all transactions for the club for the current mmonth"""
    club = get_object_or_404(Club, pk=pk)
    bookings = Booking.objects.filter(
        club=club, date__month=datetime.now().month)
    total = 0
    for booking in bookings:
        total += booking.total_price
    # TODO: Change this when moving to docker
    # total = Booking.objects.filter(club__pk=pk, date__month=datetime.now()
    #                                .month).aggregate(Sum('total_price'))['total_price__sum'] or 0
    return render(request, "UWEFlixApp/view_club_transactions.html", {"transaction_list": bookings, "club": club, "total": total, "month": datetime.now()})


def account_page(request):
    """Redicted log in users to approprate pages"""
    if request.user.role == User.Role.CUSTOMER:
        return redirect("booking_start")
    elif request.user.role == User.Role.CLUB_REP:
        return redirect("club_rep_view")
    elif request.user.role == User.Role.ACCOUNT_MANAGER:
        return redirect("account_manager")
    elif request.user.role == User.Role.CINEMA_MANAGER:
        return redirect("cinema_manager_view")
    else:
        return redirect("home")
