from datetime import datetime
from decimal import Decimal
import random
import secrets
from string import ascii_letters, digits

from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib.auth.views import LoginView
from django.db.models import Sum
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views.generic import ListView

from .forms import (
    BookingForm, ClubForm, ClubRepBookingForm, ClubRepRegistrationForm,
    ClubTopUpForm, LoginForm, MovieForm, ScreenForm, ScreeningForm,
    StudentRegistrationForm, JoinClubForm
)
from .models import (
    Booking, Club, MonthlyStatement, Movie, Screen, Screening, User,
)

class UserRoleCheck:
    """
    Custom reusable authentication test for checking User role type(s)
    Usage: pass User.Role roles to check for in the constructor, e.g:
    >>> UserRoleCheck(User.Role.CINEMA_MANAGER, User.Role.ACCOUNT_MANAGER)

    Designed to be used with the @user_passes_test() Django decorator for
    function-based views, but you can totally call it directly via test_func()
    in class-based views that inherit UserPassesTestMixin.
    """
    def __init__(self, *roles):
        self._roles_to_check = roles

    def __call__(self, user):
        return hasattr(user, 'role') and user.role in self._roles_to_check

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

@login_required()
@user_passes_test(UserRoleCheck(User.Role.CINEMA_MANAGER), redirect_field_name=None)
def delete_movie(request, pk):
    movie = Movie.objects.get(pk=pk)
    movie.delete()
    return redirect("list-movies")

@login_required()
@user_passes_test(UserRoleCheck(User.Role.CINEMA_MANAGER), redirect_field_name=None)
def update_movie(request, pk):
    movie = Movie.objects.get(pk=pk)
    form = MovieForm(request.POST or None, instance=movie)

    if request.method == "POST":
        form = MovieForm(request.POST, request.FILES, instance=movie)
        if form.is_valid():
            form.save()
            return redirect('home')
    return render(request, "UWEFlixApp/edit_movie.html", {"form": form, "button_text": "Update Movie"})

@login_required()
@user_passes_test(UserRoleCheck(User.Role.CINEMA_MANAGER, User.Role.ACCOUNT_MANAGER), redirect_field_name=None)
def create_club(request):
    form = ClubForm(request.POST or None)

    if request.method == "POST":
        if form.is_valid():
            form.save()
            return redirect('home')
    return render(request, "UWEFlixApp/create_club_form.html", {"form": form, "button_text": "Create Club"})

@login_required()
@user_passes_test(UserRoleCheck(User.Role.CINEMA_MANAGER), redirect_field_name=None)
def create_movie(request):
    form = MovieForm(request.POST or None)

    if request.method == "POST":
        form = MovieForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('cinema_manager_view')
    return render(request, "UWEFlixApp/create_movie_form.html", {"form": form, "button_text": "Create Movie"})

@login_required()
@user_passes_test(UserRoleCheck(User.Role.CINEMA_MANAGER, User.Role.ACCOUNT_MANAGER), redirect_field_name=None)
def update_club(request, pk):
    club = Club.objects.get(pk=pk)
    form = ClubForm(request.POST or None, instance=club)

    if request.method == "POST":
        if form.is_valid():
            form.save()
            return redirect('view_clubs')
    return render(request, "UWEFlixApp/create_club_form.html", {"form": form, "button_text": "Update Club"})

@login_required()
@user_passes_test(UserRoleCheck(User.Role.CINEMA_MANAGER, User.Role.ACCOUNT_MANAGER), redirect_field_name=None)
def delete_club(request, pk):
    club = Club.objects.get(pk=pk)
    club.delete()
    return redirect("view_clubs")


class ViewClubs(UserPassesTestMixin, ListView):
    model = Club

    def get_context_data(self, **kwargs):
        context = super(ViewClubs, self).get_context_data(**kwargs)
        return context

    def test_func(self):
        return UserRoleCheck(User.Role.CINEMA_MANAGER, User.Role.ACCOUNT_MANAGER)(self.request.user)
    
    def handle_no_permission(self):
        return redirect('home')


