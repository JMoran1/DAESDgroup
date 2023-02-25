from django.urls import path
from UWEFlixApp import views
from .models import MonthlyStatement, Club


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

urlpatterns = [
    path("", views.home, name="home"),
    path("view_monthly_statement/", home_list_view, name="view_monthly_statement"),
    path("cman", views.c_man, name="c_man"),
    path('list-movies/', views.list_movies, name="list-movies"),
    path("view_monthly_statement/", monthly_statement_list_view, name="view_monthly_statement"),
    path("create_club/", views.create_club, name="create_club"),
    path("view_clubs/", club_list_view, name="view_clubs"),
    path("update_club/<int:pk>/", views.update_club, name="update_club"),
    path("delete_club/<int:pk>/", views.delete_club, name="delete_club"),
]
