from django.urls import path
from UWEFlixApp import views
from .models import MonthlyStatement, Club, Movie


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


urlpatterns = [
    path("", views.home, name="home"),
    path("cinema_manager_view", views.cinema_manager_view, name="cinema_manager_view"),
    path('list-movies/', movie_list_view, name="list-movies"),
    path('update_movie/<int:pk>/', views.update_movie, name="update_movie"),
    path("view_monthly_statement/", monthly_statement_list_view, name="view_monthly_statement"),
    path("create_club/", views.create_club, name="create_club"),
    path("view_clubs/", club_list_view, name="view_clubs"),
    path("update_club/<int:pk>/", views.update_club, name="update_club"),
    path("delete_club/<int:pk>/", views.delete_club, name="delete_club"),
]