class ViewMonthlyStatement(UserPassesTestMixin, ListView):
    model = MonthlyStatement

    def get_context_data(self, **kwargs):
        context = super(ViewMonthlyStatement, self).get_context_data(**kwargs)
        return context

    def test_func(self):
        return UserRoleCheck(User.Role.CINEMA_MANAGER, User.Role.ACCOUNT_MANAGER)(self.request.user)

    def handle_no_permission(self):
        return redirect('home')

class ViewMovie(ListView):
    model = Movie

    def get_context_data(self, **kwargs):
        context = super(ViewMovie, self).get_context_data(**kwargs)
        return context


class ViewScreen(UserPassesTestMixin, ListView):
    model = Screen

    def get_context_data(self, **kwargs):
        context = super(ViewScreen, self).get_context_data(**kwargs)
        return context

    def test_func(self):
        return UserRoleCheck(User.Role.CINEMA_MANAGER)(self.request.user)
    
    def handle_no_permission(self):
        return redirect('home')

@login_required()
@user_passes_test(UserRoleCheck(User.Role.CINEMA_MANAGER), redirect_field_name=None)
def edit_movie(request, Movie_id):
    movie = Movie.objects.get(pk=Movie_id)
    form = MovieForm(request.POST or None, instance=movie)
    if form.is_valid():
        form.save()
        return redirect('home')
    return render(request, 'hello/edit_movie.html', {'movie': movie, 'form': form})

@login_required()
@user_passes_test(UserRoleCheck(User.Role.CINEMA_MANAGER), redirect_field_name=None)
def create_screen(request):
    if request.method == 'POST':
        form = ScreenForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('list-screen')
    else:
        form = ScreenForm()

    return render(request, 'UWEFlixApp/create_screen.html', {'form': form, "button_text": "Create Screen"})


@login_required()
@user_passes_test(UserRoleCheck(User.Role.CINEMA_MANAGER), redirect_field_name=None)
def create_screening(request):
    # Retrieve all movies and screens from the database
    movies = Movie.objects.all()
    screens = Screen.objects.all()


    if request.method == 'POST':
        # If the form is submitted, save the form
        form = ScreeningForm(request.POST)
        if form.is_valid():
            form.save()
            # Retrieve the selected movie id from the form
            movie_id = form.cleaned_data['movie'].id
            # Redirect to the list of showings for the selected movie
            return redirect('show_all_screening')
        else:
            print(form.errors)
    else:
        # If the form is not submitted, create a new form
        form = ScreeningForm()

    context = {
        'movies': movies,
        'screens': screens,
        'form': form,
    }
    return render(request, 'UWEFlixApp/create_screening.html', context)


@login_required()
@user_passes_test(UserRoleCheck(User.Role.CINEMA_MANAGER), redirect_field_name=None)
def delete_screen(request, pk):
    screen = Screen.objects.get(pk=pk)
    screen.delete()
    return redirect("list-screen")

@login_required()
@user_passes_test(UserRoleCheck(User.Role.CINEMA_MANAGER), redirect_field_name=None)
def update_screen(request, pk):
    screen = Screen.objects.get(pk=pk)
    form = ScreenForm(request.POST or None, instance=screen)

    if request.method == "POST":
        if form.is_valid():
            form.save()
            return redirect('home')
    return render(request, "UWEFlixApp/edit_screen.html", {"form": form, "button_text": "Update Screen"})

def show_screening(request, pk):
    """Takes the pk of a movie and returns a list of screenings for that movie"""
    movie = Movie.objects.get(pk=pk)
    screening = Screening.objects.filter(movie=movie)

    screening = sorted(screening, key=lambda x: x.showing_at)


    dates = []
    screening_dict = {}
    for show in screening:
        date = show.showing_at
        date = date.strftime("%d/%m/%Y")
        if date not in dates:
            dates.append(date)
            screening_dict[date] = []
        screening_dict[date].append(show)

    return render(request, "UWEFlixApp/show_movie_screenings_with_tabs.html", {"showing_list": screening, "movie": movie, "screening_dict": screening_dict})


