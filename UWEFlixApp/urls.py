from django.urls import path
from UWEFlixApp import views
from .models import MonthlyStatement, Club, Movie, Screen, Screening


monthly_statement_list_view = views.ViewMonthlyStatement.as_view(
    queryset=MonthlyStatement.objects.order_by("-id"),  
    context_object_name="monthly_statement_list",
    template_name="UWEFlixApp/view_monthly_statement.html",
)

club_list_view = views.ViewClubs.as_view(
    queryset=Club.objects.order_by("id"),
    context_object_name="club_list",
    template_name="UWEFlixApp/view_clubs.html",
)


movie_list_view = views.ViewMovie.as_view(
    queryset=Movie.objects.order_by("id"),
    context_object_name="movie_list",
    template_name="UWEFlixApp/view_movies.html",
)


movie_list_booking = views.ViewMovie.as_view(
    queryset=Movie.objects.order_by("id"),
    context_object_name="movie_list",
    template_name="UWEFlixApp/cust_pick_film.html",
) # This was linking to booking.html


screen_list_view = views.ViewMovie.as_view(
    queryset=Screen.objects.order_by("id"),
    context_object_name="screen_list",
    template_name="UWEFlixApp/view_screens.html",
)

screening_list_view = views.ViewMovie.as_view(
    queryset=Screening.objects.order_by("id"),
    context_object_name="screen_list",
    template_name="UWEFlixApp/view_screenings.html",
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
    path('edit_screening/<int:pk>/', views.edit_screening, name='edit_screening'),
    path('show_screenings/<int:pk>/', views.show_screening, name="show_screenings"),
    path("show_all_screening/", screening_list_view, name="show_all_screening"),
    path('delete_screening/<int:pk>/', views.delete_screening, name="delete_screening"),
    path('create_screening/', views.create_screening, name='create_screening'),
    path('create_monthly_statement/', views.create_monthly_statements, name='create_monthly_statement'),
    path('account_manager', views.account_manager_view, name='account_manager'),
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('create_booking/<int:pk>/', views.create_booking, name='create_booking'),
    path('confirm_booking/', views.confirm_booking, name='confirm_booking'),
    path('top_up/', views.club_top_up, name='top_up'),
    path('register/', views.register_student, name='register_student'),
    path("club_rep_view", views.club_rep_view, name="club_rep_view"),
    path('register_club_rep/', views.register_club_rep, name='register_club_rep'),
    path("view_transactions", views.view_transactions, name="view_transactions"),
    path("view_club_transactions/<int:pk>/", views.view_club_transactions, name="view_club_transactions"),
    path("account_page/", views.account_page, name="account_page"),
    path("join_club/", views.join_club, name="join_club"),
    path("accept_club/<int:pk>/", views.accept_join_request, name="accept_club"),
    path("reject_club/<int:pk>/", views.reject_join_request, name="reject_club"),
    path("view_pending_club_requests/", views.view_pending_requests, name="view_pending_club_requests"),
    path("student_view", views.student_view, name="student_view"),
    path("change_ticket_price/", views.change_ticket_price, name="change_ticket_price"),
]
