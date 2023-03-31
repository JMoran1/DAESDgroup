from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import redirect, render

from UWEFlixApp.forms import ScreeningForm
from UWEFlixApp.models import Movie, Screen, Screening

from .auth import UserRoleCheck

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