def show_all_screening(request):
    all_screening = Screening.objects.all()
    return render(request, "UWEFlixApp/view_screenings.html", {"all_showings": all_screening})

@login_required()
@user_passes_test(UserRoleCheck(User.Role.CINEMA_MANAGER), redirect_field_name=None)
def delete_screening(request, pk):
    screening = Screening.objects.get(pk=pk)
    screening.delete()
    return redirect("show_all_screening")

@login_required()
@user_passes_test(UserRoleCheck(User.Role.CINEMA_MANAGER), redirect_field_name=None)
def edit_screening(request, pk):
    screening = Screening.objects.get(pk=pk)

    if request.method == 'POST':
        form = ScreeningForm(request.POST, instance=screening)
        if form.is_valid():
            form.save()
            return redirect('show_all_screening')
    else:
        form = ScreeningForm(instance=screening)
        movies = Movie.objects.all()
        screens = Screen.objects.all()

    context = {
        'form': form,
        'movies': movies,
        'screens': screens,
    }
    return render(request, 'UWEFlixApp/edit_screening.html', context)

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


def create_booking(request, pk):
    user = request.user
    screening = Screening.objects.get(pk=pk)
    date = Screening.objects.get(pk=pk).showing_at

    screeningtext = screening.id
    warning = None
    request.session['selected_screening'] = screeningtext

    if request.method == 'GET':
        if not user.is_anonymous and user.role == User.Role.CLUB_REP:
            form = ClubRepBookingForm()
            return render(request, "UWEFlixApp/booking_form.html", {"form": form, "button_text": "Continue booking", "user": user, "Screening": screening, 'date': date, 'warning': warning})

    if request.method == 'POST':
        if request.user.is_anonymous or request.user.role != User.Role.CLUB_REP:
            request.session['number_of_adult_tickets'] = request.POST.get(
                'number_of_adult_tickets')

            request.session['number_of_child_tickets'] = request.POST.get(
                'number_of_child_tickets')

            request.session['number_of_student_tickets'] = request.POST.get(
                'number_of_student_tickets')
            total_tickets = int(request.POST.get('number_of_adult_tickets')) + int(request.POST.get(
                'number_of_child_tickets')) + int(request.POST.get('number_of_student_tickets'))
            request.session['total_tickets_number'] = total_tickets
            if screening.seats_remaining < total_tickets:
                warning = "Not enough seats available"
                form = BookingForm()
                return render(request, "UWEFlixApp/booking_form.html", {"form": form, "button_text": "Continue booking", "user": user, "Screening": screening, 'date': date, 'warning': warning})


            else:
                if total_tickets > 9:
                    warning = "Too many tickets, no more than 9 in one booking"
                elif total_tickets == 0:
                    warning = "No tickets selected"
                else:
                    return redirect('confirm_booking')
        else:
            request.session['number_of_student_tickets'] = request.POST.get(
                'number_of_student_tickets')
            request.session['number_of_adult_tickets'] = 0

            request.session['number_of_child_tickets'] = 0

            total_tickets = int(request.POST.get('number_of_student_tickets'))
            print(total_tickets)
            request.session['total_tickets_number'] = total_tickets
            if screening.seats_remaining < total_tickets:
                warning = "Not enough seats available"
                form = ClubRepBookingForm()
                return render(request, "UWEFlixApp/booking_form.html", {"form": form, "button_text": "Continue booking", "user": user, "Screening": screening, 'date': date, 'warning': warning})

            else:
                if total_tickets < 9:
                    warning = "A club booking requirement is 10 tickets or more"
                    form = ClubRepBookingForm()
                    return render(request, "UWEFlixApp/booking_form.html", {"form": form, "button_text": "Continue booking", "user": user, "Screening": screening, 'date': date, 'warning': warning})
                else:
                    return redirect('confirm_booking')

    form = BookingForm()

    return render(request, "UWEFlixApp/booking_form.html", {"form": form, "button_text": "Continue booking", "user": user, "Screening": screening, 'date': date, 'warning': warning})


