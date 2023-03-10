from django.urls import path
from UWEFlixApp import views
from .models import MonthlyStatement, Club, Movie, Screen, Screening


monthly_statement_list_view = views.ViewMonthlyStatement.as_view(
    queryset=MonthlyStatement.objects.order_by("id")[:5],  
    context_object_name="monthly_statement_list",
    template_name="UWEFlixApp/view_monthly_statement.html",
)

club_list_view = views.ViewClubs.as_view(
    queryset=Club.objects.order_by("id")[:5],
    context_object_name="club_list",
    template_name="UWEFlixApp/view_clubs.html",
)


movie_list_view = views.ViewMovie.as_view(
    queryset=Movie.objects.order_by("id")[:5],
    context_object_name="movie_list",
    template_name="UWEFlixApp/view_movies.html",
)


movie_list_booking = views.ViewMovie.as_view(
    queryset=Movie.objects.order_by("id")[:5],
    context_object_name="movie_list",
    template_name="UWEFlixApp/cust_pick_film.html",
) # This was linking to booking.html


screen_list_view = views.ViewMovie.as_view(
    queryset=Screen.objects.order_by("id")[:5],
    context_object_name="screen_list",
    template_name="UWEFlixApp/view_screens.html",
)




urlpatterns = [
    path("", views.home, name="home"),
    path("cinema_manager_view", views.cinema_manager_view, name="cinema_manager_view"),
    path('list-movies/', movie_list_view, name="list-movies"),
    path('list-screen/', screen_list_view, name="list-screen"),
    path('update_movie/<int:pk>/    ', views.update_movie, name="update_movie"),
    path('delete_movie/<int:pk>/', views.delete_movie, name="delete_movie"),
    path("create_movie/", views.create_movie, name="create_movie"),
    path("view_monthly_statement/", monthly_statement_list_view, name="view_monthly_statement"),
    path("create_club/", views.create_club, name="create_club"),
    path("view_clubs/", club_list_view, name="view_clubs"),
    path('create_screen/', views.create_screen, name='create_screen'),
    path("update_club/<int:pk>/", views.update_club, name="update_club"),
    path("delete_club/<int:pk>/", views.delete_club, name="delete_club"),
    path("booking_start/", movie_list_booking, name="booking_start"),
    path('update_screen/<int:pk>/    ', views.update_screen, name="update_screen"),
    path('delete_screen/<int:pk>/', views.delete_screen, name="delete_screen"),
    path('show_screenings/<int:pk>/', views.show_screening, name="show_screenings"),
    path("show_all_screening/", views.show_all_screening, name="show_all_screening"),
    path('delete_screening/<int:pk>/', views.delete_screening, name="delete_screening"),
    path('createshowings/', views.create_showing, name='createshowings'),
    path('saveshowing/', views.saveshowing, name = 'saveshowing')
]
