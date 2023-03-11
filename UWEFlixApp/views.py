from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib.auth.views import LoginView
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.generic import ListView

from .models import MonthlyStatement, Club, Movie, Screen, Screening, User, Booking
from .forms import ClubForm, MovieForm, ScreenForm, LoginForm
from datetime import datetime

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
    return render(request, "UWEFlixApp/base.html")

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
    club = Movie.objects.get(pk=pk)
    form = MovieForm(request.POST or None, instance=club)

    if request.method == "POST":
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
        if form.is_valid():
            form.save()
            return redirect('home')
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
def create_movie(request):
    form = MovieForm(request.POST or None)

    if request.method == "POST":
        if form.is_valid():
            form.save()
            return redirect('list-movies')
    return render(request, "UWEFlixApp/create_movie_form.html", {"form": form, "button_text": "Create Movie"})


# In progress
@login_required()
@user_passes_test(UserRoleCheck(User.Role.CINEMA_MANAGER), redirect_field_name=None)
def createshowings(request):

    return render(request, "UWEFlixApp/test.html")

@login_required()
@user_passes_test(UserRoleCheck(User.Role.CINEMA_MANAGER), redirect_field_name=None)
def delete_screen(request, pk):
    screen = Screen.objects.get(pk=pk)
    screen.delete()
    return redirect("list-screen")

@login_required()
@user_passes_test(UserRoleCheck(User.Role.CINEMA_MANAGER), redirect_field_name=None)
def update_screen(request, pk):
    club = Screen.objects.get(pk=pk)
    form = ScreenForm(request.POST or None, instance=club)

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
    print(screening_dict)

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

def logout_user(request):
    logout(request)
    return redirect('home')