def confirm_booking(request):

    screening = Screening.objects.get(id=request.session['selected_screening'])

    user = request.user
    if not request.user.is_anonymous and request.user.role == User.Role.CLUB_REP:
        club = user.club
        discount_rate = club.discount_rate
    discount = None
    number_of_adult_tickets = int(request.session['number_of_adult_tickets'])
    number_of_child_tickets = int(request.session['number_of_child_tickets'])
    number_of_student_tickets = int(request.session['number_of_student_tickets'])
    total_price = number_of_adult_tickets * Decimal('4.99') + \
        number_of_child_tickets * Decimal('2.99') + \
        number_of_student_tickets * Decimal('3.99')
    subtotal = total_price
    if not request.user.is_anonymous:
        if user.role == User.Role.CLUB_REP:
            total_price *= (1 - discount_rate)

    total_ticket_quantity = number_of_adult_tickets + \
        number_of_child_tickets + number_of_student_tickets
    
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if screening.seats_remaining < total_ticket_quantity:
            return render(request, "UWEFlixApp/confirm_booking.html", {"user": user, "Screening": screening, 'number_of_adult_tickets': number_of_adult_tickets, 'number_of_child_tickets': number_of_child_tickets, 'number_of_student_tickets': number_of_student_tickets, 'total_price': total_price, 'subtotal': subtotal, 'discount': discount, 'total_ticket_quantity': total_ticket_quantity, 'button_text': 'Confirm Booking', 'button_texttwo': 'Cancel Booking', 'warning': 'Too many tickets selected'})
        else:
            if request.user.is_authenticated:
                if user.role == User.Role.CLUB_REP:
                    if club.balance < total_price:
                        return render(request, "UWEFlixApp/confirm_booking.html", {"user": user, "Screening": screening, 'number_of_adult_tickets': number_of_adult_tickets, 'number_of_child_tickets': number_of_child_tickets, 'number_of_student_tickets': number_of_student_tickets, 'total_price': total_price, 'subtotal': subtotal, 'discount': discount, 'total_ticket_quantity': total_ticket_quantity, 'button_text': 'Confirm Booking', 'button_texttwo': 'Cancel Booking', 'warning': 'Insufficient funds'})
                    else:
                        Booking.objects.create(user=user, screening=screening, number_of_adult_tickets=number_of_adult_tickets, total_price=total_price,
                                            number_of_child_tickets=number_of_child_tickets, number_of_student_tickets=number_of_student_tickets, club=club)
                        club.balance = club.balance - total_price
                        club.save()
                        screening.seats_remaining = screening.seats_remaining - total_ticket_quantity
                        screening.save()
                else:
                    Booking.objects.create(user=user, screening=screening, number_of_adult_tickets=number_of_adult_tickets, total_price=total_price,
                                    number_of_child_tickets=number_of_child_tickets, number_of_student_tickets=number_of_student_tickets)
                    screening.seats_remaining = screening.seats_remaining - total_ticket_quantity
                    screening.save()
            else:
                Booking.objects.create(screening=screening, number_of_adult_tickets=number_of_adult_tickets, total_price=total_price,
                                    number_of_child_tickets=number_of_child_tickets, number_of_student_tickets=number_of_student_tickets)
                screening.seats_remaining = screening.seats_remaining - total_ticket_quantity
                screening.save()

            return redirect('home')
    else:
        form = BookingForm()

    return render(request, "UWEFlixApp/confirm_booking.html", {"user": user, "Screening": screening, "numtickets": number_of_adult_tickets, 'button_text': 'Confirm Booking', 'button_texttwo': 'Cancel Booking', 'total_price': total_price, 'total_ticket_quantity': total_ticket_quantity, 'discount': discount, 'subtotal': subtotal})

@login_required()
@user_passes_test(UserRoleCheck(User.Role.CLUB_REP), redirect_field_name=None)
def club_top_up(request):
    """Allows club rep to top up club account balance"""
    club = request.user.club  # WARN: assumes constraints set in the User model have been validated
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

