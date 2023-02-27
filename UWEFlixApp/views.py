from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.generic import ListView
from .models import MonthlyStatement, Club, Movie
from .forms import ClubForm, MovieForm

def home(request):
    return render(request, "UWEFlixApp/test.html")

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
    

def edit_movie(request, Movie_id):
    movie = Movie.objects.get(pk=Movie_id)
    form = MovieForm(request.POST or None, instance=movie)
    if form.is_valid():
        form.save()
        return redirect('home')
    return render(request, 'hello/edit_movie.html', {'movie':movie, 'form':form})
