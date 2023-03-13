from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.generic import ListView
from .models import MonthlyStatement, Club, Movie, Screen, Screening
from .forms import ClubForm, MovieForm, ScreenForm , ShowingForm

def home(request):
    return render(request, "UWEFlixApp/base.html")

def cinema_manager_view(request):
    return render(request, "UWEFlixApp/cmanager.html")

def booking_start(request):
    return render(request, "UWEFlixApp/booking.html")

def delete_movie(request, pk):
    movie = Movie.objects.get(pk=pk)
    movie.delete()
    return redirect("list-movies")
    
def update_movie(request, pk):
    club = Movie.objects.get(pk=pk)
    form = MovieForm(request.POST or None, instance=club)

    if request.method == "POST":
        if form.is_valid():
            form.save()
            return redirect('home')
    return render(request, "UWEFlixApp/edit_movie.html", {"form": form, "button_text": "Update Movie"})
    
def create_club(request):
    form = ClubForm(request.POST or None)

    if request.method == "POST":
        if form.is_valid():
            form.save()
            return redirect('home')
    return render(request, "UWEFlixApp/create_club_form.html", {"form": form, "button_text": "Create Club"})


def create_movie(request):
    form = MovieForm(request.POST or None)

    if request.method == "POST":
        if form.is_valid():
            form.save()
            return redirect('home')
    return render(request, "UWEFlixApp/create_movie_form.html", {"form": form, "button_text": "Create Movie"})

def update_club(request, pk):
    club = Club.objects.get(pk=pk)
    form = ClubForm(request.POST or None, instance=club)

    if request.method == "POST":
        if form.is_valid():
            form.save()
            return redirect('view_clubs')
    return render(request, "UWEFlixApp/create_club_form.html", {"form": form, "button_text": "Update Club"})

def delete_club(request, pk):
    club = Club.objects.get(pk=pk)
    club.delete()
    return redirect("view_clubs")


class ViewClubs(ListView):
    model = Club

    def get_context_data(self, **kwargs):
        context = super(ViewClubs, self).get_context_data(**kwargs)
        return context
        
class ViewMonthlyStatement(ListView):
    model = MonthlyStatement

    def get_context_data(self, **kwargs):
        context = super(ViewMonthlyStatement, self).get_context_data(**kwargs)
        return context
    


class ViewMovie(ListView):
    model = Movie

    def get_context_data(self, **kwargs):
        context = super(ViewMovie, self).get_context_data(**kwargs)
        return context
    
class ViewScreen(ListView):
    model = Screen

    def get_context_data(self, **kwargs):
        context = super(ViewScreen, self).get_context_data(**kwargs)
        return context
    
def edit_movie(request, Movie_id):
    movie = Movie.objects.get(pk=Movie_id)
    form = MovieForm(request.POST or None, instance=movie)
    if form.is_valid():
        form.save()
        return redirect('home')
    return render(request, 'hello/edit_movie.html', {'movie':movie, 'form':form})

def create_screen(request):
    if request.method == 'POST':
        form = ScreenForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('list-screen')
    else:
        form = ScreenForm()
   
    return render(request, 'UWEFlixApp/create_screen.html', {'form': form, "button_text": "Create Screen"})

def create_movie(request):
    form = MovieForm(request.POST or None)

    if request.method == "POST":
        if form.is_valid():
            form.save()
            return redirect('list-movies')
    return render(request, "UWEFlixApp/create_movie_form.html", {"form": form, "button_text": "Create Movie"})


# In progress
def create_screening(request):
    # Retrieve all movies and screens from the database
    movies = Movie.objects.all()
    screens = Screen.objects.all()
    print(movies)
    print(screens)

    if request.method == 'POST':
        # Retrieve the selected movie, screen, and start time from the form
        movie_id = request.POST.get('movie')
        screen_id = request.POST.get('screen')
        start_time = request.POST.get('start_time')

        # Create a new Showing object with the selected movie, screen, and start time
        movie = Movie.objects.get(id=movie_id)
        screen = Screen.objects.get(id=screen_id)
        showings = showings.objects.create(movie=movie, screen=screen, start_time=start_time)

        # Redirect to the list of showings for the selected movie
        return redirect('movie-detail', pk=movie_id)

    context = {
        'movies': movies,
        'screens': screens,
    }
    return render(request, 'UWEFlixApp/create_screening.html', context)

def delete_screen(request, pk):
    screen = Screen.objects.get(pk=pk)
    screen.delete()
    return redirect("list-screen")
    
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
    return render(request, "UWEFlixApp/show_movie_screenings.html", {"showing_list": screening, "movie": movie})

def show_all_screening(request):
    all_screening = Screening.objects.all()
    return render(request, "UWEFlixApp/view_screenings.html", {"all_showings": all_screening})

def delete_screening(request, pk):
    screening = Screening.objects.get(pk=pk)
    screening.delete()
    return redirect("show_all_screening")

def save_screening(request):
    if request.method == 'POST':
        form = ShowingForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('create_screening')
    else:
        form = ShowingForm()
    return render(request, 'UWEFlixApp/create_screening.html', {'form': form})