def register_student(request):
    """Allows a student to register for an account"""
    form = StudentRegistrationForm(request.POST or None)

    if request.method == "POST":
        if form.is_valid():
            password1 = form.cleaned_data["password1"]
            password2 = form.cleaned_data["password2"]
            # FIXME: Django user password policy isn't applied here as it is in the admin
            if password1 != password2:
                return render(request, "UWEFlixApp/register.html", {"error": "Passwords do not match", "form": form})
            else:
                if User.objects.filter(username=form.cleaned_data["username"]).exists():
                    return render(request, "UWEFlixApp/register.html", {"error": "Username already taken", "form": form})
                else:
                    u = User.objects.create_user(
                        username=form.cleaned_data["username"],
                        password=password1,
                        role=User.Role.STUDENT,
                    )
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
    form = ClubRepRegistrationForm(request.POST or None)  # or None?

    if request.method == "POST":
        if form.is_valid():
            username = random.randint(100000, 999999)
            password = ''.join(secrets.choice(ascii_letters + digits)
                               for i in range(8))
            if not User.objects.filter(username=username).exists():
                User.objects.create_user(
                    username=username, password=password,
                    role=User.Role.CLUB_REP,
                    club=form.cleaned_data['club']
                ).full_clean()

            return render(
                request,
                "UWEFlixApp/create_club_rep_success.html",
                {"username": username, "password": password}
            )
    return render(
        request,
        "UWEFlixApp/create_club_rep.html",
        {"form": form, "button_text": "Create Club Rep"}
    )


@login_required()
@user_passes_test(UserRoleCheck(User.Role.CLUB_REP), redirect_field_name=None)
def view_transactions(request):
    """Displays all transactions for the club"""
    club = request.user.club  # WARN: assumes constraints set in the User model have been validated
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
    """
    Redirect logged-in users to approprate pages
    """
    if request.user.is_anonymous:
        return redirect('home')  # not logged in
    PAGES_PER_USER_ROLE = {  # the most Pythonic way to emulate switch-case! ;)
        User.Role.STUDENT: 'student_view',
        User.Role.CLUB_REP: 'club_rep_view',
        User.Role.ACCOUNT_MANAGER: 'account_manager',
        User.Role.CINEMA_MANAGER: 'cinema_manager_view',
    }
    return redirect(PAGES_PER_USER_ROLE[request.user.role])

@login_required()
@user_passes_test(UserRoleCheck(User.Role.STUDENT), redirect_field_name=None)
def join_club(request):
    """Allows a student to join a club"""
    form = JoinClubForm(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            club = form.cleaned_data["club"]
            request.user.requested_club = club
            request.user.save()
            return redirect('home')
    return render(request, "UWEFlixApp/join_club.html", {"form": form})

@login_required()
@user_passes_test(UserRoleCheck(User.Role.CLUB_REP), redirect_field_name=None)
def accept_join_request(request, pk):
    """Allows a club rep to accept a join request"""
    user = get_object_or_404(User, pk=pk)
    user.club = user.requested_club
    user.requested_club = None
    user.save()
    return redirect('view_pending_club_requests')


@login_required()
@user_passes_test(UserRoleCheck(User.Role.CLUB_REP), redirect_field_name=None)
def reject_join_request(request, pk):
    """Allows a club rep to reject a join request"""
    user = get_object_or_404(User, pk=pk)
    user.requested_club = None
    user.save()
    return redirect('view_pending_club_requests')
    
@login_required()
@user_passes_test(UserRoleCheck(User.Role.CLUB_REP), redirect_field_name=None)
def view_pending_requests(request):
    """Allows a club rep to view pending requests"""
    club = Club.objects.get(pk=request.user.club.pk)
    users = User.objects.filter(requested_club=club)
    return render(request, "UWEFlixApp/view_requested_club_requests.html", {"users": users})

@login_required()
@user_passes_test(UserRoleCheck(User.Role.STUDENT), redirect_field_name=None)
def student_view(request):
    """Displays the student page"""
    return render(request, "UWEFlixApp/student_view.html")